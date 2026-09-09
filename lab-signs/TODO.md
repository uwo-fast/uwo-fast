# Lab Signs — Outstanding Work

What is left before each sign reaches **v1 / `approved`**. Completed work is not tracked
here; see the git history for what has already been closed.

Last reviewed: 2026-09-09. See [AUTHORING.md](AUTHORING.md) for the review process,
reference rules, and approval blockers this list is built from.

All 15 signs are `status: review` at v0.1. AUTHORING defines `review` as awaiting PI,
post-doc, equipment owner, or subject-matter review, which is where they are. That state
builds; only `approved` hard-fails while a `Reference Checks Needed` section remains.

## The current plan: post at `review`, iterate

Signs are printed and posted provisionally so the lab can start using them, with
corrections pen-marked and reprinted over time. That is a lower bar than v1: an item
blocks printing only if a person following the sign could be hurt or misdirected.

## Blocking the first printing

- [ ] **Get a separate sharps container.** Western requires sharps kept out of the
      broken-glass container ([Lab Safety Manual](https://www.uwo.ca/hr/form_doc/health_safety/doc/manuals/lab_safety_manual.pdf)
      8.7). The lab has one combined under-sink bin. The sign is correct; the lab is not.
      The only item where posting as-is leaves a real hazard.
- [ ] **Decide `printers-fgf`.** Untracked, still `draft`, and the build globs
      `lab-signs/*.md`, so it is already in the combined PDF. Finish it or move it out
      before the packet goes to Dr. Pearce.

## For Dr. Pearce, with the packet

Name these rather than leaving him to find them:

- [ ] **Bases share the flammables cabinet.** Western states bases are "incompatible with
      acids, flammables and oxidizers and should be stored on their own". The current
      arrangement is a knowing trade-off against putting bases in a non-rated cabinet. No
      sign text was changed; this needs his call.
- [ ] **The glove rule** on power tools, now resolved from CCOHS, worth him confirming.
- [ ] **The FAST phone number label.** 519-661-2111 ext. 86725 reads "FAST lab" on the
      safety sign. His office, or a general line?
- [ ] **Dress code.** Western Engineering's shop rules require long pants and closed-toe
      shoes. No FAST sign mentions clothing or footwear.

## Status at a glance

Open checks: **20**. `Today?` marks what could be closed in an afternoon without waiting
on anyone outside the group.

| Sign | Tier | Reviewer beyond PI/post-doc | Open | Pages | Today? |
| --- | --- | --- | --- | --- | --- |
| waste-disposal | High / **keystone** | Hazwaste authority | 1 | 3 | no (C1) |
| chemical-and-materials-storage | High | Chemical storage SOP | 1 | 2 | partly |
| fumehood | High | — | **0** | 2 | clear |
| sink | High | Drain authority | 1 | 1 | no (C1) |
| broken-glass-and-sharps | High | Sharps route | 1 | 1 | **yes** |
| batteries-and-ewaste | High | Campus battery route | 1 | 1 | **yes** |
| printers-resin | High | **Alessia R.** | 4 | 2 | no |
| wiring | High | **Cameron B. / Dr. Pearce** | 2 | 2 | partly |
| safety-equipment-and-incidents | High | Incident-route confirm | 1 | 1 | **yes** |
| power-tools | Equipment | Tool-access owner | 1 | 2 | **yes** |
| stationary-tools | Equipment | Training/sign-off owner | 2 | 2 | **yes** |
| printers-fff | Equipment | Printer owner | 1 | 1 | **yes** |
| soldering-station | Equipment | Station owner | 2 | 1 | **yes** |
| manual-tools | Equipment | — (light) | 1 | 1 | **yes** |
| general-storage | Housekeeping | — (light) | 1 | 1 | **yes** |

## Closeable today

Ten of the twenty need only a decision, a number, or a document already in hand.

- [ ] **broken-glass** — who collects the clean-glass container when full.
- [ ] **batteries** — who walks the FAST bins to a campus pail, and how often. TEB is not
      on Western's list of ten drop-off points; the nearest listed is Spencer Engineering,
      Loading Dock, Ground Floor.
- [ ] **safety-equipment** — the exact FAST incident-reporting route.
- [ ] **stationary-tools** — does a documented sign-off process exist, and where.
- [ ] **soldering-station** — write down FAST setup and shutdown expectations.
- [ ] **soldering-station** — photograph or scan the YIHUA 862BD+ paper manual into
      `equipment/soldering-station.md`. No manufacturer-hosted copy exists online.
- [ ] **printers-fff** — which printers are approved for TPU/TPE.
- [ ] **power-tools** — list the grinder, saw, sander and driver models held, so their
      manuals can be gathered.
- [ ] **manual-tools** — decide whether to post cutter ratings.
- [ ] **general-storage** — decide whether to list specific shelves/cabinets yet.

## Needs someone else, or longer

- [ ] **printers-resin** ×4 — Alessia R.'s review (AUTHORING says this happens *after*
      initial posting), the FAST approved solvent list, resin and solvent SDS, and the
      hazardous-waste route for resin, wash liquid, wipes and failed prints.
- [ ] **chemical** — collect the SDS for each category actually held.
- [ ] **sink** — the FAST process for collecting contaminated rinsate. Western's handbook
      covers rinsing empty containers (2.5) but not where the rinsate goes.
- [ ] **waste-disposal** — the FAST local process for oils, greases, lubricants, resins,
      solvents, acids and bases. This is C1 and the last big one.
- [ ] **wiring** ×2 — examples of approved wiring/enclosures, and the applicable equipment
      manuals, datasheets, certification and local code/ESA requirements.
- [ ] **stationary-tools** — local PPE and dust-control requirements per tool.

## Cross-Cutting Blockers

### C1. Name the remaining FAST procedures

The Western-published half is done; signs now cite real documents. What is left is local:

- [ ] **FAST waste-disposal procedure** — oils, greases, lubricants, resins, solvents,
      acids, bases, and where rinsate goes.
- [ ] **FAST resin handling procedure** — approved solvent list, wash/cure workflow, waste
      routing.
- [ ] **FAST spill & incident response** — the exact reporting route.
- [ ] **Stationary-tool training / sign-off process** — documented.

### C2. Safety-binder process

- [ ] Confirm the FAST lab safety binder index exists and define the step for adding or
      updating a sign there. Every sign's approval depends on it.

### C3. QR links — not blocking v1

- [ ] Track as a v1.x enhancement once QR support is built.
- [ ] **Cross-sign links wait on this.** Eleven signs carry 17 Markdown links in their
      Related sections. On paper those render as blue text that does nothing, which is
      what `equipment/README.md` already says: a Markdown link on a wall does nothing,
      and a sign that needs to reach a longer document wants a QR code. Decision on
      2026-09-09 was to leave them until QR support lands rather than convert them to
      plain text now. `printers-fgf` is the exception and already uses plain text.

## Deferred, not blocking

Real work, deliberately not being done now. Recorded so it is not rediscovered.

- [ ] **Diagram legibility.** The flowcharts on `waste-disposal`, `chemical` and `wiring`
      render with text far smaller than body copy. Flipping to `flowchart LR` buys a page
      but shrinks the text further, so it was rejected. Wants a redesign, not a flag flip.
- [ ] **Unicode font in the template.** `templates/lab-sign.tex` has no Unicode font, so
      lualatex silently dropped characters like `°` and `±`. The build now fails loudly
      instead, but a sign still cannot print a degree sign.
- [ ] **Normalise source labels.** Some signs say "Lab Safety Manual", others "Western
      Laboratory Health and Safety Manual".
- **`waste-disposal` stays at 3 pages.** Not fixable by trimming — reclaiming 200pt still
  leaves three, because the flowchart is atomic and dictates the page breaks. Page 3
  carries real references, not a stub. Closes only via the diagram work above.

## Definition of v1

The bar each sign must clear before `status: approved` / `version: "1.0"`:

1. All `## Reference Checks Needed` items resolved and the section removed. **The build
   hard-fails on an `approved` sign that still contains this section.**
2. Every disposal / storage / emergency / PPE / electrical / equipment instruction has a
   cited source **or** a named local FAST procedure.
3. No reference to an "approved procedure" that is not actually identified.
4. The required review owner has checked the final text.
5. The required subject-matter owner has reviewed it.
6. Nothing can be read as authorizing untrained users to do hazardous work.
7. The sign is entered in the FAST lab safety binder process.
8. Front matter bumped: `status: approved`, `version: "1.0"`.
