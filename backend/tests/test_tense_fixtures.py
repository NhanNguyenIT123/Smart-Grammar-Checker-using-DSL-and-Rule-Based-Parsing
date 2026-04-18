from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"
FIXTURES_DIR = PROJECT_ROOT / "backend" / "tests" / "fixtures"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.services import CommandService  # noqa: E402


class TenseFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.service = CommandService()
        with (FIXTURES_DIR / "tense_cases.json").open("r", encoding="utf-8") as file:
            cls.tense_cases = json.load(file)
        with (FIXTURES_DIR / "paragraph_cases.json").open("r", encoding="utf-8") as file:
            cls.paragraph_cases = json.load(file)

    def test_full_tense_detection_matrix(self) -> None:
        for case in self.tense_cases:
            with self.subTest(case=case["name"]):
                response = self.service.execute(case["command"])
                self.assertTrue(response.success)
                detected = {item["name"] for item in response.data["detected_tenses"]}
                self.assertIn(case["expected_detected"], detected)
                self.assertEqual(case["expected_spelling_count"], len(response.data["spelling_issues"]))
                self.assertEqual(case["expected_grammar_count"], len(response.data["grammar_issues"]))

    def test_long_paragraph_regression_pack(self) -> None:
        for case in self.paragraph_cases:
            with self.subTest(case=case["name"]):
                response = self.service.execute(case["command"])
                self.assertTrue(response.success)

                spelling = {item["suggestion"] for item in response.data["spelling_issues"]}
                grammar_categories = {item["category"] for item in response.data["grammar_errors"]}
                semantic_categories = {item["category"] for item in response.data["semantic_warnings"]}
                detected = {item["name"] for item in response.data["detected_tenses"]}

                self.assertEqual(case["expected_sentence_count"], response.data["sentence_count"])
                self.assertEqual(len(case["expected_spelling"]), len(response.data["spelling_issues"]))
                self.assertEqual(
                    len(case["expected_grammar_categories"]) == 0,
                    len(response.data["grammar_errors"]) == 0,
                )
                self.assertEqual(
                    len(case["expected_semantic_categories"]) == 0,
                    len(response.data["semantic_warnings"]) == 0,
                )

                for expected_spelling in case["expected_spelling"]:
                    self.assertIn(expected_spelling, spelling)

                for expected_category in case["expected_grammar_categories"]:
                    self.assertIn(expected_category, grammar_categories)

                for expected_category in case["expected_semantic_categories"]:
                    self.assertIn(expected_category, semantic_categories)

                for expected_tense in case["expected_detected"]:
                    self.assertIn(expected_tense, detected)

                for expected_snippet in case["expected_corrected_contains"]:
                    self.assertIn(expected_snippet, response.data["corrected_text"])


if __name__ == "__main__":
    unittest.main()
