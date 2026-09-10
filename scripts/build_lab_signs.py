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

import qrcode
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
QR_DIR = ARTIFACTS_DIR / "qr"
# A 22mm cell plus a 2mm gap, against a 188mm text width.
CELLS_PER_ROW = 7

# The published home of each sign. This is a contract: the QR codes printed onto
# posted signs cannot be recalled, so the path must not change. See AUTHORING.md.
SITE_SIGNS_BASE = "https://uwo-fast.github.io/signs"

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
            if not p.name.startswith("_") and p.name not in {"README.md", "AUTHORING.md", "TODO.md"}
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


def sign_url(slug: str) -> str:
    return f"{SITE_SIGNS_BASE}/{slug}/"


# A source bullet may wrap, with the URL on its own continuation line.
SOURCE_RE = re.compile(
    r"^- (?P<label>[^:\n]+?):\s*\n?\s*<(?P<url>https?://[^>]+)>\s*$", re.MULTILINE
)
RELATED_RE = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<slug>[a-z0-9-]+)\.md\)")


def render_qr(name: str, data: str) -> Path:
    """Write one QR and return its path.

    Error correction M. These are posted on a lab wall and get scuffed, but the
    links they carry are long, and every level above M costs modules that make
    the printed code smaller per module rather than more robust.
    """
    QR_DIR.mkdir(parents=True, exist_ok=True)
    code = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=16,
        border=4,
    )
    code.add_data(data)
    code.make(fit=True)
    output = QR_DIR / f"{name}.png"
    code.make_image(fill_color="black", back_color="white").save(output)
    return output


def source_qr_block(slug: str, sources: list[tuple[str, str]]) -> str:
    """Render the sources as a row of QR codes, each captioned with its label.

    A printed URL is unusable: nobody types ninety characters into a phone, so
    the URL text is replaced by the code that reaches it. They sit in one row
    with the caption underneath rather than one code per line, because that way
    the block is a fixed height whatever the number of sources.
    """
    cells = [
        "\\begin{minipage}[t]{22mm}\\centering"
        f"\\includegraphics[width=20mm,height=20mm]{{{relative(render_qr(f'{slug}-sign', sign_url(slug)))}}}\\\\[1pt]"
        "{\\tiny \\textbf{this sign online}\\par}"
        "\\end{minipage}\\hspace{7mm}"
    ]
    for index, (label, url) in enumerate(sources, start=1):
        path = relative(render_qr(f"{slug}-{index}", url))
        cells.append(
            "\\begin{minipage}[t]{22mm}\\centering"
            f"\\includegraphics[width=20mm,height=20mm]{{{path}}}\\\\[1pt]"
            f"{{\\tiny {escape_latex(label)}\\par}}"
            "\\end{minipage}"
        )
    # Wrap here rather than leaving it to LaTeX. Eight cells overran the text
    # width and spilled into the margin without failing the build; the row count
    # is arithmetic, so do the arithmetic.
    rows = [
        "\\hspace{2mm}".join(cells[i : i + CELLS_PER_ROW])
        for i in range(0, len(cells), CELLS_PER_ROW)
    ]
    body = "\\\\[3mm]\n".join(f"\\noindent {row}" for row in rows)
    return "```{=latex}\n" f"{body}\\par\\vspace{{1mm}}\n" "```\n"


def escape_latex(text: str) -> str:
    for char in ("\\", "&", "%", "$", "#", "_", "{", "}"):
        text = text.replace(char, "\\" + char)
    return text


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


def section_bounds(body: str, heading: str) -> tuple[int, int, str] | None:
    """Locate a section, returning its start, end and text."""
    start = body.find(heading)
    if start == -1:
        return None
    rest_at = start + len(heading)
    offset = body.find("\n## ", rest_at)
    end = len(body) if offset == -1 else offset
    return start, end, body[rest_at:end]


def extract_links(section: str) -> tuple[list[tuple[str, str]], str]:
    """Pull every link out of a section, with whatever text is left over.

    Two forms appear on a sign: `- Label: <url>` for an external source, and
    `[Label](slug.md)` for another sign. Both are unusable printed, so both
    become codes. Whatever does not match either is handed back so a note among
    the links is not silently dropped.
    """
    links: list[tuple[str, str]] = []
    kept: list[str] = []
    for line in SOURCE_RE.sub("", section).splitlines():
        match = RELATED_RE.search(line)
        if match:
            links.append((match.group("label").strip(), sign_url(match.group("slug"))))
        elif line.strip():
            kept.append(line)
    links += [(m.group("label").strip(), m.group("url")) for m in SOURCE_RE.finditer(section)]
    return links, "\n".join(kept).strip()


def check_no_links_lost(before: str, after: str, slug: str, path: Path) -> None:
    """Fail if a link disappeared instead of becoming a code.

    The first version of this transform cut the Related section wholesale and
    only looked for sign links in it, so a section of external sources vanished
    from the printed sign with nothing generated in its place. Nothing caught
    it, because the build still succeeded and the page count still looked fine.
    """
    urls = set(re.findall(r"<(https?://[^>]+)>", before))
    signs = {m.group("slug") for m in RELATED_RE.finditer(before)}
    encoded = set()
    for qr in QR_DIR.glob(f"{slug}-*.png"):
        encoded.add(qr)
    expected = len(urls) + len(signs)
    if expected and len(encoded) < expected:
        raise BuildError(
            f"{relative(path)}: {expected} links in the source but only "
            f"{len(encoded)} codes rendered. A link was dropped rather than "
            "turned into a code."
        )
    for url in urls:
        if url in after:
            raise BuildError(
                f"{relative(path)}: {url} is still printed as text rather than "
                "rendered as a code."
            )


def replace_links_with_qr(slug: str, body: str) -> str:
    """Swap every printed link on the sign for a scannable code.

    Related signs and sources share one strip. A second block would cost height
    on every sign; sharing means related signs cost none. A sign named
    mid-sentence cannot carry a code inside the sentence, so its text becomes
    plain and the sign it names joins the strip, where it is reachable.
    """
    sources_heading = "## Sources / Procedure Links"
    related = section_bounds(body, "## Related")
    sources = section_bounds(body, sources_heading)

    links: list[tuple[str, str]] = []
    related_kept = sources_kept = ""
    source_derived = 0
    if related:
        found, related_kept = extract_links(related[2])
        links += found
    if sources:
        found, sources_kept = extract_links(sources[2])
        links += found
        source_derived = len(found)

    spans = sorted([s for s in (related, sources) if s], key=lambda s: s[0])
    segments: list[str] = []
    cursor = 0
    for span in spans:
        segments.append(body[cursor : span[0]])
        cursor = span[1]
    segments.append(body[cursor:])

    # Links written inline, outside either section, still do nothing on paper.
    for segment in segments:
        for match in RELATED_RE.finditer(segment):
            links.append((match.group("label").strip(), sign_url(match.group("slug"))))

    seen: set[str] = set()
    deduped: list[tuple[str, str]] = []
    for label, url in links:
        if url not in seen:
            seen.add(url)
            deduped.append((label, url))
    links = deduped

    if not links:
        return body

    plain = lambda text: RELATED_RE.sub(lambda m: m.group("label"), text)
    segments = [plain(s) for s in segments]
    related_kept, sources_kept = plain(related_kept), plain(sources_kept)

    # Keep the heading the links actually came from. A sign whose only links are
    # related signs or practice material should not have them filed as sources:
    # calling a practice guide a procedure link overstates it.
    strip_heading = sources_heading if source_derived else "## Related"
    new_sources = (
        strip_heading
        + "\n\n"
        + (sources_kept + "\n\n" if sources_kept else "")
        + source_qr_block(slug, links)
        + "\n"
    )
    # A Related section that held only links is replaced by the strip; one with
    # prose in it keeps its heading and that prose.
    new_related = "## Related\n\n" + related_kept + "\n\n" if related_kept else ""

    replacements = []
    for span in spans:
        replacements.append(new_related if span is related else new_sources)
    if not sources:
        replacements.append(new_sources)
        segments.append("")

    out = []
    for index, segment in enumerate(segments):
        out.append(segment)
        if index < len(replacements):
            out.append(replacements[index])
    return "".join(out)


def prepare_markdown(path: Path) -> tuple[dict[str, Any], str]:
    metadata, body = parse_frontmatter(path)
    original = body
    body = replace_links_with_qr(metadata["slug"], body)
    check_no_links_lost(original, body, metadata["slug"], path)
    if metadata.get("include_universal_notice", True):
        notice = universal_notice_markdown()
        # Keep the sign title first; place the standing notice just beneath it.
        heading = re.match(r"#\s+.+\n", body)
        if heading:
            body = body[: heading.end()] + "\n" + notice + "\n" + body[heading.end():]
        else:
            body = notice + "\n\n" + body
    return metadata, body


def pandoc_metadata_args(metadata: dict[str, Any], source_path: Path) -> list[str]:
    # Provenance (commit links, generated timestamp) lives in manifest.json; the
    # sign face only carries the human-useful identifiers, rendered in the footer.
    # The QR and its URL are placed in the body, beside the standing notice, so
    # they are not passed to the template.
    args = [
        "--metadata", f"title={metadata['title']}",
        "--metadata", f"version={metadata['version']}",
        "--metadata", f"status={metadata['status']}",
        "--metadata", f"review_owner={metadata.get('review_owner', '')}",
        "--metadata", f"last_updated={last_updated_for(source_path)}",
        "--metadata", f"source_path={relative(source_path)}",
        "--metadata", f"logo_path={relative(LOGO)}",
    ]
    slug = metadata.get("slug")
    if slug:
        args += ["--metadata", f"sign_url={sign_url(slug).removeprefix('https://')}"]
    return args


def render_pdf(markdown_path: Path, output_path: Path, metadata: dict[str, Any], source_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pandoc",
        str(markdown_path),
        # -smart is deliberate: with smart quotes on, pandoc emits Unicode curly
        # quotes, which the template's font cannot render and which then vanish
        # entirely. Keep it off until the template gains a Unicode font.
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
    # pdftoppm writes one file per page, so a sign that loses a page would keep
    # its stale trailing image here and misrepresent the current PDF.
    shutil.rmtree(PNG_DIR, ignore_errors=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    for pdf in pdf_paths:
        run([*cmd, "-png", "-r", "150", str(pdf), str(PNG_DIR / pdf.stem)])
    return True


def check_renderable(body: str, path: Path) -> None:
    # The LaTeX template has no Unicode font set up, so lualatex drops any
    # non-ASCII character with only a warning: "260 \u00b0C" renders as "260 C"
    # and "\u00b15 V" as "5 V". Fail loudly instead of shipping a corrupted sign.
    bad = sorted({ch for ch in body if ord(ch) > 127})
    if not bad:
        return
    detail = ", ".join(f"{ch!r} (U+{ord(ch):04X})" for ch in bad)
    raise BuildError(
        f"{relative(path)}: non-ASCII characters will not render and would be "
        f"silently dropped from the PDF: {detail}"
    )


def check_reference_policy(metadata: dict[str, Any], body: str, path: Path) -> None:
    has_checks = "## Reference Checks Needed" in body
    if not has_checks:
        return
    status = str(metadata.get("status", "")).lower()
    if status == "approved":
        raise BuildError(f"{path}: approved signs cannot contain Reference Checks Needed")
    print(
        f"warning: {relative(path)} has a Reference Checks Needed section. Open questions\n"
        "         belong in lab-signs/TODO.md, not on a printed sign.",
        file=sys.stderr,
    )


def build(paths: list[Path]) -> dict[str, Any]:
    ctx = git_context()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    prepared_dir = ARTIFACTS_DIR / "prepared"
    prepared_dir.mkdir(parents=True, exist_ok=True)
    # Codes are named by sign and index, so a sign that loses a source would
    # otherwise leave a stale file behind.
    shutil.rmtree(QR_DIR, ignore_errors=True)

    manifest: dict[str, Any] = {
        "generated": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "repository": ctx["repo"],
        "branch": ctx["branch"],
        "commit": ctx["sha"],
        "signs": [],
    }
    combined_parts: list[str] = []

    for path in paths:
        metadata, markdown = prepare_markdown(path)
        check_renderable(markdown, path)
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
            "url": sign_url(metadata["slug"]),
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
