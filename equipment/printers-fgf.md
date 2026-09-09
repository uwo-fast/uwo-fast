---
title: "FGF Printer"
slug: "printers-fgf"
version: "0.1"
status: "draft"
record_owner: "PI / post-doc"
equipment: "GreenBoy3D Pellet Extruder V1 on an Original Prusa i3 MK3S, with FAST bulk pellet feed"
---

# FGF Printer — Equipment Record

Reference record for the FAST pellet printer, built in-house by converting a Prusa MK3S
to granulate feedstock. This is a binder and reference document, not a posted sign. The
wall sign is [FGF Printers](../lab-signs/printers-fgf.md).

Provenance is separated on purpose. Vendor specifications describe what the extruder was
sold as; the deviations and measurements below describe what this machine actually is.
Nearly every operating value in use here is self-derived, because GreenBoy3D ships no
firmware and effectively no technical documentation.

## What it is

> A gravity-fed auger toolhead on a desktop FFF frame. A planetary-geared stepper turns a
> screw inside a heated barrel, melting plastic pellets and pushing them out an M6 nozzle.
> It replaces the MK3S stock hotend and extruder entirely. There is no pneumatic feed:
> pellets fall from a hopper into the head.

Feedstock is virgin pellets and shredded regrind produced in-house, which is what makes
this machine part of the FAST recycling chain rather than just another printer.

It is the sixth MK3S chassis in the lab and the fourth fitted with an enclosure and HEPA
filtration. It is not one of the five printers the [FFF Printers](../lab-signs/printers-fff.md)
sign covers; those remain five machines, three of them enclosed.

Approved polymers: **PLA and PETG**.

## FAST project repositories

The engineering behind this machine lives in two repositories, both public:

- **[`uwo-fast/gb3dpe-pellet-system`](https://github.com/uwo-fast/gb3dpe-pellet-system)** —
  bulk pellet feed system, mounts, and operating docs. Parametric OpenSCAD, geometry
  regression-tested against a committed baseline.
- **[`uwo-fast/Prusa-Firmware-GB3DPE`](https://github.com/uwo-fast/Prusa-Firmware-GB3DPE)** —
  Prusa firmware fork carrying the GB3DPE configuration. Changes are tagged
  `!!!CHANGED:`; `GB3DPE_TUNING.md` holds the calibration log.

## Vendor specifications — GreenBoy3D Pellet Extruder V1

From the vendor shop page. These describe the product, not this installation.

| Parameter       | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| System voltage  | 24 V                                                         |
| Heat cartridge  | 70 W, 24 V                                                   |
| Fans            | 2                                                            |
| Drive           | planetary-geared stepper, ratio not published                |
| Max hotend temp | 330 °C stock; ~300 °C with PLA-printed parts; 420 °C upgraded |
| Max ambient     | 80 °C                                                        |
| Nozzle          | M6 thread, 0.4-2.5 mm                                        |
| Flow rate       | 125-200 g/h at a 1 mm nozzle                                 |
| Pellet size     | 0.3-5 mm                                                     |
| Retraction      | mechanical, by reversing the screw; no firmware values        |
| Net weight      | ~700 g                                                       |

The vendor wiki's `Marlin Firmware Setup`, `Klipper Firmware Setup`, all six
`Pellet 3D Printing Basics` pages and the `Recycling` pages are "Coming Soon" stubs. The
product page omits the gearbox ratio and any e-steps figure.

## Deviations on this unit

- **Printed parts are ABS.** The vendor's ~300 C ceiling applies to units with PLA-printed
  parts fitted. This unit uses ABS, so the stock 330 C rating applies.
- **Fans replaced.** The kit ships two 24 V 2-pin blowers that the Einsy board cannot
  power. Both were swapped for 5 V units sourced separately.
- **PINDA bracket replaced.** The vendor proximity-sensor adapters put the probe outside
  the MK3S X and Y travel limits. A replacement returns the probe near its original
  position.
- **Firmware is a fork, not stock.** `MK3.h` and `MK3S.h` carry modified probe offsets
  (X 2.3 / Y 0.86 mm), E-axis steps of 1187 at 1/32 microstepping (volumetrically
  calibrated), a changed thermistor table, and changed travel limits.
- **Bulk feed added.** A roof-mounted hopper on the printer enclosure gravity-feeds the
  toolhead through the supplied conveyor tube. The stock hopper is a 43 x 40 x 45 mm cup
  holding 20-30 g, which at the quoted flow rate empties in well under an hour.

## Feedstock — measured in-house

| Regrind          |                                               |
| ---------------- | --------------------------------------------- |
| Material         | Polymaker PolyLite PLA, black                 |
| Form             | shredded in-house, sieved to 3 mm             |
| Method           | gently settled in a beaker to the 700 mL line |
| Mass             | 342 g                                         |
| **Bulk density** | **0.489 kg/L**                                |

Virgin pellet density is still the general-practice 0.62 kg/L and has not been measured
here. Bulk density and particle size are properties of the shred rather than the polymer:
they depend on the shredder, its screen, and how the material settles.

## Safety-relevant consequences

Collected here because they are what the wall sign is built from.

- **The barrel runs far hotter than an FFF hotend for the same polymer**, and holds much
  more heat. PLA on an MK3S runs around 215 °C; this head is rated to 330 °C.
- **Feedstock must be within 0.3-5 mm.** In-house shred is sieved to 3 mm. Oversize
  material bridges and jams the auger.
- **Stock firmware must never be flashed onto this printer.** Probe offsets, E-steps,
  thermistor table and travel limits are all changed; stock firmware would drive the head
  into the bed and misread temperature.
- **Throughput is 125-200 g/h**, an order of magnitude above a filament hotend, so
  emissions and purge volumes scale accordingly.
- **The toolhead weighs ~700 g**, well above the stock extruder, which changes the
  machine's behaviour on a crash.
- **Recycled feedstock has a finite life.** Published work puts single-source PLA at about
  three melt cycles and mixed-source shred at about two before properties fall off, with
  molecular weight down up to 40% by six. FAST had no cycle tracking before this record;
  the convention adopted is that the feedstock container label carries the polymer and the
  cycle number, incremented on each shred-and-refill. No separate log.

## To Be Recorded From This Installation

- [ ] Printer asset ID
- [ ] Configured hotend and bed temperature per polymer
- [ ] Installed nozzle diameter
- [ ] Measured virgin pellet bulk density, if virgin becomes the main feedstock
- [ ] As-built deviations of the bulk hopper from the committed CAD

## Sources

- GreenBoy3D homepage: <https://greenboy3d.de/>
- GreenBoy3D shop, Pellet Extruder V1:
  <https://shop.greenboy3d.de/products/greenboy3d-pellet-extruder-v1>
- GreenBoy3D wiki: <https://wiki.greenboy3d.de/>
- FAST pellet system repository: <https://github.com/uwo-fast/gb3dpe-pellet-system>
- FAST firmware fork: <https://github.com/uwo-fast/Prusa-Firmware-GB3DPE>
- EPA, particle and VOC emissions from a 3D printer filament extruder:
  <https://cfpub.epa.gov/si/si_public_record_Report.cfm?Lab=CPHEA&dirEntryId=348894>

## Reference Checks Needed

- The `gb3dpe-pellet-system` README states the bulk hopper is "designed, not yet printed".
  It has since been printed and is in service. Filed upstream as
  <https://github.com/uwo-fast/gb3dpe-pellet-system/issues/2>; do not cite that README as
  current until it is closed.
- Drying temperatures on the sign (PLA 45 °C for 4-6 h, PETG 60 °C for 6 h) are general
  practice and are **not** attributable to Polymaker. Its PolyDryer blog post says
  "a lower temp (around 65-70 °C) is fine for common filaments like PLA and PETG",
  which is above the glass transition of standard PLA and contradicts the same page's
  description of its own hardware running 40-55 °C. It is marketing copy, not a data
  sheet. The figures posted are deliberately more conservative because FAST dries loose
  shred rather than spooled filament, and shred above its softening point sinters into
  a solid lump. Get the PolyLite PLA and PETG technical data sheets for a real source;
  Alessia R. to review either way.
- Reprocessing limits on the sign are published figures, not FAST measurements.
- Vendor specifications above were taken from the project repository's compiled reference
  rather than read from the vendor page directly. Confirm before relying on them.
- Confirm the items under "To Be Recorded From This Installation".
