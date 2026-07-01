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
- Review status and owner once metadata support is added.

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
2. FAST lab-specific procedure approved by the lab manager, PI, or responsible equipment owner.
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
- `review`: Awaiting lab manager, PI, equipment owner, or subject-matter review.
- `approved`: Ready to print/post.
- `retired`: No longer active.

Review expectations:

- General housekeeping signs can be reviewed by the lab manager or delegated owner.
- Chemical, hazardous waste, fume hood, spill, and drain-disposal signs need authoritative procedure checks plus local approval.
- Resin printer signs need review by the resin printer owner.
- Power tool signs need review by the person responsible for tool access/training.
- Wiring and high-power signs need review by a qualified person responsible for electrical safety in the lab.

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

> NEVER store bases in the acid cabinet. If you are unsure where a chemical belongs, do not store it: ask the lab manager or Dr. Pearce.

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
Review owner: FAST lab manager
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

## Future Technical Requirements

After the PDF build workflow exists, this guide should be updated with the exact technical requirements for:

- YAML front matter.
- Required metadata fields.
- Mermaid diagrams.
- LaTeX equations.
- Reference formatting.
- FAST logo placement.
- Generated source/provenance metadata.
- PDF rendering checks.

Until then, prioritize clear sign text, verified claims, and review ownership.
