from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.preprocessing import compile_knowledge_base, load_pipeline_report  # noqa: E402
from grammar_dsl.preprocessing.compiler import _merge_imported_rulepacks  # noqa: E402


class PreprocessingCompilerTests(unittest.TestCase):
    def test_compile_knowledge_base_uses_raw_source_packs(self) -> None:
        knowledge_base = compile_knowledge_base(write_legacy=False)
        summary = knowledge_base["pipeline_summary"]

        self.assertEqual("3.0.0", summary["pipeline_version"])
        self.assertIn("load raw lexical packs from preprocessing/raw", summary["preprocessing_steps"])
        self.assertIn("compile exercise blueprints, lexical pools, and realization rules", summary["preprocessing_steps"])
        self.assertGreater(len(knowledge_base["source_manifest"]), 0)
        self.assertGreater(len(knowledge_base["semantic_classes"]), 0)
        self.assertGreater(len(knowledge_base["feature_catalog"]), 0)
        self.assertGreater(len(knowledge_base["exercise_blueprints"]), 0)
        self.assertGreater(summary["knowledge_stats"]["dictionary_entries"], 1000)
        self.assertGreaterEqual(summary["knowledge_stats"]["imported_sources"], 4)
        self.assertGreaterEqual(summary["knowledge_stats"]["cefr_entries"], 100)
        self.assertGreaterEqual(summary["knowledge_stats"]["imported_collocation_rules"], 160)
        self.assertGreaterEqual(summary["knowledge_stats"]["exercise_blueprints"], 10)
        self.assertGreaterEqual(summary["knowledge_stats"]["feature_atoms"], 10)
        self.assertIn("src-collocation-imported", [item["id"] for item in knowledge_base["source_manifest"]])
        self.assertIn("src-exercise-generator-pack", [item["id"] for item in knowledge_base["source_manifest"]])

    def test_pipeline_report_is_available_after_compile(self) -> None:
        compile_knowledge_base(write_legacy=False)
        report = load_pipeline_report()

        self.assertEqual("3.0.0", report["pipeline_version"])
        self.assertIn("knowledge_base.json", report["artifacts"])
        self.assertIn("exercise_blueprints.json", report["artifacts"])
        self.assertIn("feature_catalog.json", report["artifacts"])
        self.assertGreater(report["knowledge_stats"]["verb_entries"], 100)
        self.assertGreaterEqual(report["knowledge_stats"]["imported_sources"], 4)
        self.assertGreaterEqual(report["knowledge_stats"]["cefr_entries"], 100)
        self.assertGreaterEqual(report["knowledge_stats"]["imported_collocation_rules"], 160)
        self.assertGreaterEqual(report["knowledge_stats"]["exercise_blueprints"], 10)

    def test_merge_imported_rulepacks_appends_new_collocation_rules(self) -> None:
        grammar_rules = {
            "semantic_patterns": {
                "unlikely_phrases": [
                    {"phrase": "make homework", "message": "existing"}
                ]
            }
        }

        imported_rules = [
            {"phrase": "make homework", "message": "duplicate"},
            {"phrase": "strong rain", "message": "new", "replacement": "heavy rain"},
        ]

        from grammar_dsl.preprocessing import compiler as compiler_module

        original_rules = compiler_module.IMPORTED_UNLIKELY_PHRASES
        compiler_module.IMPORTED_UNLIKELY_PHRASES = imported_rules
        try:
            merged = _merge_imported_rulepacks(grammar_rules)
        finally:
            compiler_module.IMPORTED_UNLIKELY_PHRASES = original_rules

        merged_phrases = [item["phrase"] for item in merged["semantic_patterns"]["unlikely_phrases"]]
        self.assertEqual(["make homework", "strong rain"], merged_phrases)


if __name__ == "__main__":
    unittest.main()
