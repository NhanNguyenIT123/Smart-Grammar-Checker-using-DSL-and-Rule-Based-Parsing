from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(slots=True)
class GrammarCheckCommand:
    paragraph: str


@dataclass(slots=True)
class ShowTokensCommand:
    source_text: str





@dataclass(slots=True)
class RevisionPlanCommand:
    pass


@dataclass(slots=True)
class HistoryCommand:
    limit: int = 12


@dataclass(slots=True)
class ResetHistoryCommand:
    pass


@dataclass(slots=True)
class VerbLookupCommand:
    word: str


@dataclass(slots=True)
class SpellLookupCommand:
    word: str


@dataclass(slots=True)
class SynonymLookupCommand:
    word: str


@dataclass(slots=True)
class HelpCommand:
    pass


CommandNode = Union[
    GrammarCheckCommand,
    ShowTokensCommand,
    RevisionPlanCommand,
    HistoryCommand,
    ResetHistoryCommand,
    VerbLookupCommand,
    SpellLookupCommand,
    SynonymLookupCommand,
    HelpCommand,
]
