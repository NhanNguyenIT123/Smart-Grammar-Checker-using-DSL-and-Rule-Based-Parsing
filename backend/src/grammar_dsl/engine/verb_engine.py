from __future__ import annotations


class VerbEngine:
    def __init__(self, verbs: dict[str, list[str]]) -> None:
        self.verbs = {base.lower(): [item.lower() for item in forms] for base, forms in verbs.items()}
        self.reverse_index = self._build_reverse_index()

    def _build_reverse_index(self) -> dict[str, str]:
        index: dict[str, str] = {}
        for base, forms in self.verbs.items():
            all_forms = {base, *forms, self.third_person_singular(base), self.gerund(base)}
            if base == "be":
                all_forms.update({"am", "is", "are", "were"})
            if base == "have":
                all_forms.add("has")
            if base == "do":
                all_forms.add("does")
            for form in all_forms:
                index[form] = base
        return index

    def lookup(self, word: str) -> tuple[str, str, str] | None:
        base = self.to_base(word)
        if base is None:
            return None
        forms = self.verbs[base]
        return forms[0], forms[1], forms[2]

    def to_base(self, word: str) -> str | None:
        normalized = word.lower()
        if normalized in self.verbs:
            return normalized
        return self.reverse_index.get(normalized)

    def is_known_verb(self, word: str) -> bool:
        return self.to_base(word) is not None

    def is_past_form(self, word: str) -> bool:
        normalized = word.lower()
        base = self.to_base(normalized)
        if base is None:
            return normalized.endswith("ed")
        if base == "be":
            return normalized in {"was", "were"}
        return normalized == self.verbs[base][1]

    def is_participle(self, word: str) -> bool:
        normalized = word.lower()
        base = self.to_base(normalized)
        if base is None:
            return normalized.endswith("ed")
        return normalized == self.verbs[base][2]

    def is_gerund(self, word: str) -> bool:
        return word.lower().endswith("ing")

    def is_third_person_form(self, word: str) -> bool:
        normalized = word.lower()
        base = self.to_base(normalized)
        if base is None:
            return normalized.endswith("s")
        if base == "be":
            return normalized == "is"
        if base == "have":
            return normalized == "has"
        if base == "do":
            return normalized == "does"
        return normalized == self.third_person_singular(base)

    def third_person_singular(self, base: str) -> str:
        normalized = base.lower()
        if normalized == "be":
            return "is"
        if normalized == "have":
            return "has"
        if normalized == "do":
            return "does"
        if normalized.endswith("y") and len(normalized) > 1 and normalized[-2] not in "aeiou":
            return f"{normalized[:-1]}ies"
        if normalized.endswith(("s", "sh", "ch", "x", "z", "o")):
            return f"{normalized}es"
        return f"{normalized}s"

    def gerund(self, base: str) -> str:
        normalized = base.lower()
        if normalized == "be":
            return "being"
        if normalized.endswith("ie"):
            return f"{normalized[:-2]}ying"
        if normalized.endswith("e") and normalized not in {"be", "see"}:
            return f"{normalized[:-1]}ing"
        if self._is_short_cvc(normalized):
            return f"{normalized}{normalized[-1]}ing"
        return f"{normalized}ing"

    def past_form(self, base: str, subject: str | None = None) -> str:
        normalized = base.lower()
        if normalized == "be":
            return "were" if subject in {"we", "they", "you"} else "was"
        if normalized in self.verbs:
            return self.verbs[normalized][1]
        if normalized.endswith("y") and len(normalized) > 1 and normalized[-2] not in "aeiou":
            return f"{normalized[:-1]}ied"
        if normalized.endswith("e"):
            return f"{normalized}d"
        if self._is_short_cvc(normalized):
            return f"{normalized}{normalized[-1]}ed"
        return f"{normalized}ed"

    def participle_form(self, base: str) -> str:
        normalized = base.lower()
        if normalized in self.verbs:
            return self.verbs[normalized][2]
        return self.past_form(normalized)

    def suggest_for_tense(self, base: str, tense: str, subject: str | None = None) -> str:
        normalized_subject = (subject or "").lower()
        if tense == "past_simple":
            return self.past_form(base, normalized_subject or None)
        if tense == "present_simple":
            if normalized_subject in {"he", "she", "it"}:
                return self.third_person_singular(base)
            if base == "be":
                return {"i": "am", "you": "are", "we": "are", "they": "are"}.get(normalized_subject, "is")
            return base
        if tense == "present_continuous":
            auxiliary = {"i": "am", "you": "are", "we": "are", "they": "are"}.get(normalized_subject, "is")
            return f"{auxiliary} {self.gerund(base)}"
        if tense == "present_perfect":
            auxiliary = "has" if normalized_subject in {"he", "she", "it"} else "have"
            return f"{auxiliary} {self.participle_form(base)}"
        if tense == "present_perfect_continuous":
            auxiliary = "has" if normalized_subject in {"he", "she", "it"} else "have"
            return f"{auxiliary} been {self.gerund(base)}"
        if tense == "past_continuous":
            auxiliary = "were" if normalized_subject in {"we", "they", "you"} else "was"
            return f"{auxiliary} {self.gerund(base)}"
        if tense == "past_perfect":
            return f"had {self.participle_form(base)}"
        if tense == "past_perfect_continuous":
            return f"had been {self.gerund(base)}"
        if tense == "future_simple":
            return f"will {base}"
        if tense == "future_continuous":
            return f"will be {self.gerund(base)}"
        if tense == "future_perfect":
            return f"will have {self.participle_form(base)}"
        if tense == "future_perfect_continuous":
            return f"will have been {self.gerund(base)}"
        return base

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

