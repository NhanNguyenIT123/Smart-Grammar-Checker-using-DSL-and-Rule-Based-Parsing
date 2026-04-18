# Vendor Drop Zone

Place original external files here before running an importer.

Recommended layout:
- `vendors/scowl/`
- `vendors/oewn/`
- `vendors/cambridge_cefr/`
- `vendors/collocations/`

These files should stay as close to the downloaded originals as possible.
Do not edit them into runtime-ready form by hand.
The importer scripts are responsible for normalizing them into `raw/imported/`.

Also review:
- `vendors/vendor_manifest.json`
- `vendors/LICENSE_NOTES.md`
