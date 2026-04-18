from __future__ import annotations

from typing import Iterable


class SuggestionEngine:
    COMMANDS = ["check", "revision", "history", "reset", "spell", "verb", "synonym", "help"]
    STRUCTURED_COMMAND_SPECS = {
        "check": {"suffix": "grammar", "takes_tail": True},
        "revision": {"suffix": "plan", "takes_tail": False},
        "reset": {"suffix": "history", "takes_tail": False},
    }
    LOOKUP_COMMANDS = {"spell", "verb", "synonym"}

    def levenshtein(self, left: str, right: str) -> int:
        if left == right:
            return 0
        if not left:
            return len(right)
        if not right:
            return len(left)

        previous = list(range(len(right) + 1))
        for i, left_char in enumerate(left, start=1):
            current = [i]
            for j, right_char in enumerate(right, start=1):
                insertion = current[j - 1] + 1
                deletion = previous[j] + 1
                substitution = previous[j - 1] + (left_char != right_char)
                current.append(min(insertion, deletion, substitution))
            previous = current
        return previous[-1]

    def suggest(self, token: str, candidates: Iterable[str], threshold: int = 2) -> tuple[str, int] | None:
        normalized = token.lower()
        best_match: tuple[str, int] | None = None

        for candidate in candidates:
            distance = self.levenshtein(normalized, candidate.lower())
            if distance > threshold:
                continue
            if best_match is None or distance < best_match[1] or (
                distance == best_match[1] and candidate < best_match[0]
            ):
                best_match = (candidate, distance)

        return best_match

    def ranked_suggestions(
        self,
        token: str,
        candidates: Iterable[str],
        threshold: int = 2,
        limit: int = 3,
    ) -> list[tuple[str, int]]:
        normalized = token.lower()
        ranked: list[tuple[str, int]] = []

        for candidate in candidates:
            distance = self.levenshtein(normalized, candidate.lower())
            if distance > threshold:
                continue
            ranked.append((candidate, distance))

        ranked.sort(key=lambda item: (item[1], item[0]))
        return ranked[:limit]

    def suggest_command_inputs(self, text: str) -> list[str]:
        parts = text.strip().split()
        if not parts:
            return []

        suggestions: list[str] = []
        first = parts[0].lower()
        first_candidates = (
            [(first, 0)]
            if first in self.COMMANDS
            else self.ranked_suggestions(first, self.COMMANDS, threshold=2, limit=2)
        )

        for first_token, _ in first_candidates:
            if first_token in self.STRUCTURED_COMMAND_SPECS:
                suffix = self.STRUCTURED_COMMAND_SPECS[first_token]["suffix"]
                takes_tail = bool(self.STRUCTURED_COMMAND_SPECS[first_token]["takes_tail"])
                if len(parts) == 1:
                    suggestions.append(f"{first_token} {suffix}")
                    continue

                second = parts[1].lower()
                if second == suffix:
                    tail = parts[2:] if takes_tail else []
                    suggestions.append(" ".join([first_token, suffix, *tail]))
                    continue

                second_matches = self.ranked_suggestions(second, [suffix], threshold=2, limit=1)
                if second_matches:
                    tail = parts[2:] if takes_tail else []
                    suggestions.append(" ".join([first_token, suffix, *tail]))
                    continue

                tail = parts[1:] if takes_tail else []
                suggestions.append(" ".join([first_token, suffix, *tail]))
                continue

            if first_token in self.LOOKUP_COMMANDS:
                suggestions.append(" ".join([first_token, *parts[1:]]).strip())
                continue

            if first_token == "help":
                suggestions.append("help")
                continue

            if first_token == "history":
                suggestions.append("history")
                continue

        seen: set[str] = set()
        unique: list[str] = []
        for suggestion in suggestions:
            lowered = suggestion.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            unique.append(suggestion)
        return unique
