from __future__ import annotations

from typing import Any


class QuizGrader:
    PASSING_RATIO = 0.5

    @staticmethod
    def normalize_answer(text: str) -> str:
        compact = " ".join((text or "").strip().lower().split())
        compact = compact.replace(" .", ".").replace(" ?", "?").replace(" !", "!")
        return compact

    def grade(self, quiz: dict[str, Any], answers: list[dict[str, Any]], grammar_checker) -> dict[str, Any]:
        expected_items = list(quiz.get("exercise_payload", []))
        answer_map = {int(entry["question_id"]): entry["answer_text"] for entry in answers}

        item_results: list[dict[str, Any]] = []
        correct_count = 0
        for index, item in enumerate(expected_items, start=1):
            student_answer = answer_map.get(index, "")
            accepted = [item.get("expected_answer", ""), *(item.get("accepted_variants", []) or [])]
            accepted = [candidate for candidate in accepted if candidate]
            expected_normalized = {self.normalize_answer(candidate) for candidate in accepted}
            student_normalized = self.normalize_answer(student_answer)
            is_correct = bool(student_normalized and student_normalized in expected_normalized)
            score = 1 if is_correct else 0
            correct_count += score

            feedback = ""
            if not is_correct and student_answer.strip():
                analysis = grammar_checker.check(student_answer)
                
                # Diagnostic comparison for focused feedback
                diagnostic = self._diagnose_error(student_answer, item.get("expected_answer", ""))
                
                feedback = {
                    "corrected_text": analysis.corrected_text,
                    "grammar_errors": [issue.message for issue in analysis.grammar_errors[:3]],
                    "semantic_warnings": [issue.message for issue in analysis.semantic_warnings[:2]],
                }
                
                if diagnostic:
                    feedback["grammar_errors"].insert(0, diagnostic)

            item_results.append(
                {
                    "question_id": index,
                    "item_index": index,
                    "prompt": item.get("prompt"),
                    "student_answer": student_answer,
                    "answer_text": student_answer,
                    "expected_answer": item.get("expected_answer"),
                    "accepted_variants": item.get("accepted_variants", []),
                    "score": score,
                    "max_score": 1,
                    "is_correct": is_correct,
                    "feedback": feedback,
                }
            )

        max_score = len(expected_items)
        summary = self._summarize(item_results)
        return {
            "score": correct_count,
            "max_score": max_score,
            "status": "passed" if max_score and (correct_count / max_score) >= self.PASSING_RATIO else "failed",
            "item_results": item_results,
            "feedback_summary": summary,
        }

    def _diagnose_error(self, student: str, expected: str) -> str | None:
        s = self.normalize_answer(student)
        e = self.normalize_answer(expected)
        if not s or not e:
            return None
            
        # 1. Missing Future Auxiliary
        if "will" in e and "will" not in s:
            return "It looks like you're missing the 'will' auxiliary for the future tense."
            
        # 2. Missing Negation
        if ("not" in e or "n't" in e) and ("not" not in s and "n't" not in s):
            return "Don't forget to make the sentence negative (using 'not' or \"n't\")."
            
        # 3. Third-person 's' check
        if e.endswith('s') and not s.endswith('s'):
             return "Check your subject-verb agreement—does the verb need an 's' at the end?"
        if not e.endswith('s') and s.endswith('s') and len(e) > 3:
             return "This verb might not need the 's' ending for this subject."

        # 4. Continuous '-ing' check
        if e.endswith('ing') and not s.endswith('ing'):
             return "This exercise seems to require the continuous (-ing) form."
             
        # 5. Near-miss (Spelling heuristic)
        if len(s) > 3 and len(e) > 3:
            diff_count = sum(1 for a, b in zip(s, e) if a != b) + abs(len(s) - len(e))
            if diff_count <= 2:
                 return "You're very close! Double-check your spelling."

        return None

    @staticmethod
    def _summarize(item_results: list[dict[str, Any]]) -> str:
        incorrect = [item for item in item_results if not item["is_correct"]]
        if not incorrect:
            return "Excellent work. Every answer matched the expected grammar target."
        if len(incorrect) == 1:
            return "One item still needs revision. Compare your answer with the expected grammar pattern."
        return f"{len(incorrect)} items still need revision. Focus on the incorrect prompts and try again."
