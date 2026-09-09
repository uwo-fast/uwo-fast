# Equipment Records

Reference records for FAST lab equipment: nameplate data, model and manufacturer
specifications, operating limits, certification status, and service details.

These are binder and reference documents. They are not printed and posted. For the short
wall reminders people read at the point of work, see [lab-signs](../lab-signs/README.md).

## Current Records

- [Fume Hood](fumehood.md)
- [FGF Printer](printers-fgf.md)

## What Belongs Here

An equipment record, rather than a sign, when the content is:

- Nameplate, model, serial and manufacture data.
- Manufacturer specifications, drawings, and performance tables.
- Certification and inspection history, and what is due when.
- Facilities details: circuits, disconnects, exhaust identifiers, service contacts.
- Anything too long or too static to be useful on a wall.

Keep it out of `lab-signs/`. The sign build globs `lab-signs/*.md` and renders every file
it finds as a printed sign, so a record placed there ends up in the combined PDF.

## Linking

Records link to the corresponding sign. Signs do not link back: a sign is printed and
posted, and a Markdown link on a wall does nothing. If a posted sign needs to reach a
longer document, that is a QR code, per the sign
[authoring guide](../lab-signs/AUTHORING.md).

Where a record and a sign cover the same equipment, give them the same slug, as
`equipment/fumehood.md` and `lab-signs/fumehood.md` do.

## Front Matter

Records carry front matter parallel to the signs:

```yaml
---
title: "Fume Hood"
slug: "fumehood"
version: "0.1"
status: "draft"
record_owner: "PI / post-doc"
equipment: "Mott Pro Bench vertical-sash chemical fume hood, model 7321000"
---
```

`status` uses the same states as the signs: `notes`, `draft`, `review`, `approved`,
`retired`. Nothing here is built, so the front matter is documentation rather than build
input.

## Provenance

Separate what was read off the installed unit from what came out of a manufacturer
catalog. A model number establishes what the equipment was designed to do. It does not
establish what the installed unit currently does, and catalog performance figures are not
a substitute for a certification record.

Keep the unrecorded as-installed values visible as an unchecked list in the record rather
than dropping them, and use a `Reference Checks Needed` section for claims that still need
verifying against a primary source.
