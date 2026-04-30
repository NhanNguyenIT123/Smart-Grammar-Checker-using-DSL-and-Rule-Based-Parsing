from __future__ import annotations

from typing import Iterable


class SuggestionEngine:
    COMMANDS = [
        "check",
        "show",
        "revision",
        "history",
        "reset",
        "spell",
        "verb",
        "synonym",
        "help",
        "generate",
        "create",
        "submit",
    ]
    STRUCTURED_COMMAND_SPECS = {
        "check": [{"suffix": "grammar", "takes_tail": True}],
        "show": [
            {"suffix": "students", "takes_tail": True},
            {"suffix": "class", "takes_tail": True},
            {"suffix": "results", "takes_tail": True},
        ],
        "revision": [{"suffix": "plan", "takes_tail": False}],
        "reset": [{"suffix": "history", "takes_tail": False}],
        "create": [{"suffix": "quiz", "takes_tail": True}],
        "submit": [{"suffix": "answers", "takes_tail": True}],
    }
    LOOKUP_COMMANDS = {"spell", "verb", "synonym"}
    CORE_KEYWORDS = {
        "grammar",
        "class",
        "students",
        "plan",
        "history",
        "quiz",
        "answers",
        "exercise",
        "exercises",
        "with",
        "for",
        "submitted",
        "passed",
        "failed",
        "score",
        "and",
        "or",
        "not",
        ">",
        "<",
        ">=",
        "<=",
        "=",
        "!=",
        "==",
    }

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
            if first_token == "generate":
                suggestions.extend(self._suggest_generate(parts))
                continue

            if first_token in self.STRUCTURED_COMMAND_SPECS:
                specs = self.STRUCTURED_COMMAND_SPECS[first_token]
                if len(parts) == 1:
                    suggestions.extend([f"{first_token} {spec['suffix']}" for spec in specs])
                    continue

                second = parts[1].lower()
                best_spec = self._select_structured_spec(second, specs)
                suffix = best_spec["suffix"]
                takes_tail = bool(best_spec["takes_tail"])

                if second == suffix:
                    # For 'check grammar', we preserve the tail as-is because it's natural language.
                    # For others (like 'show students'), we correct keywords.
                    tail = parts[2:] if suffix == "grammar" else self._correct_tail_keywords(parts[2:])
                    suggestions.append(" ".join([first_token, suffix, *tail]))
                    continue

                second_matches = self.ranked_suggestions(second, [suffix], threshold=2, limit=1)
                if second_matches:
                    tail = parts[2:] if suffix == "grammar" else self._correct_tail_keywords(parts[2:])
                    suggestions.append(" ".join([first_token, suffix, *tail]))
                    continue

                tail = self._correct_tail_keywords(parts[1:]) if takes_tail else []
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

    def _select_structured_spec(self, second: str, specs: list[dict[str, object]]) -> dict[str, object]:
        if len(specs) == 1:
            return specs[0]
        ranked: list[tuple[int, dict[str, object]]] = []
        for spec in specs:
            suffix = str(spec["suffix"])
            ranked.append((self.levenshtein(second, suffix), spec))
        ranked.sort(key=lambda item: (item[0], str(item[1]["suffix"])))
        return ranked[0][1]

    def _suggest_generate(self, parts: list[str]) -> list[str]:
        if len(parts) == 1:
            return ["generate exercise"]

        second = parts[1].lower()
        if second.isdigit():
            if len(parts) == 2:
                return [f"generate {second} exercises"]
            third = parts[2].lower()
            third_matches = self.ranked_suggestions(third, ["exercises"], threshold=2, limit=1)
            tail = self._correct_tail_keywords(parts[3:])
            if third == "exercises" or third_matches:
                return [" ".join(["generate", parts[1], "exercises", *tail])]
            return [" ".join(["generate", parts[1], "exercises", *self._correct_tail_keywords(parts[2:])])]

        second_matches = self.ranked_suggestions(second, ["exercise"], threshold=2, limit=1)
        if second == "exercise" or second_matches:
            return [" ".join(["generate", "exercise", *self._correct_tail_keywords(parts[2:])])]
        return [" ".join(["generate", "exercise", *self._correct_tail_keywords(parts[1:])])]

    def _correct_tail_keywords(self, tail_parts: list[str]) -> list[str]:
        corrected = []
        for part in tail_parts:
            lowered = part.lower()
            # 1. If it's quoted text, don't touch it
            if (part.startswith('"') and part.endswith('"')) or (
                part.startswith("'") and part.endswith("'")
            ):
                corrected.append(part)
                continue

            # 2. If it's already a keyword, keep it
            if lowered in self.CORE_KEYWORDS:
                corrected.append(part)
                continue

            # 3. If it's a number, don't touch it.
            # Operators ARE now in CORE_KEYWORDS so they can be corrected if mistyped (like '>:')
            if lowered.isdigit():
                corrected.append(part)
                continue

            # 4. Try to suggest a keyword if it's close
            # For very short words, use a stricter threshold (1) to avoid junk matches like ">" -> "or"
            dynamic_threshold = 1 if len(lowered) <= 2 else 2
            match = self.suggest(lowered, self.CORE_KEYWORDS, threshold=dynamic_threshold)
            
            if match:
                corrected.append(match[0])
            else:
                corrected.append(part)
        return corrected
