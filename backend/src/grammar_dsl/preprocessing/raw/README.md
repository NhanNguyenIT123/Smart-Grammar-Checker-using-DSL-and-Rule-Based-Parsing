# Raw Source Packs

This folder stores the human-curated source packs that feed the preprocessing pipeline.

Flow:
- edit the curated raw packs in this directory
- optionally drop vendor files into `vendors/`
- optionally run an importer to emit normalized packs into `imported/`
- run `python backend/run.py compile`
- use the compiled artifacts in `backend/src/grammar_dsl/data/compiled`

Current raw packs:
- `pipeline_config.json`: pipeline version and preprocessing stages
- `source_manifest.json`: high-level description of bundled sources
- `verbs_seed.json`: irregular seeds, regular seeds, and doubling exceptions
- `synonym_groups.json`: synonym clusters before graph compilation
- `project_words.json`: project-specific vocabulary kept in the dictionary
- `semantic_classes.json`: place, food, drink, document, and vehicle classes
- `vendors/`: original external source drops, manifest, and license notes
- `imported/`: normalized packs emitted by importer scripts

Recommended rule for future expansion:
- keep raw sources small, explainable, and citeable
- add new external sources here in raw form first, then normalize them in the compiler
