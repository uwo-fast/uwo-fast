# Recruiting posters

One-page US-letter posters for FAST projects, built to PDF by `just posters`
(`just posters-preview` also writes PNGs to `artifacts/posters/png`).

Each `posters/<slug>.md` is one poster: the YAML front matter fills the layout in
`templates/poster.tex`, and the Markdown body becomes "The project" paragraph.
Copy `allears.md` to start a new one.

## Rules

- **Real images only.** A photo of the actual hardware, a CAD render from the
  project's repo, or a composite of those. No generated product shots or
  people. Put files in `posters/images/` and name them as `hero.image`.
- **Credit what the licence asks for.** A CC BY or CC BY-SA photo needs
  `hero.credit` (author, licence, source), which prints under the image. A
  photo of a recognisable person needs that person's OK first.
- **No image yet?** Leave `hero.image` out and write `hero.placeholder` as a
  brief for the photo. It prints as a marked box. A poster with a placeholder
  cannot be set to `status: approved`.
- **Facts carry a source.** Anything about funding, partners or results goes in
  `sources` in the front matter, so the next editor can check it.
- **Print the address, too.** `apply.url` becomes the QR code and is printed
  under it for phones that will not scan.

## Multi-photo hero (optional)

Add `layout` and `panels` under `hero` to split the hero band into several
photos. Each panel takes the same `image` / `credit` / `placeholder` keys.

| `layout` | Panels | Shape |
|---|---|---|
| `diagonal` | 2 | One slanted cut |
| `diagonal3` | 3 | Two parallel slanted cuts, wide middle panel |
| `mosaic` | 3 | One large photo, two stacked on the right |

Without `layout` the single `hero.image` is used, so deleting `layout` and
`panels` returns a poster to its single photo. Keep `hero.image` filled in as
that fallback.

## Checks the build makes

- The poster fits on one page. The layout flows, so text that does not fit
  pushes onto a second page and the build fails instead of printing it.
- Every character is in the font (shared with the lab signs).
- A named image exists, and an approved poster has no placeholder.

## Before an approved print

- Confirm the Western purple (`accent` in `templates/poster.tex`, `#4F2683`)
  and any use of the Western name against the Western Brand Standards Guide.
- Scan the printed QR code with a phone.

The typeface is IBM Plex Sans, vendored in `branding/fonts/ibm-plex` under the
SIL Open Font License, so the PDF looks the same on every machine and in CI.
