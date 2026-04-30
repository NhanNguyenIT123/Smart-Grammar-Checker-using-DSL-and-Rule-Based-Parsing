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
class FeatureExpr:
    name: str


@dataclass(slots=True)
class AndExpr:
    left: "BooleanExprNode"
    right: "BooleanExprNode"


@dataclass(slots=True)
class OrExpr:
    left: "BooleanExprNode"
    right: "BooleanExprNode"


@dataclass(slots=True)
class ComparisonExpr:
    field: str
    operator: str
    value: float
    is_percentage: bool = False


@dataclass(slots=True)
class StatusExpr:
    status: str


BooleanExprNode = Union[FeatureExpr, AndExpr, OrExpr]
StudentFilterNode = Union[ComparisonExpr, StatusExpr, AndExpr, OrExpr]


@dataclass(slots=True)
class GenerateExerciseCommand:
    requested_count: int | None
    feature_expr: BooleanExprNode
    raw_feature_text: str
    singular_form_requested: bool = False


@dataclass(slots=True)
class CreateQuizCommand:
    title: str
    requested_count: int
    feature_expr: BooleanExprNode
    raw_feature_text: str


@dataclass(slots=True)
class AnswerEntry:
    question_id: int
    answer_text: str


@dataclass(slots=True)
class SubmitAnswersCommand:
    quiz_id: int
    answers: list[AnswerEntry]


@dataclass(slots=True)
class ShowStudentsCommand:
    filter_expr: StudentFilterNode | None = None
    quiz_id: int | None = None


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
class ShowClassCommand:
    class_id: int


@dataclass(slots=True)
class ShowResultsCommand:
    student_username: str
    quiz_id: int | None = None


@dataclass(slots=True)
class ShowQuizCommand:
    quiz_id: int


@dataclass(slots=True)
class HelpCommand:
    pass


CommandNode = Union[
    GrammarCheckCommand,
    GenerateExerciseCommand,
    CreateQuizCommand,
    SubmitAnswersCommand,
    ShowStudentsCommand,
    ShowResultsCommand,
    ShowQuizCommand,
    ShowClassCommand,
    RevisionPlanCommand,
    HistoryCommand,
    ResetHistoryCommand,
    VerbLookupCommand,
    SpellLookupCommand,
    SynonymLookupCommand,
    HelpCommand,
]
