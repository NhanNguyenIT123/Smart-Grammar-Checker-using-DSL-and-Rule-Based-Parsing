from __future__ import annotations

from .suggestion_engine import SuggestionEngine
from .types import SpellingSuggestion


class SpellingChecker:
    def __init__(self, dictionary_words: set[str], suggestion_engine: SuggestionEngine | None = None) -> None:
        self.dictionary_words = {word.lower() for word in dictionary_words}
        self.suggestion_engine = suggestion_engine or SuggestionEngine()

    def check_words(self, words: list[str]) -> list[SpellingSuggestion]:
        suggestions: list[SpellingSuggestion] = []

        for position, word in enumerate(words):
            normalized = word.lower().replace("’", "'").replace("‘", "'")
            if not normalized.isalpha():
                continue
            if "'" in normalized:
                continue
            if normalized in self.dictionary_words:
                continue
            if word.istitle() or word.isupper():
                continue

            match = self.suggestion_engine.suggest(normalized, self.dictionary_words, threshold=2)
            if not match:
                continue

            candidate, distance = match
            suggestions.append(
                SpellingSuggestion(
                    token=word,
                    suggestion=candidate,
                    distance=distance,
                    position=position,
                )
            )

        return suggestions
