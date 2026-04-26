from __future__ import annotations

from .suggestion_engine import SuggestionEngine
from .types import SpellingSuggestion
from .verb_engine import VerbEngine


COMMON_CONTRACTION_SUGGESTIONS = {
    "arent": "aren't",
    "cant": "can't",
    "couldnt": "couldn't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "dont": "don't",
    "hadnt": "hadn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "isnt": "isn't",
    "shouldnt": "shouldn't",
    "wasnt": "wasn't",
    "werent": "weren't",
    "wont": "won't",
    "wouldnt": "wouldn't",
}
SUBJECT_CONTEXT_WORDS = {
    "everybody",
    "everyone",
    "he",
    "i",
    "it",
    "physics",
    "she",
    "somebody",
    "someone",
    "they",
    "we",
    "who",
    "you",
}
OBJECT_CONTEXT_WORDS = {"her", "him", "it", "me", "them", "us", "you"}
VERB_CONTEXT_AUXILIARIES = {
    "can",
    "could",
    "did",
    "do",
    "does",
    "dont",
    "don't",
    "had",
    "has",
    "have",
    "may",
    "might",
    "must",
    "not",
    "should",
    "to",
    "was",
    "were",
    "will",
    "would",
}
ADJECTIVE_SUFFIXES = (
    "al",
    "ic",
    "ive",
    "ous",
    "able",
    "ible",
    "ful",
    "less",
    "ent",
    "ant",
)
COMMON_NOUN_FOLLOWERS = {
    "place",
    "places",
    "people",
    "thing",
    "things",
    "area",
    "areas",
    "scene",
    "scenes",
    "environment",
    "environments",
    "resource",
    "resources",
    "world",
    "life",
    "history",
    "activity",
    "activities",
    "day",
    "days",
    "way",
    "ways",
}


class SpellingChecker:
    def __init__(
        self,
        dictionary_words: set[str],
        suggestion_engine: SuggestionEngine | None = None,
        verb_engine: VerbEngine | None = None,
    ) -> None:
        self.dictionary_words = {word.lower() for word in dictionary_words}
        self.suggestion_engine = suggestion_engine or SuggestionEngine()
        self.verb_engine = verb_engine

    def check_words(self, words: list[str]) -> list[SpellingSuggestion]:
        suggestions: list[SpellingSuggestion] = []
        normalized_words = [word.lower().replace("â€™", "'").replace("â€˜", "'") for word in words]

        for position, word in enumerate(words):
            normalized = normalized_words[position]
            if not normalized.isalpha():
                continue
            if "'" in normalized:
                continue
            if normalized in COMMON_CONTRACTION_SUGGESTIONS:
                suggestion = COMMON_CONTRACTION_SUGGESTIONS[normalized]
                suggestions.append(
                    SpellingSuggestion(
                        token=word,
                        suggestion=suggestion,
                        distance=1,
                        position=position,
                        alternatives=[suggestion],
                    )
                )
                continue
            if normalized in self.dictionary_words:
                continue
            if word.istitle() or word.isupper():
                continue

            ranked = self.suggestion_engine.ranked_suggestions(normalized, self.dictionary_words, threshold=2, limit=8)
            ranked = self._rank_suggestions_for_context(
                token=normalized,
                ranked=ranked,
                words=normalized_words,
                position=position,
            )
            if not ranked:
                continue

            candidate, distance = ranked[0]
            suggestions.append(
                SpellingSuggestion(
                    token=word,
                    suggestion=candidate,
                    distance=distance,
                    position=position,
                    alternatives=[item[0] for item in ranked[:3]],
                )
            )

        return suggestions

    def _rank_suggestions_for_context(
        self,
        *,
        token: str,
        ranked: list[tuple[str, int]],
        words: list[str],
        position: int,
    ) -> list[tuple[str, int]]:
        if not ranked:
            return ranked

        previous = words[position - 1] if position > 0 else ""
        next_word = words[position + 1] if position + 1 < len(words) else ""
        prefers_verb = self._looks_like_verb_context(previous, next_word)
        prefers_adjective = self._looks_like_adjective_context(next_word)

        if prefers_verb:
            verb_candidates = [item for item in ranked if self._candidate_is_verb(item[0].lower())]
            if verb_candidates:
                ranked = verb_candidates
        elif prefers_adjective:
            adj_candidates = [item for item in ranked if self._is_likely_adjective(item[0].lower())]
            if adj_candidates:
                ranked = adj_candidates

        def sort_key(item: tuple[str, int]) -> tuple[int, int, int, int, int, int, str]:
            candidate, distance = item
            lowered = candidate.lower()
            return (
                distance,
                0 if prefers_verb and self._candidate_is_verb(lowered) else 1,
                0 if prefers_adjective and self._is_likely_adjective(lowered) else 1,
                0 if self._is_subsequence(token, lowered) else 1,
                abs(len(lowered) - len(token)),
                0 if token and lowered and token[0] == lowered[0] else 1,
                lowered,
            )

        ranked.sort(key=sort_key)
        return ranked

    def _looks_like_verb_context(self, previous: str, next_word: str) -> bool:
        if previous in SUBJECT_CONTEXT_WORDS or previous in VERB_CONTEXT_AUXILIARIES:
            return True
        if next_word in OBJECT_CONTEXT_WORDS:
            return True
        return False

    def _looks_like_adjective_context(self, next_word: str) -> bool:
        if next_word in COMMON_NOUN_FOLLOWERS:
            return True
        # If followed by a plural word that is not a verb, it's likely a noun
        if next_word.endswith("s") and len(next_word) > 3:
            if self.verb_engine and not self.verb_engine.is_known_verb(next_word):
                return True
        return False

    def _is_likely_adjective(self, candidate: str) -> bool:
        return candidate.endswith(ADJECTIVE_SUFFIXES)

    def _candidate_is_verb(self, token: str) -> bool:
        if self.verb_engine is None:
            return False
        return (
            self.verb_engine.is_known_verb(token)
            or self.verb_engine.is_past_form(token)
            or self.verb_engine.is_participle(token)
            or self.verb_engine.is_gerund(token)
        )

    @staticmethod
    def _is_subsequence(source: str, candidate: str) -> bool:
        if not source:
            return False

        source_index = 0
        for character in candidate:
            if source_index < len(source) and source[source_index] == character:
                source_index += 1
        return source_index == len(source)
