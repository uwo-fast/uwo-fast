#!/usr/bin/env python3
"""Build FAST recruiting poster PDFs from Markdown sources in posters/."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml
from PIL import Image

from build_lab_signs import (
    ROOT,
    BuildError,
    check_missing_glyphs,
    last_updated_for,
    parse_frontmatter,
    relative,
    render_qr,
    render_pngs_to,
)

POSTERS_DIR = ROOT / "posters"
OUTPUT_DIR = ROOT / "output" / "posters"
ARTIFACTS_DIR = ROOT / "artifacts" / "posters"
TEMPLATE = ROOT / "templates" / "poster.tex"
FONT_DIR = ROOT / "branding" / "fonts" / "ibm-plex"
LOGO = ROOT / "branding" / "logos" / "FASTlogobw.png"
ACCENT = (0x4F, 0x26, 0x83)

REQUIRED = {
    "title", "slug", "version", "status", "review_owner",
    "eyebrow", "subtitle", "hero", "facts", "work", "looking_for", "apply", "supervisor",
}
STATUSES = {"draft", "review", "approved"}

# Letter width less the template's margins.
CONTENT_WIDTH_IN = 8.5 - 2 * 0.55
HERO_HEIGHT = "2.5in"
HERO_HEIGHT_IN = 2.5
GAP_IN = 0.07


def _quad(points, bbox, credit_at, credit_anchor):
    """One hero panel: its clip shape, the box its photo fills, where its credit sits."""
    return {"points": points, "bbox": bbox, "credit_at": credit_at, "credit_anchor": credit_anchor}


def layout_panels(layout: str) -> list[dict[str, Any]]:
    """Panel shapes for a multi-photo hero, in inches from the hero's bottom left.

    Each panel is a quadrilateral, so every layout is drawn by the same template
    loop. A photo fills its panel's bounding box and is clipped to the shape.
    """
    W, H, g = CONTENT_WIDTH_IN, HERO_HEIGHT_IN, GAP_IN / 2
    if layout == "diagonal":
        # One slanted cut, top further right than bottom.
        bot, top = 0.44 * W, 0.58 * W
        return [
            _quad([(0, 0), (bot - g, 0), (top - g, H), (0, H)], (0, 0, top, H), (0, 0), "south west"),
            _quad([(bot + g, 0), (W, 0), (W, H), (top + g, H)], (bot, 0, W - bot, H), (W, 0), "south east"),
        ]
    if layout == "diagonal3":
        # Two parallel slanted cuts: a wide middle panel between two wings.
        a_bot, a_top, b_bot, b_top = 0.27 * W, 0.37 * W, 0.63 * W, 0.73 * W
        return [
            _quad([(0, 0), (a_bot - g, 0), (a_top - g, H), (0, H)], (0, 0, a_top, H), (0, 0), "south west"),
            _quad([(a_bot + g, 0), (b_bot - g, 0), (b_top - g, H), (a_top + g, H)],
                  (a_bot, 0, b_top - a_bot, H), ((a_bot + b_bot) / 2, 0), "south"),
            _quad([(b_bot + g, 0), (W, 0), (W, H), (b_top + g, H)], (b_bot, 0, W - b_bot, H), (W, 0), "south east"),
        ]
    if layout == "mosaic":
        # One large photo and two stacked on the right.
        x = 0.64 * W
        return [
            _quad([(0, 0), (x - g, 0), (x - g, H), (0, H)], (0, 0, x - g, H), (x - g, 0), "south east"),
            _quad([(x + g, H / 2 + g), (W, H / 2 + g), (W, H), (x + g, H)],
                  (x + g, H / 2 + g, W - x - g, H / 2 - g), (W, H / 2 + g), "south east"),
            _quad([(x + g, 0), (W, 0), (W, H / 2 - g), (x + g, H / 2 - g)],
                  (x + g, 0, W - x - g, H / 2 - g), (W, 0), "south east"),
        ]
    raise BuildError(f"unknown hero layout {layout!r}; use diagonal, diagonal3 or mosaic")


def hero_panels(hero: dict[str, Any], path: Path) -> tuple[list[dict[str, Any]], bool]:
    """Resolve a multi-photo hero into template-ready panels.

    Returns the panels and whether any is still a placeholder.
    """
    shapes = layout_panels(hero["layout"])
    panels = hero.get("panels") or []
    if len(panels) != len(shapes):
        raise BuildError(
            f"{relative(path)}: hero layout {hero['layout']} takes {len(shapes)} panels, got {len(panels)}"
        )
    out, any_placeholder = [], False
    for index, (panel, shape) in enumerate(zip(panels, shapes), start=1):
        any_placeholder |= resolve_image(panel, f"hero panel {index}", path)
        bx, by, bw, bh = shape["bbox"]
        pts = shape["points"]
        entry = {f"p{i}{axis}": f"{v:.3f}" for i, pt in enumerate(shape["points"], start=1)
                 for axis, v in zip("xy", pt)}
        entry.update({
            "bx": f"{bx:.3f}", "by": f"{by:.3f}", "bw": f"{bw:.3f}", "bh": f"{bh:.3f}",
            # Placeholder text centres on the shape, not its bounding box, and is
            # as wide as the shape's average width so a slanted edge cannot clip it.
            # Points run bottom-left, bottom-right, top-right, top-left.
            "cx": f"{sum(x for x, _ in pts) / 4:.3f}", "cy": f"{by + bh / 2:.3f}",
            "tw": f"{max(((pts[1][0] - pts[0][0]) + (pts[2][0] - pts[3][0])) / 2 - 0.4, 0.8):.3f}",
            "credit_x": f"{shape['credit_at'][0]:.3f}", "credit_y": f"{shape['credit_at'][1]:.3f}",
            "credit_anchor": shape["credit_anchor"],
        })
        for key in ("image", "placeholder", "credit"):
            if panel.get(key):
                entry[key] = panel[key]
        out.append(entry)
    return out, any_placeholder


def resolve_image(slot: dict[str, Any], where: str, path: Path) -> bool:
    """Point an image slot at its file, returning whether it is a placeholder.

    A named image that does not exist is a typo, not a missing photo, so it
    fails rather than quietly printing the placeholder box.
    """
    if slot.get("image"):
        image = ROOT / "posters" / slot["image"]
        if not image.is_file():
            raise BuildError(f"{relative(path)}: {where} image not found: {relative(image)}")
        slot["image"] = relative(image)
        return False
    if not slot.get("placeholder"):
        raise BuildError(f"{relative(path)}: {where} needs an image or a placeholder description")
    return True


def tinted_logo() -> Path:
    """The logo recoloured to the accent. Its shape is in the alpha channel."""
    output = ARTIFACTS_DIR / "fast-logo-accent.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    alpha = Image.open(LOGO).getchannel("A")
    logo = Image.new("RGBA", alpha.size, ACCENT + (0,))
    logo.putalpha(alpha)
    logo.save(output)
    return output


def prepare(path: Path, logo: Path) -> dict[str, Any]:
    metadata, body = parse_frontmatter(path, REQUIRED)
    if metadata["status"] not in STATUSES:
        raise BuildError(f"{relative(path)}: status must be one of {sorted(STATUSES)}")

    # A layout is opt-in: without one the single hero photo is used as before,
    # so deleting `layout` and `panels` returns a poster to its single photo.
    if metadata["hero"].get("layout"):
        panels, placeholder = hero_panels(metadata["hero"], path)
        metadata["hero_panels"] = panels
    else:
        placeholder = resolve_image(metadata["hero"], "hero", path)
    if placeholder and metadata["status"] == "approved":
        raise BuildError(f"{relative(path)}: an approved poster cannot carry an image placeholder")

    url = metadata["apply"].get("url")
    if not url:
        raise BuildError(f"{relative(path)}: apply.url is required")
    qr = render_qr(f"{metadata['slug']}-apply", url, ARTIFACTS_DIR / "qr")

    metadata.update({
        "font_dir": relative(FONT_DIR),
        "logo_path": relative(logo),
        "qr_path": relative(qr),
        "apply_display": url.removeprefix("https://").removeprefix("http://").removeprefix("www."),
        "hero_height": HERO_HEIGHT,
        "hero_height_in": f"{HERO_HEIGHT_IN:.3f}",
        "content_width": f"{CONTENT_WIDTH_IN:.3f}",
        "fact_width": f"{(CONTENT_WIDTH_IN - 0.25 * (len(metadata['facts']) - 1)) / len(metadata['facts']):.3f}in",
        "last_updated": last_updated_for(path),
        "draft": metadata["status"] != "approved",
    })
    prepared = ARTIFACTS_DIR / "prepared" / f"{metadata['slug']}.md"
    prepared.parent.mkdir(parents=True, exist_ok=True)
    prepared.write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True) + "---\n\n" + body)
    metadata["prepared"] = prepared
    return metadata


def page_count(pdf: Path) -> int:
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True).stdout
    return int(next(line.split()[1] for line in info.splitlines() if line.startswith("Pages:")))


def render(metadata: dict[str, Any], source: Path) -> Path:
    output = OUTPUT_DIR / f"{metadata['slug']}.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "pandoc", str(metadata["prepared"]),
        "--from", "markdown",
        "--pdf-engine=lualatex",
        "--template", str(TEMPLATE),
        "--resource-path", str(ROOT),
        "-o", str(output),
    ]
    result = subprocess.run(cmd, cwd=ROOT, check=False, text=True, stderr=subprocess.PIPE)
    sys.stderr.write(result.stderr)
    if result.returncode != 0:
        raise BuildError(f"Command failed: {' '.join(cmd)}")
    check_missing_glyphs(result.stderr, source)
    # The layout flows, so content that does not fit lands on a second page.
    pages = page_count(output)
    if pages != 1:
        raise BuildError(f"{relative(source)}: poster runs to {pages} pages; cut text to fit one")
    return output


def poster_files(selected: list[str]) -> list[Path]:
    if selected:
        return [Path(p) if Path(p).is_absolute() else ROOT / p for p in selected]
    return sorted(p for p in POSTERS_DIR.glob("*.md") if p.name != "README.md")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("posters", nargs="*", help="Poster Markdown files; all of posters/ by default.")
    parser.add_argument("--png", action="store_true", help="Also render PNG previews for visual QA.")
    args = parser.parse_args()
    try:
        logo = tinted_logo()
        pdfs = [render(prepare(path, logo), path) for path in poster_files(args.posters)]
        if args.png and render_pngs_to(pdfs, ARTIFACTS_DIR / "png"):
            print(f"Rendered PNG previews in {relative(ARTIFACTS_DIR / 'png')}")
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Built {len(pdfs)} poster PDFs in {relative(OUTPUT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
