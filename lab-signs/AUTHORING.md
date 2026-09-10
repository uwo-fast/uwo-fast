# Lab Sign Authoring Guide

This guide defines how to write, review, and maintain FAST lab signs in this directory.

The signs are practical wall reminders for trained lab users. They are not substitutes for training, SOPs, equipment manuals, or Western University procedures.

## Core Rule

Every sign should reinforce the same safety culture:

- If you are unsure, uncomfortable, or not trained, stop and ask.
- Do not do work you are not trained or authorized to do.
- Signs remind people of the correct process; they do not grant permission to use equipment or handle materials.
- Asking early is expected lab behavior.

## When To Make A Sign

Create or revise a sign when the lab needs a short, visible reminder for:

- A common mistake or repeated cleanup problem.
- A local storage, disposal, or equipment location rule.
- A decision people need to make at the point of work.
- A high-risk "stop and ask" situation.
- A QR link to a longer guide, SOP, manual, or authoritative procedure.

Do not use a wall sign for long training content. If the material needs step-by-step instruction, make or link a guide/SOP and keep the sign as the quick reminder.

## Required Sign Content

Every public sign should include:

- A clear title.
- The scope: what area, equipment, material, or process the sign applies to.
- Required behavior.
- Prohibited behavior where relevant.
- What to do when unsure.
- Local FAST lab details when they matter, such as cabinet, bin, station, or owner.
- Related signs or QR-linked resources when useful.
- Review status and owner, set in the YAML front matter (see [Front Matter and Build](#front-matter-and-build)).

Every posted sign must also be represented in the FAST lab safety binder. When a sign is added, revised, replaced, or retired, update the binder copy/index at the same time.

## Reference Rules

Use authoritative references for claims that depend on policy, procedure, regulation, safety data, or external instructions.

References are required for:

- Western/UWO procedures.
- Hazardous waste, chemical waste, drain disposal, recycling, and e-waste rules.
- Chemical storage and compatibility guidance.
- Fume hood, spill, PPE, emergency, and incident procedures.
- Equipment-specific procedures from a manufacturer or owner.
- Numerical safety limits, equations, ratings, thresholds, or engineering criteria.
- Claims that a material belongs in a specific campus, municipal, or hazardous waste stream.

References are usually not required for:

- General housekeeping reminders.
- Simple local etiquette.
- Common mechanical safety reminders.
- Basic tool-selection reminders.
- "Stop and ask if unsure."

Preferred source order:

1. Western University / UWO official pages, policies, procedures, and safety documents.
2. FAST lab-specific procedure approved by the PI, a post-doc, or responsible equipment owner.
3. Ontario or Canadian government guidance where applicable.
4. Recognized standards bodies or safety organizations.
5. Manufacturer manuals or official equipment documentation.
6. Reputable educational resources for background only.

Avoid using casual web pages as primary sources for safety-critical claims. Wikipedia may be useful for orientation, but not as the authority for posted safety procedure.

## Research Workflow

Use `_reference/` for untracked research notes, downloaded documents, source captures, and temporary files. Keep durable sign text and approved references in `lab-signs/`.

For each researched source, record:

- Source title.
- URL.
- Accessed date.
- Which sign and claim it supports.
- Whether the source is required for sign text or only background.

Do not mark a safety-critical sign approved until the relevant procedure and local practice have both been checked.

## Review States

Use these states while working:

- `notes`: Rough captured ideas.
- `draft`: Written as sign copy but not fully verified.
- `review`: Awaiting PI, post-doc, equipment owner, or subject-matter review.
- `approved`: Ready to print/post.
- `retired`: No longer active.

Review expectations:

- The PI is the ultimate local authority for FAST lab signs.
- Post-docs may be escalation contacts and may approve or coordinate review when delegated by the PI.
- General housekeeping signs can be reviewed by the PI, a post-doc, or a delegated owner.
- Chemical, hazardous waste, fume hood, spill, and drain-disposal signs need authoritative procedure checks plus PI/post-doc approval.
- Resin printer signs should be reviewed by the resin printer owner after initial posting, then revised and reposted if needed.
- Power tool signs need review by the PI, a post-doc, or the person responsible for tool access/training.
- Wiring and high-power signs need review by Cameron B., Dr. Pearce, or another qualified electrical reviewer identified by them.

## Approval Blockers

Do not mark a sign `approved` (`status: approved` in the front matter) while any of these are unresolved:

- It still has `status: draft`, `review`, or `notes`.
- It has open items in [TODO.md](TODO.md). The build also refuses to render an `approved` sign that still contains a `Reference Checks Needed` section, which should no longer appear in a sign body at all.
- It gives disposal, storage, emergency, PPE, electrical, or equipment-specific instructions without a source or local procedure.
- It names an "approved procedure" that is not actually identified.
- The review owner has not checked the final sign text.
- A required subject-matter owner has not reviewed it.
- The sign could reasonably be read as authorizing untrained users to perform hazardous work.
- The sign has not been added to the FAST lab safety binder process.

For safety-critical signs, unresolved questions should stay visible in the draft until they are answered.

## Reference Section Format

A sign carries its sources and nothing else about its own provenance:

```markdown
## Sources / Procedure Links

- Source title: <https://example.com/source>
```

**Open questions do not go on a printed sign.** They belong in [TODO.md](TODO.md),
tracked per sign. A wall reminder is read by someone deciding what to do at the bench;
telling them the lab has not yet confirmed who empties a bin is noise at best, and at
worst it undermines the instructions around it.

`Reference Checks Needed` sections were previously kept in the sign body while a sign was
in draft. They are not any more. The build still warns if one reappears, and still
hard-fails on an `approved` sign that contains one, as a guard against regression.

## Writing Style

Write for someone standing at the work area who needs the answer quickly.

Prefer:

- Short sections.
- Short bullets.
- Direct verbs.
- Local locations and actions.
- "Ask first" language for uncertain cases.
- QR links to longer guidance.

Avoid:

- Long paragraphs.
- Repeated warnings.
- Dense explanations.
- Unverified disposal or safety instructions.
- Language that implies untrained users may perform hazardous work.
- Emotional wording in final posted signs, even when the underlying issue is serious.

Good final sign language is firm and calm:

> NEVER store bases in the acid cabinet. If you are unsure where a chemical belongs, do not store it: ask the PI or a post-doc.

## Choosing The Right Format

Use bullets for short actions:

- Wear required PPE.
- Clamp the work.
- Clear the print bed.
- Keep the sink open for shared use.

Use tables for classification:

- Waste stream selection.
- Chemical storage locations.
- Tool type versus intended use.
- Printer material versus disposal route.
- Fume hood line color versus utility.

Use flowcharts for decisions:

- Can this go in the sink?
- Is this hazardous waste?
- Which chemical cabinet should this go in?
- Should this polymer scrap be reused, recycled, or discarded?
- Should I proceed or ask first?

Use QR links for detail:

- Training guides.
- SOPs.
- Western/UWO procedures.
- Manufacturer manuals.
- Full reference lists.

**Every link on a sign is printed as a QR code, not as text.** A URL on paper cannot be
used: nobody types ninety characters into a phone, and a Markdown link to another sign is
just blue ink. The build strips both and renders one code per link instead.

Write sources the normal way and the build does the rest:

```markdown
## Sources / Procedure Links

- Source title: <https://example.com/source>
```

The `## Related` bullets are folded into the same strip, pointing at
`https://uwo-fast.github.io/signs/<slug>/` for the sign they name, so nobody has to go
looking for another sign on the wall. A sign named mid-sentence is handled the same way:
its text becomes plain and it joins the strip.

The strip also leads with the sign's **own** code, captioned "this sign online". Keeping
every code in one strip is deliberate: a separate block beside the title reads better but
costs roughly 40pt on the first page, which pushed the two tightest signs onto a second
page. The strip is a fixed height whatever it holds, so this costs nothing.

The strip wraps at seven codes per row. That is arithmetic against the text width, not
something LaTeX is left to work out: eight cells overran the margin without failing the
build.

The label before the colon becomes the caption under the code, so keep it short. It is
what someone reads to decide which code to scan.

**Treat the sign URL as a contract.** A printed code cannot be recalled, so
`/signs/<slug>/` encodes neither the repo name nor a directory: this repo can be
restructured without breaking codes already on a wall.

## Warning Language

Reserve strong warning language for genuinely high-risk actions.

- `STOP`: Do not continue without training, approval, or review.
- `NEVER`: Hard prohibition.
- `ASK FIRST`: Variable or uncertain cases.
- `REMEMBER`: Routine reminder.

If every line is a warning, nothing stands out. Keep the strongest language for the decisions that can injure people, damage equipment, contaminate waste streams, or violate procedure.

## Draft Sign Template

Use this as a starting structure until the PDF workflow defines required front matter.

```markdown
# Sign Title

Status: draft
Review owner: PI / post-doc
Last updated: YYYY-MM-DD

Scope: One short sentence describing where or when this sign applies.

## Before You Start

- Use this only if trained.
- Stop and ask if you are unsure.

## Always

- Do the most important required action.
- Keep the local area/equipment ready for the next user.

## Never

- Do not do the highest-risk prohibited action.
- Do not guess about disposal, storage, or equipment setup.

## Local Details

| Item | Location / Action |
| --- | --- |
| Example item | Example local instruction |

## Related

- Related sign or guide.
- Authoritative procedure or QR target.
```

## Front Matter and Build

Signs are built to PDF by `scripts/build_lab_signs.py` (see `lab-signs/README.md` for setup and commands). Each sign starts with YAML front matter:

```yaml
---
title: "Sink"                 # display title, shown in the page header
slug: "sink"                  # output filename (sink.pdf); match the source filename stem
version: "0.1"
status: "draft"               # notes | draft | review | approved | retired
review_owner: "PI / post-doc"
include_universal_notice: true  # optional, defaults to true
---
```

`title`, `slug`, `version`, `status`, and `review_owner` are required; the build fails if any are missing.

What the build adds automatically, so you do not write it into each sign:

- **Universal notice** — the boxed "Before You Work" callout from `_UNIVERSAL_NOTICE.md` is inserted just below the sign title, unless `include_universal_notice: false`. Edit it in one place; it updates on every sign.
- **Sign Metadata** — a small table (version, status, review owner, last updated) plus a source/provenance line is appended to the end of each sign.
- **Header/footer** — FAST logo, title, `version | status`, source path, and page numbers.

Content features you can use in a sign body:

- **Mermaid diagrams** — a ```` ```mermaid ```` fenced block is rendered to a centred PNG. Prefer simple flowcharts; dense diagrams print small.
- **Math** — `$P = IV$` inline, or `$$ ... $$` for display equations.
- **Tables and bullets** — standard Markdown; use tables for classification and bullets for short actions.

Do not hand-add a `DRAFT` banner or a metadata table; the header status and the appended metadata cover both.
