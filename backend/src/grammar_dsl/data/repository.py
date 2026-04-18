from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


class DataRepository:
    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parent
        self.compiled_path = self.base_path / "compiled" / "knowledge_base.json"

        if self.compiled_path.exists():
            knowledge_base = self._load_json_path(self.compiled_path)
            self.verbs: dict[str, list[str]] = knowledge_base.get("verbs", {})
            self.synonyms: dict[str, list[str]] = knowledge_base.get("synonyms", {})
            self.dictionary: list[str] = knowledge_base.get("dictionary", [])
            self.grammar_rules: dict[str, Any] = knowledge_base.get("grammar_rules", {})
            self.semantic_classes: dict[str, list[str]] = knowledge_base.get("semantic_classes", {})
            self.cefr_vocabulary: dict[str, list[str]] = knowledge_base.get("cefr_vocabulary", {})
            self.phrase_index: list[dict[str, Any]] = knowledge_base.get("phrase_index", [])
            self.pipeline_summary: dict[str, Any] = knowledge_base.get("pipeline_summary", {})
            self.source_manifest: list[dict[str, Any]] = knowledge_base.get("source_manifest", [])
            self.metadata: dict[str, Any] = knowledge_base.get("metadata", {})
        else:
            self.verbs = self._load_json("verbs.json")
            self.synonyms = self._load_json("synonyms.json")
            self.dictionary = self._load_json("dictionary.json")
            self.grammar_rules = self._load_json("grammar_rules.json")
            self.semantic_classes = {}
            self.cefr_vocabulary = {}
            self.phrase_index = []
            self.pipeline_summary = {
                "pipeline_version": "legacy-runtime",
                "compiled_at": None,
                "preprocessing_steps": ["legacy JSON loading"],
                "sources": [],
                "artifacts": [],
                "knowledge_stats": {
                    "verb_entries": len(self.verbs),
                    "synonym_entries": len(self.synonyms),
                    "dictionary_entries": len(self.dictionary),
                    "semantic_classes": 0,
                    "phrase_index_entries": 0,
                    "grammar_rules": len(self.grammar_rules.get("time_expressions", {})) + 
                                     len(self.grammar_rules.get("semantic_patterns", {}).get("unlikely_phrases", [])),
                    "coverage_entries": len(self.grammar_rules.get("coverage_matrix", [])),
                },
            }
            self.source_manifest = []
            self.metadata = {"name": "Legacy GrammarDSL Data Pack"}

    def _load_json(self, filename: str) -> Any:
        path = self.base_path / filename
        return self._load_json_path(path)

    def _load_json_path(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    @property
    def dictionary_words(self) -> set[str]:
        words = {word.lower() for word in self.dictionary}
        words.update(self._collect_strings(self.verbs))
        words.update(self._generate_inflected_verb_forms())
        words.update(self._collect_strings(self.synonyms))
        words.update(self._collect_strings(self.grammar_rules))
        words.update(self._collect_strings(self.semantic_classes))
        words.update(self._collect_strings(self.phrase_index))
        words.update({"check", "grammar", "explain", "verb", "spell", "synonym", "help"})
        return {word for word in words if word}

    def _generate_inflected_verb_forms(self) -> set[str]:
        generated: set[str] = set()
        for base, forms in self.verbs.items():
            normalized = base.lower()
            generated.update({normalized, *[item.lower() for item in forms]})
            generated.add(self._third_person_singular(normalized))
            generated.add(self._gerund(normalized))
            if normalized == "be":
                generated.update({"am", "is", "are", "was", "were", "been", "being"})
            if normalized == "have":
                generated.add("has")
            if normalized == "do":
                generated.add("does")
        return generated

    def _collect_strings(self, value: Any) -> set[str]:
        results: set[str] = set()

        if isinstance(value, dict):
            for key, item in value.items():
                results.update(self._split_phrase(str(key)))
                results.update(self._collect_strings(item))
            return results

        if isinstance(value, list):
            for item in value:
                results.update(self._collect_strings(item))
            return results

        if isinstance(value, str):
            results.update(self._split_phrase(value))

        return results

    @staticmethod
    def _split_phrase(text: str) -> set[str]:
        return {token.lower() for token in text.replace(",", " ").split()}

    @staticmethod
    def _third_person_singular(base: str) -> str:
        if base == "be":
            return "is"
        if base == "have":
            return "has"
        if base == "do":
            return "does"
        if base.endswith("y") and len(base) > 1 and base[-2] not in "aeiou":
            return f"{base[:-1]}ies"
        if base.endswith(("s", "sh", "ch", "x", "z", "o")):
            return f"{base}es"
        return f"{base}s"

    @staticmethod
    def _gerund(base: str) -> str:
        if base == "be":
            return "being"
        if base.endswith("ie"):
            return f"{base[:-2]}ying"
        if base.endswith("e") and base not in {"be", "see"}:
            return f"{base[:-1]}ing"
        if DataRepository._is_short_cvc(base):
            return f"{base}{base[-1]}ing"
        return f"{base}ing"

    @staticmethod
    def _is_short_cvc(word: str) -> bool:
        if len(word) < 3:
            return False
        vowels = "aeiou"
        return (
            word[-1] not in vowels
            and word[-1] not in {"w", "x", "y"}
            and word[-2] in vowels
            and word[-3] not in vowels
        )


@lru_cache(maxsize=1)
def get_repository() -> DataRepository:
    return DataRepository()


def clear_repository_cache() -> None:
    get_repository.cache_clear()
