from __future__ import annotations

from collections import defaultdict
from typing import Any

from .store import UserProfileStore


class RevisionPlanner:
    def __init__(self, store: UserProfileStore) -> None:
        self.store = store

    def build_plan(self, user_id: str) -> dict[str, Any]:
        source_data = self.store.get_revision_source_data(user_id)
        runs = source_data["runs"]
        issues = [
            issue
            for issue in source_data["issues"]
            if (issue.get("rule_id") or "").upper() != "SYSTEM_ERROR"
        ]

        if not runs or not issues:
            return {
                "summary": {
                    "reviewed_submissions": len(runs),
                    "tracked_issues": len(issues),
                    "main_focus": "No recurring pattern yet",
                },
                "recurring_patterns": [],
                "recommended_focus": [],
                "revision_checklist": [],
                "recent_examples": [],
            }

        issue_groups: dict[str, dict[str, Any]] = {}
        issue_examples: dict[str, list[str]] = defaultdict(list)

        for issue in issues:
            meta = self._pattern_meta(issue)
            pattern_key = meta["bucket"]

            if pattern_key not in issue_groups:
                issue_groups[pattern_key] = {
                    "pattern_key": pattern_key,
                    "rule_id": issue.get("rule_id"),
                    "category": issue.get("category", "Unknown"),
                    "title": meta["title"],
                    "focus": meta["focus"],
                    "count": 0,
                }

            issue_groups[pattern_key]["count"] += 1
            example = self._example_text(issue)
            if example and example not in issue_examples[pattern_key] and len(issue_examples[pattern_key]) < 3:
                issue_examples[pattern_key].append(example)

        recurring_patterns = sorted(
            issue_groups.values(),
            key=lambda item: (-item["count"], item["title"]),
        )

        for pattern in recurring_patterns:
            pattern["examples"] = issue_examples.get(pattern["pattern_key"], [])

        top_patterns = recurring_patterns[:4]
        recommended_focus = [
            {
                "priority": index + 1,
                "title": pattern["title"],
                "reason": f'This pattern appeared {pattern["count"]} time(s) in your recent checked paragraphs.',
                "action": pattern["focus"],
            }
            for index, pattern in enumerate(top_patterns[:3])
        ]

        checklist = self._build_checklist(top_patterns)
        recent_examples = [
            {
                "created_at": run["created_at"],
                "command": self._compact(run["command"]),
                "corrected_excerpt": self._compact(run["corrected_text"] or run["original_text"] or ""),
                "issue_count": run["spelling_issue_count"] + run["grammar_error_count"] + run["semantic_warning_count"],
            }
            for run in runs[:4]
        ]

        return {
            "summary": {
                "reviewed_submissions": len(runs),
                "tracked_issues": len(issues),
                "main_focus": top_patterns[0]["title"],
                "last_checked_at": runs[0]["created_at"],
            },
            "recurring_patterns": top_patterns,
            "recommended_focus": recommended_focus,
            "revision_checklist": checklist,
            "recent_examples": recent_examples,
        }

    @staticmethod
    def _example_text(issue: dict[str, Any]) -> str:
        evidence = (issue.get("evidence") or "").strip()
        replacement = (issue.get("replacement") or issue.get("suggestion") or "").strip()
        if evidence and replacement:
            return f"{evidence} -> {replacement}"
        if evidence:
            return evidence
        return (issue.get("message") or "").strip()

    @staticmethod
    def _compact(text: str, limit: int = 140) -> str:
        normalized = " ".join(text.split())
        if len(normalized) <= limit:
            return normalized
        return f"{normalized[:limit - 3]}..."

    def _build_checklist(self, patterns: list[dict[str, Any]]) -> list[str]:
        checklist: list[str] = []
        for pattern in patterns[:3]:
            action = pattern["focus"]
            if action not in checklist:
                checklist.append(action)
        return checklist

    @staticmethod
    def _pattern_meta(issue: dict[str, Any]) -> dict[str, str]:
        rule_id = (issue.get("rule_id") or "").upper()
        category = (issue.get("category") or "").lower()

        if rule_id in {"RULE-TENSE-MISMATCH", "RULE-CLAUSE-TENSE-PROPAGATION"} or category == "tense":
            return {
                "bucket": "tense-consistency",
                "title": "Tense consistency",
                "focus": "Match verb forms with time markers like yesterday, now, by tomorrow, and this time tomorrow.",
            }
        if rule_id == "RULE-SUBJECT-VERB" or category == "agreement":
            return {
                "bucket": "subject-verb-agreement",
                "title": "Subject-verb agreement",
                "focus": "Recheck whether singular subjects take singular verbs and plural subjects take plural verbs.",
            }
        if rule_id == "RULE-PREPOSITION" or category == "preposition":
            return {
                "bucket": "verb-preposition-patterns",
                "title": "Verb-preposition patterns",
                "focus": "Memorize common pairs like depend on, discriminate against, and interested in.",
            }
        if rule_id == "RULE-RELATIVE-CLAUSE-AGREEMENT":
            return {
                "bucket": "relative-clause-agreement",
                "title": "Relative clause agreement",
                "focus": "When the noun before which/who is plural, keep the verb plural too.",
            }
        if rule_id == "RULE-DETERMINER-NOUN-AGREEMENT":
            return {
                "bucket": "determiner-noun-agreement",
                "title": "Determiner and noun agreement",
                "focus": "Check whether this/that/these/those match countable and uncountable nouns correctly.",
            }
        if rule_id == "SPELL-LEVENSHTEIN" or category == "spelling":
            return {
                "bucket": "spelling-accuracy",
                "title": "Spelling accuracy",
                "focus": "Slow down on low-frequency words and verify their spelling before you submit the paragraph.",
            }
        if category == "semantic":
            return {
                "bucket": "natural-collocations-and-meaning",
                "title": "Natural collocations and meaning",
                "focus": "Replace awkward verb-noun combinations with natural English collocations such as do research or make a complaint.",
            }
        return {
            "bucket": f'general:{category or "unknown"}',
            "title": issue.get("category", "General review"),
            "focus": "Review this pattern carefully in your next paragraph and compare the original sentence with the corrected output.",
        }
