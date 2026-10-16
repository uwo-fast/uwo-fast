# Lab Signs — Outstanding Work

What is left before each sign reaches **v1 / `approved`**. Completed work is not tracked
here; the git history has it.

Last reviewed: 2026-10-07. See [AUTHORING.md](AUTHORING.md) for the review process,
reference rules, and approval blockers this list is built from.

Every sign is `status: review` at v0.1. Open questions are tracked here, not on the
signs. `just pages` gives page counts.

## The current plan: post at `review`, iterate

Signs are printed and posted provisionally so the lab can start using them, with
corrections pen-marked and reprinted over time. That is a lower bar than v1: an item
blocks printing only if a person following the sign could be hurt or misdirected.

## Blocking the first printing

Nothing.

## For Dr. Pearce

- [ ] **Bases share the flammables cabinet.** Western states bases are "incompatible with
      acids, flammables and oxidizers and should be stored on their own". The current
      arrangement is a knowing trade-off against putting bases in a non-rated cabinet. No
      sign text was changed; this is the PI's call.
- [ ] **The glove rule** on power tools, resolved from CCOHS, to confirm.
- [ ] **The FAST phone number label.** 519-661-2111 ext. 86725 reads "FAST lab" on the
      safety sign. The PI's office, or a general line?
- [ ] **chemical-and-materials-storage, special-hazard rows.** The peroxide-former,
      water-reactive and pyrophoric rows read as Western's general list. Keep only the
      categories the lab actually holds. Also confirm "inorganic salts and ordinary organic
      liquids and solids may be stored together", which as written also covers flammables.

## Local write-ups

- [ ] **soldering-station** — write down the FAST setup and shutdown expectations.
- [ ] **soldering-station** — photograph or scan the YIHUA 862BD+ paper manual into
      `equipment/soldering-station.md`. No manufacturer-hosted copy exists online, so the
      paper copy is the only source.
- [ ] **general-storage** — confirm glassware, strainers and funnels still live in the red
      standing cabinet bottom drawer.
- [ ] **waste-disposal / printers-fgf** — confirm the purge split: FFF purge lines go to
      garbage, FGF purge of a known polymer goes to polymer recycling.
- [ ] **power-tools** — list the grinder, saw, sander and driver models actually held, so
      their manuals can be gathered.

## Waiting on someone else

- [ ] **printers-resin** — Alessia R.'s review of the whole sign. AUTHORING says this
      happens *after* initial posting, so it does not hold up the print run.
- [ ] **printers-resin** — resin and solvent SDS on file.
- [ ] **printers-resin** — the hazardous-waste route for resin, wash liquid, wipes and
      failed prints, beyond what Western's handbook already covers.
- [ ] **chemical-and-materials-storage** — collect the SDS for each category actually held in the lab.
- [ ] **sink** — where contaminated rinsate goes. Western's handbook covers rinsing empty
      containers (2.5) but not the rinsate itself.
- [ ] **wiring** — examples of approved wiring and enclosures from Cameron B. or
      Dr. Pearce.
- [ ] **wiring** — the applicable equipment manuals, component datasheets, certification
      requirements and local code / ESA requirements.
- [ ] **stationary-tools** — local PPE and dust-control requirements per tool.
- [ ] **printers-fgf** — a readable source for the drying figures. Polymaker blocks
      automated access, so the PolyLite PLA and PETG technical data sheets have to be
      pulled by hand; the sign labels the numbers general practice until then. Alessia R.
      to review these and the reprocessing limits.

## Cross-Cutting Blockers

### C1. Name the remaining FAST procedures

The Western-published half is done and the signs cite real documents. Two local
procedures are still unwritten, and each is the reason a sign above is blocked:

- [ ] **FAST waste-disposal procedure** — oils, greases, lubricants, resins, solvents,
      acids, bases, and where rinsate goes. Blocks `waste-disposal` and `sink`.
- [ ] **FAST resin handling procedure** — approved solvent list, wash/cure workflow,
      waste routing. Blocks `printers-resin`.

### C2. Safety-binder process

- [ ] Confirm the FAST lab safety binder index exists and define the step for adding or
      updating a sign there. Every sign's approval depends on it.

## Deferred, not blocking

Measurements are recorded so they are not repeated.

- [ ] **Flowcharts.** Removed from `waste-disposal`, `chemical-and-materials-storage` and
      `wiring` for the first printing: their text printed far smaller than body copy, and
      each repeated a table or bullet list on the same sign. Two dead ends are ruled out.
      `flowchart LR` fits but shrinks the text further. Raising the mermaid font size is
      self-defeating, because the image is height-capped at `0.62\textheight` and grows
      faster than the text does:

          wiring  784x1090 @ ~16px font  ->  text 1.97 mm on the page
          wiring 1862x3618 @  28px font  ->  text 1.04 mm on the page

      Bring one back only as a shallower diagram, with fewer decision levels.
- [ ] **Orphan headings.** A heading or a short table can be stranded at a page break.
      Measured on 2026-10-15 against the signs as they are now:
      `\usepackage[nobottomtitles*]{titlesec}` costs four signs a page (printers-fff,
      safety-equipment-and-incidents, stationary-tools, waste-disposal);
      `\needspace{5\baselineskip}` before every `##` heading costs
      safety-equipment-and-incidents a page, its code strip alone moving to page 2, and
      does not keep a table with its heading. Fixed case by case instead: the fume hood's
      utility table follows Ask First, waste-disposal's Do Not Guess comes before Special
      Streams, and chemical storage reserves space before Chemical Inventory. A reserve
      placed after a table pushed that table's repeated header onto the next page alone.
- [ ] **`chemical-and-materials-storage` and `wiring` page 2 holds little more than the
      code strip and a section.** The strip cannot split. Merging duplicate bullets was not enough, and
      neither was 16 mm codes in place of 20 mm.
- [ ] **`safety-equipment` strip sits tight against the footer rule.** Not overlapping,
      but the least margin in the set.
- [ ] **Normalise source labels.** Some signs say "Lab Safety Manual", others "Western
      Laboratory Health and Safety Manual".
- [ ] **Immediate site rebuilds.** <https://uwo-fast.github.io> rebuilds daily and accepts
      a `repository_dispatch` of type `signs-updated`, but nothing sends one. A token with
      access to the site repo would let this repo push a rebuild the moment it publishes,
      rather than the codes on the wall trailing by up to a day.

## Definition of v1

The bar each sign must clear before `status: approved` / `version: "1.0"`:

1. Every item listed for that sign in this file is resolved.
2. Every disposal / storage / emergency / PPE / electrical / equipment instruction has a
   cited source **or** a named local FAST procedure.
3. No reference to an "approved procedure" that is not actually identified.
4. The required review owner has checked the final text.
5. The required subject-matter owner has reviewed it.
6. Nothing can be read as authorizing untrained users to do hazardous work.
7. The sign is entered in the FAST lab safety binder process.
8. Front matter bumped: `status: approved`, `version: "1.0"`.
