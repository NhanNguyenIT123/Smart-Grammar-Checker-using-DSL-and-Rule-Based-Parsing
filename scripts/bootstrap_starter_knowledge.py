from __future__ import annotations

import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

for candidate in (str(PROJECT_ROOT), str(BACKEND_SRC)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

from grammar_dsl.preprocessing.importers import (
    import_cambridge_cefr_pack,
    import_collocation_pack,
    import_open_english_wordnet_pack,
    import_scowl_pack,
)

VENDORS_DIR = PROJECT_ROOT / "backend" / "src" / "grammar_dsl" / "preprocessing" / "raw" / "vendors"


def bootstrap_starter_knowledge() -> dict[str, object]:
    imports = [
        import_scowl_pack(VENDORS_DIR / "scowl" / "scowl_starter.txt"),
        import_open_english_wordnet_pack(VENDORS_DIR / "oewn" / "oewn_starter.json"),
        import_cambridge_cefr_pack(VENDORS_DIR / "cambridge_cefr" / "cambridge_a2_b1_starter.json"),
        import_collocation_pack(VENDORS_DIR / "collocations" / "collocations_starter.csv"),
    ]
    from grammar_dsl.preprocessing import compiler as compiler_module
    from grammar_dsl.preprocessing import source_packs as source_packs_module

    importlib.reload(source_packs_module)
    compiler_module = importlib.reload(compiler_module)
    knowledge_base = compiler_module.compile_knowledge_base(write_legacy=True)
    return {
        "imported_sources": [payload["metadata"] for payload in imports],
        "pipeline_summary": knowledge_base["pipeline_summary"],
    }


if __name__ == "__main__":
    result = bootstrap_starter_knowledge()
    imported = len(result["imported_sources"])
    summary = result["pipeline_summary"]
    print(
        f'Starter knowledge batch imported ({imported} packs) and compiled to '
        f'pipeline v{summary["pipeline_version"]}.'
    )
