# Imported Packs

This folder stores normalized packs produced by the importer scripts.

Typical flow:
- put the original vendor file in `raw/vendors/...`
- run an importer such as `python backend/run.py import-scowl --input <path>`
- inspect the normalized JSON written here
- run `python backend/run.py compile`

Generated files may include:
- `scowl_pack.json`
- `oewn_pack.json`
- `cambridge_cefr_pack.json`
- `collocation_pack.json`
