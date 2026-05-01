from __future__ import annotations

from typing import Iterable


import re


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
            {"suffix": "quiz", "takes_tail": True},
            {"suffix": "history", "takes_tail": True},
            {"suffix": "revision plan", "takes_tail": False},
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
        "results",
        "quiz",
        "for",
        "student",
        "plan",
        "score",
        "status",
        "with",
        "exercises",
        "present",
        "simple",
        "continuous",
        "perfect",
        "past",
        "future",
        "affirmative",
        "negative",
        "interrogative",
        "and",
        "or",
        "not",
        ">",
        "<",
        ">=",
        "<=",
        "=",
        "!=",
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
        # Split by whitespace but keep quoted strings together
        parts = re.findall(r'"[^"]*"|\'[^\']*\'|\S+', text)
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
            if first_token == "create":
                suggestions.extend(self._suggest_create(parts))
                continue

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

    def _suggest_create(self, parts: list[str]) -> list[str]:
        if len(parts) == 1:
            return ["create quiz"]
        
        second = parts[1].lower()
        if second != "quiz":
            second_match = self.suggest(second, ["quiz"], threshold=2)
            if second_match:
                second = "quiz"
            else:
                return ["create quiz"]

        # If it's just 'create quiz'
        if len(parts) == 2:
            return ['create quiz "My New Quiz" generate 5 exercises with present simple']

        # Look for the title and the count
        # Typical: create quiz "title" generate 5 exercises with ...
        # Or: create quiz "title" with 5 exercises with ...
        
        title = None
        for i, part in enumerate(parts):
            if part.startswith('"'):
                title = part
                break
        
        if title is None and len(parts) >= 3:
            candidate = parts[2]
            if candidate.lower() not in {"generate", "with"} and not candidate.isdigit():
                title = f'"{candidate}"'
        
        if title is None:
            title = '"My New Quiz"'
        
        # Look for the count
        count = "5"
        count_idx = -1
        for i, part in enumerate(parts):
            if part.isdigit():
                count = part
                count_idx = i
                break
        
        # Look for 'exercises' keyword
        exercises_kw = "exercises"
        if count_idx != -1 and count_idx + 1 < len(parts):
            ex_token = parts[count_idx + 1].lower()
            if ex_token != "exercises":
                ex_match = self.suggest(ex_token, ["exercises"], threshold=2)
                if ex_match:
                    exercises_kw = "exercises"
        
        # Reconstruct with tail
        # We find where 'with' or features start. Usually after 'exercises'
        tail_start = 3
        if count_idx != -1:
            tail_start = count_idx + 2
        
        tail = self._correct_tail_keywords(parts[tail_start:])
        if "with" not in [t.lower() for t in tail] and tail:
            # Check if the first tail part is close to 'with'
            if self.levenshtein(tail[0].lower(), "with") <= 1:
                tail[0] = "with"
            else:
                tail.insert(0, "with")
        elif not tail:
            tail = ["with", "present", "simple"]

        return [f'create quiz {title} generate {count} {exercises_kw} {" ".join(tail)}']

    def _suggest_generate(self, parts: list[str]) -> list[str]:
        if len(parts) == 1:
            return ["generate exercise"]

        second = parts[1].lower()
        if second.isdigit():
            if len(parts) == 2:
                return [f"generate {second} exercises"]
            
            tail = self._correct_tail_keywords(parts[2:])
            # If the user already provided 'exercises' (or a typo of it), don't duplicate it
            if tail and tail[0].lower() == "exercises":
                return [f'generate {second} {" ".join(tail)}']
            
            if "with" not in [t.lower() for t in tail] and tail:
                # Check if the first tail part is close to 'with'
                if self.levenshtein(tail[0].lower(), "with") <= 1:
                    tail[0] = "with"
                else:
                    tail.insert(0, "with")
            elif not tail:
                tail = ["with", "present", "simple"]

            return [f'generate {second} exercises {" ".join(tail)}']
        
        if second != "exercise":
            second_match = self.suggest(second, ["exercise"], threshold=2)
            if second_match:
                second = "exercise"
            else:
                return ["generate exercise"]
        
        tail = self._correct_tail_keywords(parts[2:])
        if tail and tail[0].lower() == "exercise":
            return [f'generate {" ".join(tail)}']
            
        if "with" not in [t.lower() for t in tail] and tail:
            # Check if the first tail part is close to 'with'
            if self.levenshtein(tail[0].lower(), "with") <= 1:
                tail[0] = "with"
            else:
                tail.insert(0, "with")
        elif not tail:
            tail = ["with", "present", "simple"]

        return [f'generate exercise {" ".join(tail)}']

    def _correct_tail_keywords(self, parts: list[str]) -> list[str]:
        corrected: list[str] = []
        for part in parts:
            lowered = part.lower()
            
            # 1. Skip if it's already a quoted string
            if part.startswith('"') or part.startswith("'"):
                corrected.append(part)
                continue
            
            # 2. Skip if it's already in CORE_KEYWORDS (case insensitive check)
            if lowered in self.CORE_KEYWORDS:
                corrected.append(lowered)
                continue

            # 3. If it's a number, don't touch it.
            if lowered.isdigit():
                corrected.append(part)
                continue

            # 4. Try to suggest a keyword if it's close
            dynamic_threshold = 1 if len(lowered) <= 2 else 2
            match = self.suggest(lowered, self.CORE_KEYWORDS, threshold=dynamic_threshold)
            
            if match:
                corrected.append(match[0])
            else:
                corrected.append(part)
        return corrected
