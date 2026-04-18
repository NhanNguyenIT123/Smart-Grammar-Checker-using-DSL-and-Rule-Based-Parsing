from __future__ import annotations

import sys
import tempfile
import unittest
from uuid import uuid4
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.personalization import UserProfileStore  # noqa: E402
from grammar_dsl.services import CommandService  # noqa: E402


class CommandServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.service = CommandService()

    def create_isolated_service(self) -> tuple[CommandService, Path]:
        db_path = Path(tempfile.gettempdir()) / f"grammardsl-test-{uuid4().hex}.sqlite3"
        return CommandService(profile_store=UserProfileStore(db_path)), db_path

    def test_help_command(self) -> None:
        response = self.service.execute("help")
        self.assertTrue(response.success)
        self.assertEqual(response.command, "help")
        self.assertEqual(len(response.data["commands"]), 9)
        self.assertGreater(len(response.data["coverage_matrix"]), 0)
        self.assertIn("pipeline_summary", response.data)
        self.assertIn("knowledge_stats", response.data["pipeline_summary"])
        self.assertGreaterEqual(response.data["pipeline_summary"]["knowledge_stats"]["imported_sources"], 4)
        self.assertGreaterEqual(response.data["pipeline_summary"]["knowledge_stats"]["cefr_entries"], 100)
        self.assertGreaterEqual(response.data["pipeline_summary"]["knowledge_stats"]["imported_collocation_rules"], 160)
        usages = [item["usage"] for item in response.data["commands"]]
        self.assertFalse(any("why" in usage for usage in usages))
        self.assertIn("revision plan", usages)
        self.assertIn("history", usages)
        self.assertIn("reset history", usages)

    def test_spell_command_for_correct_word(self) -> None:
        response = self.service.execute("spell generate")
        self.assertTrue(response.success)
        self.assertTrue(response.data["is_correct"])
        self.assertEqual(response.data["closest_match"], "generate")

    def test_spell_command_for_incorrect_word(self) -> None:
        response = self.service.execute("spell generte")
        self.assertTrue(response.success)
        self.assertFalse(response.data["is_correct"])
        self.assertEqual(response.data["closest_match"], "generate")

    def test_verb_lookup(self) -> None:
        response = self.service.execute("verb know")
        self.assertTrue(response.success)
        self.assertEqual(response.data["formatted"], "know - knew - known")

    def test_common_verb_lookup_get(self) -> None:
        response = self.service.execute("verb get")
        self.assertTrue(response.success)
        self.assertEqual(response.data["formatted"], "get - got - gotten")

    def test_regular_verb_generation_quality(self) -> None:
        answer = self.service.execute("verb answer")
        visit = self.service.execute("verb visit")
        prefer = self.service.execute("verb prefer")

        self.assertEqual(answer.data["formatted"], "answer - answered - answered")
        self.assertEqual(visit.data["formatted"], "visit - visited - visited")
        self.assertEqual(prefer.data["formatted"], "prefer - preferred - preferred")

    def test_grammar_check_finds_spelling_and_tense(self) -> None:
        response = self.service.execute("check grammar I go to chracter yesterday.")
        self.assertTrue(response.success)
        spelling = response.data["spelling_issues"]
        grammar_issues = response.data["grammar_issues"]
        grammar_errors = response.data["grammar_errors"]
        semantic_warnings = response.data["semantic_warnings"]

        self.assertTrue(any(item["suggestion"] == "character" for item in spelling))
        self.assertTrue(any(item["category"] == "Tense" for item in grammar_issues))
        self.assertTrue(any(item["category"] == "Tense" for item in grammar_errors))
        self.assertTrue(any(item["category"] == "Semantic" for item in semantic_warnings))
        self.assertEqual(response.data["corrected_text"], "I went to character yesterday.")

    def test_subject_verb_agreement_flags_proper_name_subject(self) -> None:
        response = self.service.execute("check grammar Nhan go to school every day.")
        self.assertTrue(response.success)
        self.assertTrue(any(item["category"] == "Agreement" for item in response.data["grammar_errors"]))
        self.assertIn("Nhan goes to school every day.", response.data["corrected_text"])

    def test_subject_verb_agreement_flags_singular_and_plural_noun_phrases(self) -> None:
        singular = self.service.execute("check grammar The student go to school every day.")
        plural = self.service.execute("check grammar The students goes to school every day.")

        self.assertTrue(any(item["category"] == "Agreement" for item in singular.data["grammar_errors"]))
        self.assertTrue(any(item["category"] == "Agreement" for item in plural.data["grammar_errors"]))
        self.assertIn("The student goes to school every day.", singular.data["corrected_text"])
        self.assertIn("The students go to school every day.", plural.data["corrected_text"])

    def test_subject_verb_agreement_handles_singular_nouns_ending_in_s(self) -> None:
        response = self.service.execute("check grammar Physics are difficult for some students.")
        self.assertTrue(response.success)
        self.assertTrue(any(item["category"] == "Agreement" for item in response.data["grammar_errors"]))
        self.assertIn("Physics is difficult for some students.", response.data["corrected_text"])

    def test_semantic_warning_for_odd_but_spelled_phrase(self) -> None:
        response = self.service.execute("check grammar However I go to chracter school yesterday.")
        self.assertTrue(response.success)
        self.assertTrue(response.data["semantic_warnings"])
        self.assertEqual(response.data["corrected_text"], "However, I went to character school yesterday.")

    def test_semantic_warning_for_go_to_non_destination(self) -> None:
        response = self.service.execute("check grammar I go to chracter yesterday.")
        self.assertTrue(response.success)
        semantic_issues = response.data["semantic_warnings"]
        self.assertTrue(semantic_issues)
        self.assertIn("go to", semantic_issues[0]["message"])

    def test_semantic_collocation_warning_can_apply_safe_rewrite(self) -> None:
        response = self.service.execute("check grammar I make homework every day.")
        self.assertTrue(response.success)
        self.assertTrue(response.data["semantic_warnings"])
        self.assertEqual(response.data["corrected_text"], "I do homework every day.")

    def test_parse_error_returns_did_you_mean_suggestion(self) -> None:
        response = self.service.execute("chexk grammar He go to school every day.")
        self.assertFalse(response.success)
        self.assertIn("Did you mean", response.message)
        self.assertIn("check grammar He go to school every day.", response.suggestions)

    def test_svo_examples_are_reported_for_missing_subject_or_missing_verb(self) -> None:
        missing_subject = self.service.execute("check grammar Go to school every day.")
        missing_verb = self.service.execute("check grammar The beautiful park near the river.")

        self.assertTrue(any(item["category"] == "SVO" for item in missing_subject.data["grammar_errors"]))
        self.assertTrue(any(item["category"] == "SVO" for item in missing_verb.data["grammar_errors"]))

    def test_parse_error_only_returns_grammar_valid_command_suggestions(self) -> None:
        response = self.service.execute("chek gramar He go to school every day.")
        self.assertFalse(response.success)
        self.assertIn("check grammar He go to school every day.", response.suggestions)
        self.assertNotIn("check gramar He go to school every day.", response.suggestions)

    def test_missing_grammar_keyword_gets_inserted_into_suggestion(self) -> None:
        response = self.service.execute("check He go to school every day.")
        self.assertFalse(response.success)
        self.assertIn("check grammar He go to school every day.", response.suggestions)

    def test_multi_command_paste_is_rejected_before_it_pollutes_history(self) -> None:
        response = self.service.execute(
            "check grammar I go to chracter yesterday.\ncheck grammar He go to school every day."
        )
        self.assertFalse(response.success)
        self.assertEqual(response.command, "invalid_multi_command")
        self.assertIn("multiple DSL commands", response.message)
        self.assertEqual(response.suggestions, ["check grammar I go to chracter yesterday."])

    def test_revision_command_suggestion_repairs_both_tokens(self) -> None:
        response = self.service.execute("revison paln")
        self.assertFalse(response.success)
        self.assertIn("revision plan", response.suggestions)

    def test_reset_history_command_clears_the_current_users_profile(self) -> None:
        service, db_path = self.create_isolated_service()
        try:
            service.execute("check grammar I go to chracter yesterday.", user_id="learner-reset")
            before = service.execute("history", user_id="learner-reset")
            self.assertGreaterEqual(before.data["total_commands"], 1)

            reset = service.execute("reset history", user_id="learner-reset")
            self.assertTrue(reset.success)
            self.assertEqual(reset.command, "reset history")
            self.assertGreaterEqual(reset.data["deleted_runs"], 1)

            after_history = service.execute("history", user_id="learner-reset")
            self.assertEqual(after_history.data["total_commands"], 0)

            after_plan = service.execute("revision plan", user_id="learner-reset")
            self.assertEqual(after_plan.data["summary"]["reviewed_submissions"], 0)
            self.assertFalse(after_plan.data["recurring_patterns"])
        finally:
            if db_path.exists():
                db_path.unlink()

    def test_explain_command_returns_rule_trace_and_coverage(self) -> None:
        response = self.service.execute("explain grammar He go to school every day.")
        self.assertTrue(response.success)
        self.assertEqual(response.command, "explain")
        self.assertGreater(len(response.data["rule_trace"]), 0)
        self.assertGreater(len(response.data["matched_coverage"]), 0)
        self.assertIn("pipeline_summary", response.data)
        self.assertGreaterEqual(response.data["pipeline_summary"]["knowledge_stats"]["imported_sources"], 4)

    def test_check_command_carries_pipeline_context_for_ui(self) -> None:
        response = self.service.execute("check grammar I make homework every day.")
        self.assertTrue(response.success)
        self.assertIn("pipeline_summary", response.data)
        self.assertIn("source_manifest", response.data)
        self.assertGreaterEqual(response.data["pipeline_summary"]["knowledge_stats"]["imported_collocation_rules"], 160)
        self.assertIn("corrections", response.data)
        self.assertIn("knowledge_hits", response.data)

    def test_check_command_exposes_correction_log_and_vocabulary_profile(self) -> None:
        response = self.service.execute(
            "check grammar Yesterday I do a decision quickly because I make research for my school project."
        )
        self.assertTrue(response.success)
        self.assertTrue(response.data["corrections"])
        self.assertTrue(any(item["knowledge_source"] == "src-collocation-imported" for item in response.data["corrections"]))
        self.assertTrue(response.data["vocabulary_profile"])
        self.assertTrue(any(hit["source_id"] == "src-cambridge-cefr-imported" for hit in response.data["knowledge_hits"]))

    def test_clause_segmenter_propagates_simple_past_across_long_sentence(self) -> None:
        response = self.service.execute(
            "check grammar Yesterday I do a decision quickly because I make research for my school project, and my sister says the truth during her presentation while my brother makes attention in class."
        )
        self.assertTrue(response.success)
        self.assertIn("I made a decision quickly", response.data["corrected_text"])
        self.assertIn("I did research for my school project", response.data["corrected_text"])
        self.assertIn("my sister told the truth", response.data["corrected_text"])
        self.assertIn("my brother paid attention in class", response.data["corrected_text"])
        self.assertTrue(
            any(item["rule_id"] == "RULE-CLAUSE-TENSE-PROPAGATION" for item in response.data["grammar_errors"])
        )

    def test_check_grammar_accepts_book_paragraph_with_typographic_punctuation(self) -> None:
        paragraph = (
            "check grammar Thus the literature does suggest food promotion is influencing children’s diet in a number of ways. "
            "This does not amount to proof; as noted above with this kind of research, incontrovertible proof simply isn’t attainable. "
            "Nor do all studies point to this conclusion; several have not found an effect. "
            "In addition, very few studies have attempted to measure how strong these effects are relative to other factors influencing children’s food choices. "
            "Nonetheless, many studies have found clear effects and they have used sophisticated methodologies that make it possible to determine that i) these effects are not just due to chance; "
            "ii) they are independent of other factors that may influence diet, such as parents’ eating habits or attitudes; "
            "and iii) they occur at a brand and category level."
        )
        response = self.service.execute(paragraph)
        self.assertTrue(response.success)
        self.assertEqual(response.command, "check grammar")
        self.assertIn("children’s diet", response.data["original_text"])
        self.assertIn("isn’t attainable", response.data["original_text"])
        self.assertEqual(response.data["corrected_text"], response.data["original_text"])

    def test_essay_paragraph_detects_word_choice_preposition_and_relative_clause_issues(self) -> None:
        paragraph = (
            "check grammar Nowadays, some advertisements convey the message in an inappropriate way by hidden encourage "
            "children’s bully or discriminating a certain religion. "
            "These unquestionable content can effect on children’s behaviour. "
            "In addition, in some modern cities, there are a lot of posters, which is designed on the wall. "
            "This can make the aesthetic of the city less appeal. "
            "This can lose the traditional appeal of the city, which makes people feel less interested in visiting their country."
        )
        response = self.service.execute(paragraph)
        self.assertTrue(response.success)
        self.assertEqual(response.command, "check grammar")
        self.assertFalse(response.data["spelling_issues"])
        self.assertGreaterEqual(len(response.data["grammar_errors"]), 3)
        self.assertGreaterEqual(len(response.data["semantic_warnings"]), 6)
        self.assertTrue(any(item["category"] == "Preposition" for item in response.data["grammar_errors"]))
        self.assertTrue(any(item["rule_id"] == "RULE-RELATIVE-CLAUSE-AGREEMENT" for item in response.data["grammar_errors"]))
        self.assertTrue(any(item["rule_id"] == "RULE-DETERMINER-NOUN-AGREEMENT" for item in response.data["grammar_errors"]))
        self.assertIn("covertly encouraging", response.data["corrected_text"])
        self.assertIn("children’s bullying", response.data["corrected_text"])
        self.assertIn("discriminating against a certain religion", response.data["corrected_text"])
        self.assertIn("this objectionable content", response.data["corrected_text"].lower())
        self.assertIn("affect children’s behaviour", response.data["corrected_text"])
        self.assertIn("which are", response.data["corrected_text"])
        self.assertIn("less appealing", response.data["corrected_text"])
        self.assertIn("reduce the traditional appeal", response.data["corrected_text"])
        self.assertIn("visiting the city", response.data["corrected_text"])

    def test_history_tracks_recent_commands_for_the_current_user(self) -> None:
        service, db_path = self.create_isolated_service()
        try:
            service.execute("spell generte", user_id="user-history")
            service.execute("check grammar I go to chracter yesterday.", user_id="user-history")

            response = service.execute("history", user_id="user-history")
            self.assertTrue(response.success)
            self.assertEqual(response.command, "history")
            self.assertEqual(response.data["total_commands"], 2)
            self.assertEqual(len(response.data["entries"]), 2)
            self.assertEqual(response.data["entries"][0]["command_name"], "check grammar")
            self.assertEqual(response.data["entries"][1]["command_name"], "spell")
        finally:
            if db_path.exists():
                db_path.unlink()

    def test_revision_plan_uses_only_the_current_users_checked_paragraphs(self) -> None:
        service, db_path = self.create_isolated_service()
        try:
            service.execute("check grammar I go to chracter yesterday.", user_id="learner-a")
            service.execute("check grammar He go to school every day.", user_id="learner-a")
            service.execute("check grammar I have been working since yesterday.", user_id="learner-b")

            response = service.execute("revision plan", user_id="learner-a")
            self.assertTrue(response.success)
            self.assertEqual(response.command, "revision plan")
            self.assertEqual(response.data["summary"]["reviewed_submissions"], 2)
            self.assertGreaterEqual(response.data["summary"]["tracked_issues"], 3)
            self.assertTrue(response.data["recurring_patterns"])
            titles = [item["title"] for item in response.data["recurring_patterns"]]
            self.assertTrue(any(title in {"Tense consistency", "Subject-verb agreement", "Spelling accuracy"} for title in titles))
            self.assertEqual(titles.count("Tense consistency"), 1)
            self.assertTrue(response.data["revision_checklist"])
        finally:
            if db_path.exists():
                db_path.unlink()


if __name__ == "__main__":
    unittest.main()
