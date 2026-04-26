from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SpellingSuggestion:
    token: str
    suggestion: str
    distance: int
    position: int
    alternatives: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GrammarIssue:
    category: str
    message: str
    sentence: str
    evidence: str | None = None
    suggestion: str | None = None
    replacement: str | None = None
    severity: str = "error"
    rule_id: str | None = None
    knowledge_source: str | None = None
    target_tense: str | None = None
    source_tense: str | None = None


@dataclass(slots=True)
class TenseSignal:
    name: str
    source: str
    evidence: str


@dataclass(slots=True)
class CorrectionEntry:
    kind: str
    original: str
    corrected: str
    reason: str
    knowledge_source: str


@dataclass(slots=True)
class VocabularyBand:
    level: str
    match_count: int
    words: list[str] = field(default_factory=list)


@dataclass(slots=True)
class KnowledgeHit:
    source_id: str
    label: str
    detail: str
    match_count: int = 0
    examples: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GrammarAnalysis:
    original_text: str
    normalized_text: str
    corrected_text: str
    sentence_count: int
    spelling_issues: list[SpellingSuggestion] = field(default_factory=list)
    grammar_issues: list[GrammarIssue] = field(default_factory=list)
    grammar_errors: list[GrammarIssue] = field(default_factory=list)
    semantic_warnings: list[GrammarIssue] = field(default_factory=list)
    detected_tenses: list[TenseSignal] = field(default_factory=list)
    corrections: list[CorrectionEntry] = field(default_factory=list)
    vocabulary_profile: list[VocabularyBand] = field(default_factory=list)
    knowledge_hits: list[KnowledgeHit] = field(default_factory=list)


@dataclass(slots=True)
class RuleTrace:
    rule_id: str
    stage: str
    matched: bool
    sentence: str
    detail: str
    evidence: str | None = None


@dataclass(slots=True)
class CoverageEntry:
    id: str
    label: str
    units: str
    support_level: str = "partial"
    capabilities: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)


@dataclass(slots=True)
class GrammarExplanation:
    analysis: GrammarAnalysis
    rule_trace: list[RuleTrace] = field(default_factory=list)
    matched_coverage: list[CoverageEntry] = field(default_factory=list)
    coverage_matrix: list[CoverageEntry] = field(default_factory=list)


@dataclass(slots=True)
class CommandResponse:
    success: bool
    command: str
    message: str
    data: dict
    suggestions: list[str] = field(default_factory=list)
