#!/usr/bin/env python3
"""Build FAST lab sign PDFs from Markdown sources."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SIGNS_DIR = ROOT / "lab-signs"
UNIVERSAL_NOTICE = SIGNS_DIR / "_UNIVERSAL_NOTICE.md"
OUTPUT_DIR = ROOT / "output" / "lab-signs"
ARTIFACTS_DIR = ROOT / "artifacts" / "lab-signs"
PNG_DIR = ARTIFACTS_DIR / "png"
TEMPLATE = ROOT / "templates" / "lab-sign.tex"
LOGO = ROOT / "branding" / "logos" / "FASTlogobw.png"
MERMAID_CONFIG = ROOT / "scripts" / "mermaid-puppeteer-config.json"

REQUIRED_FRONTMATTER = {
    "title",
    "slug",
    "version",
    "status",
    "review_owner",
}

MERMAID_RE = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)


class BuildError(RuntimeError):
    pass


def run(cmd: list[str], *, cwd: Path = ROOT, capture: bool = False) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if result.returncode != 0:
        details = ""
        if capture:
            details = f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        raise BuildError(f"Command failed: {' '.join(cmd)}{details}")
    return result.stdout.strip() if capture else ""


def git_value(args: list[str], fallback: str = "") -> str:
    try:
        return run(["git", *args], capture=True)
    except BuildError:
        return fallback


def repository_slug() -> str:
    env_repo = os.environ.get("GITHUB_REPOSITORY")
    if env_repo:
        return env_repo
    remote = git_value(["config", "--get", "remote.origin.url"])
    if remote.startswith("git@github.com:"):
        remote = remote.removeprefix("git@github.com:").removesuffix(".git")
    elif remote.startswith("https://github.com/"):
        remote = remote.removeprefix("https://github.com/").removesuffix(".git")
    return remote or "uwo-fast/uwo-fast"


def git_context() -> dict[str, str]:
    sha = os.environ.get("GITHUB_SHA") or git_value(["rev-parse", "HEAD"], "unknown")
    branch = os.environ.get("GITHUB_REF_NAME") or git_value(["branch", "--show-current"], "main")
    repo = repository_slug()
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    return {
        "sha": sha,
        "short_sha": sha[:8] if sha and sha != "unknown" else "unknown",
        "branch": branch or "main",
        "repo": repo,
        "server": server,
        "run_url": f"{server}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID')}"
        if os.environ.get("GITHUB_RUN_ID")
        else "",
    }


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise BuildError(f"{path}: missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise BuildError(f"{path}: malformed YAML front matter")
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        raise BuildError(f"{path}: front matter must be a mapping")
    missing = sorted(REQUIRED_FRONTMATTER - set(metadata))
    if missing:
        raise BuildError(f"{path}: missing front matter fields: {', '.join(missing)}")
    return metadata, parts[2].strip() + "\n"


def sign_files(selected: list[str], all_signs: bool) -> list[Path]:
    if selected:
        paths = [Path(p) if Path(p).is_absolute() else ROOT / p for p in selected]
    elif all_signs:
        paths = sorted(
            p for p in SIGNS_DIR.glob("*.md")
            if not p.name.startswith("_") and p.name not in {"README.md", "AUTHORING.md"}
        )
    else:
        raise BuildError("Specify --all or one or more sign Markdown files.")
    return paths


def last_updated_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    value = git_value(["log", "-1", "--format=%cs", "--", rel])
    if value:
        return value
    return dt.date.today().isoformat()


def mermaid_command() -> list[str] | None:
    local = ROOT / "node_modules" / ".bin" / "mmdc"
    if local.exists():
        return [str(local)]
    found = shutil.which("mmdc")
    if found:
        return [found]
    npx = shutil.which("npx")
    if npx:
        return [npx, "mmdc"]
    return None


def render_mermaid(markdown: str, sign_artifacts: Path) -> str:
    matches = list(MERMAID_RE.finditer(markdown))
    if not matches:
        return markdown
    cmd = mermaid_command()
    if cmd is None:
        raise BuildError("Mermaid diagrams found, but mmdc/npx is not available. Run npm install first.")
    sign_artifacts.mkdir(parents=True, exist_ok=True)

    def replace(match: re.Match[str]) -> str:
        idx = len(list(sign_artifacts.glob("diagram-*.mmd"))) + 1
        source = sign_artifacts / f"diagram-{idx}.mmd"
        output = sign_artifacts / f"diagram-{idx}.png"
        source.write_text(match.group(1).strip() + "\n")
        mermaid_cmd = [
            *cmd, "-i", str(source), "-o", str(output),
            "-b", "white", "-t", "neutral", "-s", "2",
        ]
        if MERMAID_CONFIG.exists():
            mermaid_cmd.extend(["-p", str(MERMAID_CONFIG)])
        run(mermaid_cmd)
        rel = output.relative_to(ROOT).as_posix()
        # Empty alt text suppresses the "Figure N: ..." caption; the raw-latex
        # fences centre the diagram while letting pandoc resolve the image path.
        return (
            "```{=latex}\n\\begin{center}\n```\n\n"
            f"![]({rel})\n\n"
            "```{=latex}\n\\end{center}\n```"
        )

    return MERMAID_RE.sub(replace, markdown)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_urls(path: Path, ctx: dict[str, str]) -> tuple[str, str]:
    rel = relative(path)
    base = f"{ctx['server']}/{ctx['repo']}/blob"
    branch_url = f"{base}/{ctx['branch']}/{rel}"
    pinned_url = f"{base}/{ctx['sha']}/{rel}"
    return branch_url, pinned_url


def universal_notice_markdown() -> str:
    text = UNIVERSAL_NOTICE.read_text().strip()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    # Demote the leading level-1 heading to a bold label so the notice reads as
    # a compact callout instead of a second page title.
    text = re.sub(r"^#\s+(.+)$", r"**\1**", text, count=1, flags=re.MULTILINE)
    return (
        "```{=latex}\n\\begin{signnotice}\n```\n\n"
        + text
        + "\n\n```{=latex}\n\\end{signnotice}\n```\n"
    )


def append_metadata(
    markdown: str,
    metadata: dict[str, Any],
    path: Path,
    ctx: dict[str, str],
) -> str:
    generated = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    branch_url, pinned_url = source_urls(path, ctx)
    build_ref = f"[build]({ctx['run_url']})" if ctx["run_url"] else "local build"
    lines = [
        "## Sign Metadata",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Version | {metadata['version']} |",
        f"| Status | {metadata['status']} |",
        f"| Review owner | {metadata['review_owner']} |",
        f"| Last updated | {last_updated_for(path)} |",
        "",
        f"Source: `{relative(path)}` "
        f"([current]({branch_url}), [permanent commit {ctx['short_sha']}]({pinned_url})). "
        f"Generated {generated}; {build_ref}.",
    ]
    return markdown.rstrip() + "\n\n" + "\n".join(lines) + "\n"


def prepare_markdown(path: Path, ctx: dict[str, str]) -> tuple[dict[str, Any], str]:
    metadata, body = parse_frontmatter(path)
    if metadata.get("include_universal_notice", True):
        notice = universal_notice_markdown()
        # Keep the sign title first; place the standing notice just beneath it.
        heading = re.match(r"#\s+.+\n", body)
        if heading:
            body = body[: heading.end()] + "\n" + notice + "\n" + body[heading.end():]
        else:
            body = notice + "\n\n" + body
    body = append_metadata(body, metadata, path, ctx)
    return metadata, body


def pandoc_metadata_args(metadata: dict[str, Any], source_path: Path) -> list[str]:
    return [
        "--metadata", f"title={metadata['title']}",
        "--metadata", f"version={metadata['version']}",
        "--metadata", f"status={metadata['status']}",
        "--metadata", f"source_path={relative(source_path)}",
        "--metadata", f"logo_path={relative(LOGO)}",
    ]


def render_pdf(markdown_path: Path, output_path: Path, metadata: dict[str, Any], source_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pandoc",
        str(markdown_path),
        "--from", "markdown+tex_math_dollars-smart",
        "--pdf-engine=lualatex",
        "--template", str(TEMPLATE),
        "--resource-path", str(ROOT),
        *pandoc_metadata_args(metadata, source_path),
        "-o", str(output_path),
    ]
    run(cmd)


def png_command() -> list[str] | None:
    for tool in ("pdftoppm", "pdftocairo"):
        found = shutil.which(tool)
        if found:
            return [found]
    return None


def render_pngs(pdf_paths: list[Path]) -> bool:
    cmd = png_command()
    if cmd is None:
        print("warning: --png requested but pdftoppm/pdftocairo not found", file=sys.stderr)
        return False
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    for pdf in pdf_paths:
        run([*cmd, "-png", "-r", "150", str(pdf), str(PNG_DIR / pdf.stem)])
    return True


def check_reference_policy(metadata: dict[str, Any], body: str, path: Path) -> None:
    has_checks = "## Reference Checks Needed" in body
    if not has_checks:
        return
    status = str(metadata.get("status", "")).lower()
    if status == "approved":
        raise BuildError(f"{path}: approved signs cannot contain Reference Checks Needed")
    print(f"warning: {relative(path)} contains unresolved Reference Checks Needed", file=sys.stderr)


def build(paths: list[Path]) -> dict[str, Any]:
    ctx = git_context()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    prepared_dir = ARTIFACTS_DIR / "prepared"
    prepared_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {
        "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "repository": ctx["repo"],
        "branch": ctx["branch"],
        "commit": ctx["sha"],
        "signs": [],
    }
    combined_parts: list[str] = []

    for path in paths:
        metadata, markdown = prepare_markdown(path, ctx)
        check_reference_policy(metadata, markdown, path)
        sign_artifacts = ARTIFACTS_DIR / str(metadata["slug"])
        markdown = render_mermaid(markdown, sign_artifacts)
        prepared = prepared_dir / f"{metadata['slug']}.md"
        prepared.write_text(markdown)
        output_pdf = OUTPUT_DIR / f"{metadata['slug']}.pdf"
        render_pdf(prepared, output_pdf, metadata, path)
        branch_url, pinned_url = source_urls(path, ctx)
        manifest["signs"].append({
            "title": metadata["title"],
            "slug": metadata["slug"],
            "version": metadata["version"],
            "status": metadata["status"],
            "source": relative(path),
            "pdf": relative(output_pdf),
            "branch_url": branch_url,
            "pinned_url": pinned_url,
            "last_updated": last_updated_for(path),
        })
        combined_parts.append(markdown)

    combined_md = prepared_dir / "FAST-lab-signs-combined.md"
    combined_md.write_text("\n\n\\newpage\n\n".join(combined_parts) + "\n")
    combined_meta = {
        "title": "FAST Lab Signs",
        "version": "0.1",
        "status": "draft",
        "review_owner": "PI / post-doc",
    }
    render_pdf(combined_md, OUTPUT_DIR / "FAST-lab-signs-combined.pdf", combined_meta, SIGNS_DIR / "README.md")

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("signs", nargs="*", help="Specific sign Markdown files to build.")
    parser.add_argument("--all", action="store_true", help="Build all public lab signs.")
    parser.add_argument(
        "--png",
        action="store_true",
        help="Also render PNG previews of each PDF into artifacts (for visual QA).",
    )
    args = parser.parse_args()
    try:
        paths = sign_files(args.signs, args.all)
        manifest = build(paths)
        if args.png and render_pngs(sorted(OUTPUT_DIR.glob("*.pdf"))):
            print(f"Rendered PNG previews in {relative(PNG_DIR)}")
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Built {len(manifest['signs'])} sign PDFs in {relative(OUTPUT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
