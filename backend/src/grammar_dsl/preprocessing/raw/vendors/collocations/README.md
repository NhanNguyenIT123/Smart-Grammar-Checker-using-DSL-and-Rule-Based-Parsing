# Collocation Vendor Drop

Place a curated collocation export here before importing it.

Supported scaffold formats:
- `.json` with `entries` or `unlikely_phrases`
- `.csv` / `.tsv` with columns like `incorrect_phrase`, `preferred_phrase`, and optional `message`
- plain text using `incorrect | preferred | optional message`

Import examples:

```powershell
python backend/run.py import-collocations --input backend/src/grammar_dsl/preprocessing/raw/vendors/collocations/collocations.csv
python scripts/import_collocations.py --input backend/src/grammar_dsl/preprocessing/raw/vendors/collocations/collocations.csv
```
