# Lab Signs — Road to v1

Tracking what remains before each sign can graduate from `draft` to **v1 / `approved`** and be printed and posted.

Last reviewed: 2026-07-05. See [AUTHORING.md](AUTHORING.md) for the review process, reference rules, and approval blockers this list is built from.

## How to use this file

- Each sign has its own section listing what is **blocking approval**.
- Cross-cutting work that unblocks several signs at once is grouped under [Cross-Cutting Blockers](#cross-cutting-blockers) — do these first.
- A sign is ready for v1 only when its section is clear **and** it passes the [Definition of v1](#definition-of-v1) checklist.

## Definition of v1

Every sign must satisfy all of these before `status: approved` / `version: "1.0"` (from AUTHORING.md → Approval Blockers):

- [ ] All `## Reference Checks Needed` items resolved and the section removed. **The build hard-fails on an `approved` sign that still contains this section.**
- [ ] Every disposal / storage / emergency / PPE / electrical / equipment instruction has a cited source **or** a named local FAST procedure.
- [ ] No reference to an "approved procedure" that is not actually identified (see cross-cutting item below).
- [ ] The required review owner has checked the final text.
- [ ] The required subject-matter owner has reviewed it (varies by sign — noted per section).
- [ ] Nothing can be read as authorizing untrained users to do hazardous work.
- [ ] The sign is entered in the FAST lab safety binder process.
- [ ] Front matter bumped: `status: approved`, `version: "1.0"`.

## Status at a glance

| Sign | Tier | Required reviewer(s) beyond PI/post-doc | Open checks | Pages |
| --- | --- | --- | --- | --- |
| waste-disposal | High / **keystone** | Hazwaste + drain authority | 3 | 3 |
| chemical-and-materials-storage | High | Chemical storage SOP | 2 | 2 |
| fumehood | High | Fume hood procedure | 1 | 2 |
| sink | High | Drain-disposal authority | 2 | 1 |
| broken-glass-and-sharps | High | Sharps disposal route | 2 | 1 |
| batteries-and-ewaste | High | Campus battery/e-waste route | 2 | 1 |
| printers-resin | High | **Alessia R.** (resin owner) | 4 | 2 |
| wiring | High | **Cameron B. / Dr. Pearce** | 5* | 3 |
| safety-equipment-and-incidents | High | Location + incident-route confirm | 3 | 2 |
| power-tools | Equipment | Tool-access/training owner | 2 | 2 |
| stationary-tools | Equipment | Training/sign-off owner | 5* | 1 |
| printers-fff | Equipment | Printer/material owner | 1 | 1 |
| soldering-station | Equipment | Station owner | 2 | 1 |
| manual-tools | Equipment | — (light) | 1 | 1 |
| general-storage | Housekeeping | — (light) | 2 | 1 |

`*` Some "checks" are really source links that belong in a Sources section (see per-sign notes).

## Cross-Cutting Blockers

These block multiple signs; resolving each clears items across the set.

### C1. Define and name the FAST procedures the signs defer to
Many signs say "follow the approved procedure" / "the waste-disposal procedure" / "emergency procedures" / "approved workflow." AUTHORING treats an unidentified "approved procedure" as an approval blocker. Author or point to a real document for each:
- [ ] **FAST waste-disposal procedure** — drain rules; handling of oils, greases, lubricants, resins, solvents, acids, bases (unblocks waste-disposal, sink, chemical, fumehood, printers-fff, general-storage).
- [ ] **FAST resin handling procedure** — approved solvent list, wash/cure workflow, cleanup, resin/solvent waste routing (unblocks printers-resin).
- [ ] **FAST spill & incident response** — spill steps + the exact incident-reporting route for FAST (unblocks safety-equipment, sink, printers-resin).
- [ ] **Chemical storage / compatibility SOP** — including where special-hazard classes go (unblocks chemical, fumehood).
- [ ] **Stationary-tool training / sign-off process** — documented (unblocks stationary-tools, power-tools TEB6 reference).

### C2. One lab walk-through to confirm all physical locations
Batch-verify every location/bin/cabinet a sign names, in one pass, once the layout is stable:
- [ ] Battery bin + e-waste bin (TEB7 south wall counter); accepted chemistries.
- [ ] Under-sink broken-glass/sharps bin; whether separate containers are required.
- [ ] Chemical cabinets: acids (right-lower hood), bases (left-lower hood), flammable cabinets, yellow floor cabinet — confirm current assignments.
- [ ] Fume hood **utility line colours** (currently yellow=vacuum, orange=air, green=cold water) — verify against the actual hood; a wrong mapping is dangerous.
- [ ] Resin waste containers (hazardous-waste + resin bag) locations.
- [ ] Safety equipment: eyewash, spill kit, safety shower, first aid kit, fire extinguisher, safety binder, emergency-contact signage.
- [ ] Red standing cabinet drawer assignments (general storage).
- [ ] Sink cleaning log — confirm it exists and where.

### C3. Fix Sources sections for consistency
- [ ] **stationary-tools** and **wiring**: real source URLs currently live inside `## Reference Checks Needed`. Split them into a proper `## Sources / Procedure Links` section (they are resolved sources, not open questions).
- [ ] **printers-fff** and **general-storage**: no `## Sources / Procedure Links` section. Confirm whether any authoritative source is required (general-storage is housekeeping and may legitimately need none; printers-fff makes equipment/material claims that likely need a source or local procedure).
- [ ] **soldering-station**: replace the "YIHUA 862BD+ … product/manual source needed" placeholder with the real manual link.

### C4. Set up the safety-binder process
- [ ] Confirm the FAST lab safety binder index exists and define the step for adding/updating a sign there. Every sign's approval depends on it.

### C5. Optional (not blocking v1): QR links
AUTHORING encourages QR links to longer guidance; chemical notes a future inventory QR. Track as a v1.x enhancement once QR support is built — not required for graduation.

---

# Per-Sign Blockers

## Waste & Disposal

### waste-disposal.md — KEYSTONE, do first
Current: `draft` v0.1, PI/post-doc, 3 pages, has decision diagram. Many other signs defer to this one, so its gaps cascade.
- [ ] Confirm Western/UWO **drain-disposal rules**.
- [ ] Define the **FAST local process** for oils, greases, lubricants, resins, solvents, acids, and bases (→ C1).
- [ ] Confirm whether any battery or e-waste types are excluded from the TEB7 bins (align with batteries-and-ewaste).
- [ ] Reviewer: PI/post-doc + hazardous-waste authority. This is the reference other disposal signs point to — approve it before or with them.

### sink.md
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Western/UWO **drain-disposal rules specific to lab sinks**.
- [ ] Approved process for rinsing/cleaning chemical containers, contaminated tools, and rinsate (→ C1 waste-disposal procedure).
- [ ] Confirm the referenced **cleaning log** exists and where to sign it (→ C2).
- [ ] Reviewer: PI/post-doc + drain-disposal authority.

### broken-glass-and-sharps.md
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Confirm exact Western disposal route for the under-sink broken-glass/sharps bin.
- [ ] Confirm whether separate containers are needed for clean glass, sharps, and contaminated sharps (→ C2).
- [ ] Reviewer: PI/post-doc + sharps/hazwaste authority.

### batteries-and-ewaste.md
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Confirm which battery chemistries the TEB7 battery bin accepts.
- [ ] Confirm the final campus destination/process for the FAST battery and e-waste bins (→ C2).
- [ ] Reviewer: PI/post-doc + campus battery/e-waste route.

## Chemicals & Fume Hood

### chemical-and-materials-storage.md
Current: `draft` v0.1, PI/post-doc, 2 pages, has storage decision diagram.
- [ ] SDS and compatibility guidance for the chemical categories stored in the lab.
- [ ] Confirm where oxidizers, peroxide formers, water-reactives, toxics, and compressed gases should be stored — the sign deliberately says "do not guess," so these locations must be defined elsewhere (→ C1 storage SOP).
- [ ] Verify the storage table + diagram match the **current** cabinet assignments (→ C2).
- [ ] Confirm the chemical inventory spreadsheet is the source of truth (QR link is future, non-blocking).
- [ ] Reviewer: PI/post-doc + chemical storage authority.

### fumehood.md
Current: `draft` v0.1, PI/post-doc, 2 pages.
- [ ] Confirm whether powder work has additional requirements beyond fume-hood use.
- [ ] **Verify the utility line colour table** (yellow=vacuum, orange=air, green=cold water) against the actual hood (→ C2) — safety-critical.
- [ ] Confirm the alarm/out-of-service and max-exhaust wording matches the hood's actual controls/procedure.
- [ ] Reviewer: PI/post-doc + fume-hood procedure authority.

## Tools

### power-tools.md
Current: `draft` v0.1, PI/post-doc, 2 pages.
- [ ] Gather tool manuals for the specific grinders, saws, sanders, drills, and drivers in use.
- [ ] Confirm a Western/UWO job hazard analysis or shop-safety guidance for hand-held power tools.
- [ ] Confirm the TEB7 (hand-held, honour system) vs TEB6 (stationary, sign-off) policy split is accurate (→ ties to stationary-tools / C1).
- [ ] Reviewer: PI/post-doc + person responsible for tool access/training.

### stationary-tools.md
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Confirm the **documented sign-off process** for stationary tools exists and reference it (→ C1).
- [ ] Confirm the complete stationary-tool inventory in TEB6.
- [ ] Confirm local PPE and dust-control requirements per tool (→ C2).
- [ ] Move the two CCOHS links into a proper Sources section (→ C3).
- [ ] Reviewer: PI/post-doc + training/sign-off owner.

### manual-tools.md — closest to ready
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Decide whether specific cutter ratings should be posted for common FAST cutters.
- [ ] Reviewer: PI/post-doc. Lowest-risk sign; likely the first to graduate.

### soldering-station.md
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Define FAST soldering-station setup and shutdown expectations.
- [ ] Add the manufacturer guidance / manual for the YIHUA 862BD+ station and replace the placeholder in Sources (→ C3).
- [ ] Reviewer: PI/post-doc + station owner.

## Printers

### printers-fff.md
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Confirm which printers are approved for ASA and flexible materials.
- [ ] Confirm the enclosed-printer + HEPA requirement for ABS/ASA is accurate (equipment-specific claim → needs owner confirmation or a source).
- [ ] Add a Sources section or a local-procedure reference for the material/enclosure rules (→ C3).
- [ ] Reviewer: PI/post-doc + printer/material owner.

### printers-resin.md
Current: `draft` v0.1, PI/post-doc **+ Alessia R. follow-up**, 2 pages.
- [ ] **Alessia R. review of the full sign** (resin printer owner) — primary blocker; there is an in-file review reminder comment.
- [ ] FAST approved solvent list and handling procedure (→ C1).
- [ ] Resin and solvent SDS documents on file.
- [ ] Western/UWO hazardous-waste and drain-disposal procedures for resin, solvents, wash liquid, wipes, gloves, supports, and failed prints (→ C1 + waste-disposal).
- [ ] Confirm the fleet statement (Prusa SL1S + CW1S) is current and the designated waste containers exist (→ C2).
- [ ] Reviewer: PI/post-doc + Alessia R.

## Safety & Storage

### safety-equipment-and-incidents.md
Current: `draft` v0.1, PI/post-doc, 2 pages.
- [ ] Confirm **all** listed safety-equipment locations before posting (eyewash, spill kit, shower, first aid, extinguisher, binder, emergency-contact signage) (→ C2).
- [ ] Confirm the exact incident-reporting route for FAST (→ C1).
- [ ] Confirm the fume-hood maximum-exhaust control wording and whether users should operate it (align with fumehood).
- [ ] Reviewer: PI/post-doc. This sign also documents the safety-binder location — tie to C4.

### general-storage.md — light
Current: `draft` v0.1, PI/post-doc, 1 page.
- [ ] Confirm final red-cabinet drawer assignments (→ C2).
- [ ] Decide whether to list specific shelves/cabinets after the lab layout stabilizes.
- [ ] Confirm no external source is required (housekeeping content — likely none).
- [ ] Reviewer: PI/post-doc.

## Electrical

### wiring.md
Current: `draft` v0.1, **Cameron B. / Dr. Pearce / qualified electrical reviewer**, 3 pages, has decision diagram + equations.
- [ ] **Qualified electrical reviewer** (Cameron B. or Dr. Pearce) must review the full sign before approval.
- [ ] Collect examples of approved wiring/enclosures from Cameron B. or Dr. Pearce.
- [ ] Confirm applicable equipment manuals, component datasheets, certification requirements, and local code/ESA requirements.
- [ ] Move the three Western/reference URLs into a proper Sources section; keep only genuine open questions under Reference Checks (→ C3).
- [ ] Reviewer: qualified electrical reviewer (highest bar in the set).
