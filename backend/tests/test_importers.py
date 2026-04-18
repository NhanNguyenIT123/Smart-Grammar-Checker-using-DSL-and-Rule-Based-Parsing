from __future__ import annotations

import sys
import unittest
from shutil import rmtree
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"
FIXTURES_DIR = PROJECT_ROOT / "backend" / "tests" / "fixtures" / "importers"
TMP_ROOT = PROJECT_ROOT / "backend" / "tests" / "tmp"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.preprocessing.importers import (  # noqa: E402
    import_cambridge_cefr_pack,
    import_collocation_pack,
    import_open_english_wordnet_pack,
    import_scowl_pack,
)


class ImporterTests(unittest.TestCase):
    def setUp(self) -> None:
        TMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.output_dir = TMP_ROOT / f"importers-{uuid4().hex}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        if self.output_dir.exists():
            rmtree(self.output_dir, ignore_errors=True)

    def test_scowl_importer_normalizes_word_list(self) -> None:
        payload = import_scowl_pack(FIXTURES_DIR / "scowl_sample.txt", output_dir=self.output_dir)

        self.assertEqual("src-scowl-imported", payload["metadata"]["id"])
        self.assertIn("apple", payload["dictionary_words"])
        self.assertIn("teacher", payload["dictionary_words"])
        self.assertNotIn("invalid-word-1", payload["dictionary_words"])
        self.assertTrue((self.output_dir / "scowl_pack.json").exists())

    def test_oewn_importer_builds_synonym_groups_and_semantic_classes(self) -> None:
        payload = import_open_english_wordnet_pack(FIXTURES_DIR / "oewn_sample.json", output_dir=self.output_dir)

        self.assertEqual("src-open-english-wordnet-imported", payload["metadata"]["id"])
        self.assertTrue(any("smart" in group for group in payload["synonym_groups"]))
        self.assertIn("vehicles", payload["semantic_classes"])
        self.assertIn("automobile", payload["dictionary_words"])
        self.assertTrue((self.output_dir / "oewn_pack.json").exists())

    def test_cambridge_importer_extracts_plain_text_terms(self) -> None:
        payload = import_cambridge_cefr_pack(
            FIXTURES_DIR / "cambridge_a2_sample.txt",
            level="A2",
            output_dir=self.output_dir,
        )

        self.assertEqual("src-cambridge-cefr-imported", payload["metadata"]["id"])
        self.assertIn("A2", payload["levels"])
        self.assertIn("able", payload["levels"]["A2"])
        self.assertIn("airport", payload["levels"]["A2"])
        self.assertIn("alright", payload["dictionary_words"])
        self.assertTrue((self.output_dir / "cambridge_cefr_pack.json").exists())

    def test_collocation_importer_builds_semantic_rule_pack(self) -> None:
        payload = import_collocation_pack(FIXTURES_DIR / "collocation_sample.csv", output_dir=self.output_dir)

        self.assertEqual("src-collocation-imported", payload["metadata"]["id"])
        phrases = {entry["phrase"]: entry["replacement"] for entry in payload["unlikely_phrases"]}
        self.assertEqual(3, len(payload["unlikely_phrases"]))
        self.assertEqual("do homework", phrases["make homework"])
        self.assertEqual("does homework", phrases["makes homework"])
        self.assertEqual("heavy rain", phrases["strong rain"])
        self.assertIn("heavy", payload["dictionary_words"])
        self.assertTrue((self.output_dir / "collocation_pack.json").exists())


if __name__ == "__main__":
    unittest.main()
