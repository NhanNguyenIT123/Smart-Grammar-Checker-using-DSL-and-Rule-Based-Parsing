# Open English WordNet Vendor Drop

Place an exported Open English WordNet file here.

Supported scaffold formats:
- `.json` with `synonym_groups`, `semantic_classes`, or `entries`
- `.csv` / `.tsv` with columns such as `lemma`, `synonyms`, and optional `semantic_class`

Import command:

```powershell
python backend/run.py import-oewn --input backend/src/grammar_dsl/preprocessing/raw/vendors/oewn/oewn_export.json
```
