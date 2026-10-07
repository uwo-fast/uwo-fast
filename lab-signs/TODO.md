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

- [ ] **Diagram legibility.** The flowcharts on `waste-disposal`, `chemical` and `wiring`
      print with text far smaller than body copy. Two dead ends are already ruled out.
      `flowchart LR` fits but shrinks the text further. Raising the mermaid font size is
      self-defeating, because the image is height-capped at `0.62\textheight` and grows
      faster than the text does:

          wiring  784x1090 @ ~16px font  ->  text 1.97 mm on the page
          wiring 1862x3618 @  28px font  ->  text 1.04 mm on the page

      The only levers left are a shallower diagram — fewer decision levels — or more page
      height for it. Both change the sign, not a config value.
- [ ] **Orphan headings.** A section heading can be stranded at the foot of a page with
      its content overleaf, as "Common Waste Streams" is on `waste-disposal` page 1.
      `\usepackage[nobottomtitles*]{titlesec}` fixes it in one line, but it was measured
      at **two signs gaining a page**, so it is off. Turn it on if that becomes an
      acceptable trade.
- [ ] **`chemical-and-materials-storage` diagram and table disagree.** The table gained
      peroxide formers, water-reactives, pyrophorics and shock-sensitives; the flowchart still ends at
      "Check SDS and ask before storing". Defensible, since that branch covers them
      implicitly, but the two no longer say the same thing.
- [ ] **`safety-equipment` strip sits tight against the footer rule.** Not overlapping,
      but the least margin in the set.
- [ ] **Unicode font in the template.** `templates/lab-sign.tex` has no Unicode font, so
      lualatex silently dropped characters like `°` and `±`. The build now fails loudly
      instead, but a sign still cannot print a degree sign. `fontspec` did not load Latin
      Modern locally. CI's PDFs embed Latin Modern OpenType fonts, so the problem may be
      local only: build a sign containing `°` in CI with the check off before relaxing it.
- [ ] **Normalise source labels.** Some signs say "Lab Safety Manual", others "Western
      Laboratory Health and Safety Manual".
- [ ] **Immediate site rebuilds.** <https://uwo-fast.github.io> rebuilds daily and accepts
      a `repository_dispatch` of type `signs-updated`, but nothing sends one. A token with
      access to the site repo would let this repo push a rebuild the moment it publishes,
      rather than the codes on the wall trailing by up to a day.
- **`waste-disposal` stays at 3 pages.** Not fixable by trimming — reclaiming 200pt still
  leaves three, because the flowchart is atomic and dictates the page breaks. Page 3
  carries real references, not a stub. Closes only via the diagram work above.

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
