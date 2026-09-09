---
title: "FGF Printers"
slug: "printers-fgf"
version: "0.1"
status: "review"
review_owner: "PI / post-doc"
include_universal_notice: true
---

# Fused Granulate Fabrication (FGF) Printers

## Trained Users Only

- This is a GreenBoy3D pellet extruder on a converted Prusa MK3S. It takes granulate
  feedstock instead of filament and is a specialty machine, not a shared printer.
- STOP. Do not use an FGF printer without express permission and training from a post-doc
  or Dr. Pearce.
- Training covers the extruder, the feedstock rules, purging, and the waste route. Being
  trained on the FFF printers does not carry over.
- NEVER flash stock Prusa firmware onto this printer. It runs a fork with changed probe
  offsets, E-steps, thermistor table and travel limits. Stock firmware drives the head
  into the bed and misreads temperature.

## Feedstock

| Feedstock | Use | Notes |
| --- | --- | --- |
| Virgin pellets, PLA or PETG | Yes | The reference case. Confirm the material is dry. |
| FAST recycled shred, PLA or PETG, known history | Yes, within the reprocessing limit | Check the container label. See below. |
| Any polymer other than PLA or PETG | NEVER | This printer is set up for PLA and PETG only currently. Ask first. |
| Unknown polymer, mixed polymer, or unlabelled container | NEVER | Unknown melt behaviour and unknown fumes. Ask. |
| Anything with metal, grit, labels, adhesive, or dirt in it | NEVER | Wrecks the auger and barrel. Re-sort or discard it. |
| Anything outside 0.3 to 5 mm | NEVER | Oversize bridges and jams the auger. In-house shred is sieved to 3 mm. |

- Keep feedstock containers closed and labelled with polymer and cycle count.
- Wet feedstock prints badly and can spit. Dry it if it has been open to room air.
- General practice: PLA at 45 C for 4 to 6 hours, PETG at 60 C for 6 hours. Do not dry
  PLA hotter. It softens near 60 C and loose shred will fuse into a solid lump.

## Reprocessing Limit

Every melt shortens the polymer chains, so recycled stock is not indefinitely reusable.
**A cycle is one trip through a melt.** Virgin pellets printed once are cycle 1; shred
from those prints, printed again, is cycle 2.

- **The container label is the log.** Write the polymer and the cycle number on every
  feedstock container, and increment it when a batch is shredded and refilled.
- Single-source PLA or PETG: up to **3 cycles**.
- Mixed-source shred: up to **2 cycles**.
- Past that, or if the label is missing or the count unknown, treat the batch as
  non-structural only, or ask before using it at all.
- Published work reports molecular weight down by up to 40% after six cycles.

## Before You Print

- Check the hopper is clear and holds the feedstock you expect. Do not mix polymers in a
  hopper.
- Confirm the previous user purged the barrel, or purge it yourself before starting.
- Check the nozzle, barrel, and heater wiring look undamaged.
- Have a metal tray or container ready for purge material.
- Check the bulk hopper has enough feedstock for the print, and that its feed tube is
  clear.
- Check the enclosure door closes and the HEPA fan runs.

## While Printing

- The barrel is rated to 330 C and holds far more heat than an FFF hotend, which prints
  the same PLA near 215 C. Treat every metal part of the extruder as hot.
- NEVER put fingers or tools into the hopper or feed throat while the printer is powered.
  Clear blockages only when the machine is off and you have been trained to do it.
- Purge material comes out hot and in quantity. NEVER let it land on your hand or the
  floor. Aim it into a tray; the bed works but makes more cleanup.
- Stop the print if the extruder grinds, stalls, runs empty, smokes, or smells wrong.
- Do not restart the same failing job without finding the cause. A repeated jam damages
  the auger and barrel.

## Spills And Housekeeping

- Pellets and shred on the floor are a slip hazard. Sweep up spills immediately, do not
  leave them for later.
- Keep feedstock off the floor and off walkways.
- Do not return floor-swept material to a feedstock container. It is contaminated.

## Ventilation And Emissions

- Ground and pulverized material emits more ultrafine particles than virgin pellets, and
  this machine pushes 125 to 200 g/h, an order of magnitude above a filament hotend.
- Run with the enclosure door closed and the HEPA filter fan on. This machine is enclosed
  and filtered; use it that way.
- Ask before running any polymer other than PLA or PETG.

## Waste And Cleanup

- Purge, failed prints, and clean single-polymer offcuts go back to FAST polymer recycling
  if the polymer is known. See the Waste Disposal sign.
- Contaminated, mixed, or unknown material does not go into polymer recycling.
- Leave the printer, hopper area, and bench clean and clear for the next user.
- Report printer problems rather than leaving them for the next user.

## Sources / Procedure Links

- GreenBoy3D pellet extruder: <https://greenboy3d.de/>
- FAST pellet system and operating docs: <https://github.com/uwo-fast/gb3dpe-pellet-system>
- EPA, particle and VOC emissions from a 3D printer filament extruder:
  <https://cfpub.epa.gov/si/si_public_record_Report.cfm?Lab=CPHEA&dirEntryId=348894>
- Reprocessing limits, Hidalgo-Carvajal et al., Polymers 2023:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10490016/>
