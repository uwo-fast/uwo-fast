# Lab Signs

This directory contains the documents printed out and posted in the FAST lab.

Use [AUTHORING.md](AUTHORING.md) when creating or revising signs. It defines the sign-writing process, reference rules, review expectations, and current draft template.

Current signs are drafts unless explicitly marked approved. Do not print or post a sign until its review owner has checked the content, required references are resolved, and local FAST procedures are confirmed.

When a sign is posted, update the FAST lab safety binder stored in the west-wall safety cabinet in TEB7.

## Current Signs

Public sign drafts:

- [Batteries and E-Waste](batteries-and-ewaste.md)
- [Broken Glass and Sharps](broken-glass-and-sharps.md)
- [Chemical and Materials Storage](chemical-and-materials-storage.md)
- [FFF Printers](printers-fff.md)
- [Fume Hood](fumehood.md)
- [General Storage](general-storage.md)
- [Manual Tools](manual-tools.md)
- [Power Tools](power-tools.md)
- [Resin Printers](printers-resin.md)
- [Safety Equipment and Incidents](safety-equipment-and-incidents.md)
- [Sink](sink.md)
- [Soldering Station](soldering-station.md)
- [Stationary Tools](stationary-tools.md)
- [Waste Disposal](waste-disposal.md)
- [Wiring](wiring.md)

Support documents:

- [Authoring Guide](AUTHORING.md)
- [Universal Notice Partial](_UNIVERSAL_NOTICE.md)

## Build PDFs

Local one-time setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
fnm use
npm install
```

Build all signs:

```bash
source .venv/bin/activate
fnm use
python scripts/build_lab_signs.py --all
```

Build selected signs:

```bash
source .venv/bin/activate
fnm use
python scripts/build_lab_signs.py lab-signs/sink.md lab-signs/wiring.md
```

Generated PDFs are written to `output/lab-signs/`. Intermediate files and logs are written to `artifacts/lab-signs/`. Both directories are ignored by Git.
