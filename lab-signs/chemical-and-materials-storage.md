# Chemical and Materials Storage

Status: draft
Review owner: FAST lab manager
Last updated: 2026-07-01

Scope: Local storage reminders for chemicals, flammables, and shared materials in the FAST lab.

## Do Not Guess

- Store chemicals only if you are trained and authorized to handle them.
- Read the label and SDS before storing a chemical.
- Keep chemicals in compatible, labeled, closed containers.
- NEVER store bases in the acid cabinet.
- If you are unsure where something belongs, do not put it away: ask the lab manager, post-doc, or Dr. Pearce.

## Chemical Storage Locations

These local locations need final confirmation before this sign is approved.

| Item / category | Location | Notes |
| --- | --- | --- |
| Acids | Right lower cabinet of the fume hood | Never store bases here. Confirm compatibility before storage. |
| Bases | Left lower fume hood cabinet | Keep separate from acids. Confirm compatibility before storage. |
| Lab-grade flammable solvents | Main flammable cabinet below the hood | Keep closed, labeled, and in approved containers. |
| Spray paints, lubricants, and hardware-store flammables | Yellow flammable cabinet behind and left of the hood | Keep separate from lab-grade solvent storage. |
| Unknown, unlabeled, leaking, damaged, or expired chemical | Do not store | Stop and ask. |

```mermaid
flowchart TD
    A[Chemical or material to store] --> B{Known, labeled, and authorized?}
    B -->|No| C[Do not store. Ask first.]
    B -->|Yes| D{Acid?}
    D -->|Yes| E[Right lower fume hood cabinet. Never with bases.]
    D -->|No| F{Base?}
    F -->|Yes| G[Left lower fume hood cabinet. Never with acids.]
    F -->|No| H{Lab-grade flammable solvent?}
    H -->|Yes| I[Main flammable cabinet below hood.]
    H -->|No| J{Spray paint, lubricant, or hardware-store flammable?}
    J -->|Yes| K[Yellow flammable cabinet behind/left of hood.]
    J -->|No| L[Check SDS and ask before storing.]
```

## General Materials

| Item | Location | Notes |
| --- | --- | --- |
| Glassware, strainers, funnels, and similar shared items | Red standing cabinet on the north wall of TEB6, bottom drawer | Confirm final drawer assignment before approval. |

## Related

- See [Fume Hood](fumehood.md) before working with volatile chemicals.
- See [Waste Disposal](waste-disposal.md) before discarding chemicals or contaminated materials.

## Reference Checks Needed

- Western/UWO chemical storage and hazardous materials procedures.
- SDS and compatibility guidance for chemical categories stored in the lab.
- Local confirmation of cabinet locations and labels.
- Local confirmation of "lab-grade flammables" versus "hardware-store flammables" wording.
