# Cambridge CEFR Vendor Drop

Place Cambridge CEFR-aligned vocabulary exports here.

Supported scaffold formats:
- `.json` with a `levels` map
- `.csv` / `.tsv` with `term` and `level` columns
- plain text extracted from a PDF, together with `--level`

Import examples:

```powershell
python backend/run.py import-cefr --input backend/src/grammar_dsl/preprocessing/raw/vendors/cambridge_cefr/a2_terms.txt --level A2
python backend/run.py import-cefr --input backend/src/grammar_dsl/preprocessing/raw/vendors/cambridge_cefr/b1_terms.csv
```
