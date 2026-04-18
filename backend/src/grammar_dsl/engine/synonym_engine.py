from __future__ import annotations


class SynonymEngine:
    def __init__(self, synonyms: dict[str, list[str]]) -> None:
        self.synonyms = {key.lower(): [item.lower() for item in value] for key, value in synonyms.items()}

    def lookup(self, word: str) -> list[str] | None:
        return self.synonyms.get(word.lower())
