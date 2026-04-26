from __future__ import annotations

import re
from dataclasses import asdict

from grammar_dsl.data import get_repository
from grammar_dsl.dsl import ParserService
from grammar_dsl.dsl.ast import (
    GrammarCheckCommand,
    HistoryCommand,
    HelpCommand,
    ResetHistoryCommand,
    RevisionPlanCommand,
    ShowTokensCommand,
    SpellLookupCommand,
    SynonymLookupCommand,
    VerbLookupCommand,
)
from grammar_dsl.dsl.exceptions import DSLParseError
from grammar_dsl.engine import GrammarChecker, SpellingChecker, SuggestionEngine, SynonymEngine, VerbEngine
from grammar_dsl.engine.types import CommandResponse
from grammar_dsl.personalization import RevisionPlanner, UserProfileStore


class CommandService:
    MULTI_COMMAND_PATTERN = re.compile(
        r"(?:[\r\n]+|[.!?;:]\s+)(check\s+grammar|revision\s+plan|reset\s+history|history|spell\s+\S+|verb\s+\S+|synonym\s+\S+|help)\b",
        re.IGNORECASE,
    )

    def __init__(self, profile_store: UserProfileStore | None = None) -> None:
        repository = get_repository()
        self.repository = repository
        self.parser = ParserService()
        self.suggestion_engine = SuggestionEngine()
        self.verb_engine = VerbEngine(repository.verbs)
        self.synonym_engine = SynonymEngine(repository.synonyms)
        self.spelling_checker = SpellingChecker(
            repository.dictionary_words,
            self.suggestion_engine,
            self.verb_engine,
        )
        self.grammar_checker = GrammarChecker(repository, self.spelling_checker, self.verb_engine)
        self.profile_store = profile_store or UserProfileStore()
        self.revision_planner = RevisionPlanner(self.profile_store)

    def execute(self, raw_input: str, user_id: str | None = None) -> CommandResponse:
        resolved_user_id = (user_id or "local-session").strip() or "local-session"
        text = raw_input.strip()
        if not text:
            response = CommandResponse(False, "invalid", "Input is empty.", {})
            self._record_response(resolved_user_id, raw_input, response)
            return response

        multi_command_error = self._build_multi_command_error(text)
        if multi_command_error is not None:
            self._record_response(resolved_user_id, text, multi_command_error)
            return multi_command_error

        try:
            command = self.parser.parse(text)
        except DSLParseError:
            suggestions = self.suggestion_engine.suggest_command_inputs(text)
            message = "Command not recognized."
            if suggestions:
                message = "Command not recognized. Did you mean: " + " | ".join(suggestions)
            response = CommandResponse(
                success=False,
                command="invalid",
                message=message,
                data={},
                suggestions=suggestions,
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, GrammarCheckCommand):
            analysis = self.grammar_checker.check(command.paragraph)
            total_issues = len(analysis.spelling_issues) + len(analysis.grammar_issues)
            message = (
                f"Analyzed {analysis.sentence_count} sentence(s) and found {total_issues} issue(s)."
                if total_issues
                else "No obvious rule-based issues were found."
            )
            response = CommandResponse(
                True,
                "check grammar",
                message,
                self._with_pipeline_context(asdict(analysis)),
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, ShowTokensCommand):
            inspection = self.parser.inspect(command.source_text)
            parse_note = (
                f' The inspected snippet also parses as {inspection["command_type"]}.'
                if inspection["parsable"]
                else " The inspected snippet does not match a full GrammarDSL command yet."
            )
            response = CommandResponse(
                success=True,
                command="show tokens",
                message=f'Lexed {inspection["token_count"]} token(s) from the requested DSL input.{parse_note}',
                data=inspection,
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, RevisionPlanCommand):
            plan = self.revision_planner.build_plan(resolved_user_id)
            reviewed_submissions = int(plan["summary"].get("reviewed_submissions", 0))
            response = CommandResponse(
                success=True,
                command="revision plan",
                message=(
                    "No personalized revision plan yet. Run a few check grammar commands first."
                    if reviewed_submissions == 0
                    else f"Built a personalized revision plan from {reviewed_submissions} checked submission(s)."
                ),
                data=plan,
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, HistoryCommand):
            history = self.profile_store.get_command_history(resolved_user_id, limit=command.limit)
            response = CommandResponse(
                success=True,
                command="history",
                message=(
                    "No command history yet."
                    if history["total_commands"] == 0
                    else f'Loaded {len(history["entries"])} command(s) from your history.'
                ),
                data=history,
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, ResetHistoryCommand):
            deleted_runs = self.profile_store.clear_user_history(resolved_user_id)
            response = CommandResponse(
                success=True,
                command="reset history",
                message=(
                    "Your history was already empty."
                    if deleted_runs == 0
                    else f"Cleared {deleted_runs} tracked command run(s) for the current user."
                ),
                data={
                    "deleted_runs": deleted_runs,
                },
            )
            return response

        if isinstance(command, VerbLookupCommand):
            forms = self.verb_engine.lookup(command.word)
            if forms is None:
                ranked = self.suggestion_engine.ranked_suggestions(command.word, self.repository.verbs.keys(), threshold=2, limit=3)
                message = f'No verb entry found for "{command.word}".'
                if ranked:
                    message = f'No verb entry found for "{command.word}". Did you mean: {" | ".join(suggestion[0] for suggestion in ranked)}?'

                response = CommandResponse(
                    success=False,
                    command="verb",
                    message=message,
                    data={},
                    suggestions=[f"verb {suggestion[0]}" for suggestion in ranked],
                )
                self._record_response(resolved_user_id, text, response)
                return response

            response = CommandResponse(
                success=True,
                command="verb",
                message="Verb forms loaded successfully.",
                data={
                    "word": command.word.lower(),
                    "forms": {"base": forms[0], "past": forms[1], "participle": forms[2]},
                    "formatted": f"{forms[0]} - {forms[1]} - {forms[2]}",
                },
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, SpellLookupCommand):
            normalized = command.word.lower()
            if normalized in self.repository.dictionary_words:
                response = CommandResponse(
                    success=True,
                    command="spell",
                    message=f'"{normalized}" is spelled correctly.',
                    data={
                        "word": normalized,
                        "is_correct": True,
                        "closest_match": normalized,
                    },
                )
                self._record_response(resolved_user_id, text, response)
                return response

            ranked = self.suggestion_engine.ranked_suggestions(normalized, self.repository.dictionary_words, threshold=2, limit=3)
            message = f'"{normalized}" is potentially misspelled.'
            if ranked:
                message = f'Did you mean: {" | ".join(suggestion[0] for suggestion in ranked)}?'

            response = CommandResponse(
                success=True,
                command="spell",
                message=message,
                data={
                    "word": normalized,
                    "is_correct": False,
                    "closest_match": ranked[0][0] if ranked else None,
                    "distance": ranked[0][1] if ranked else None,
                },
                suggestions=[f"spell {suggestion[0]}" for suggestion in ranked],
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, SynonymLookupCommand):
            synonyms = self.synonym_engine.lookup(command.word)
            if synonyms is None:
                ranked = self.suggestion_engine.ranked_suggestions(command.word, self.repository.synonyms.keys(), threshold=2, limit=3)
                message = f'No synonym entry found for "{command.word}".'
                if ranked:
                    message = f'No synonym entry found for "{command.word}". Did you mean: {" | ".join(suggestion[0] for suggestion in ranked)}?'

                response = CommandResponse(
                    success=False,
                    command="synonym",
                    message=message,
                    data={},
                    suggestions=[f"synonym {suggestion[0]}" for suggestion in ranked],
                )
                self._record_response(resolved_user_id, text, response)
                return response

            response = CommandResponse(
                success=True,
                command="synonym",
                message="Synonym list loaded successfully.",
                data={
                    "word": command.word.lower(),
                    "synonyms": synonyms,
                    "formatted": ", ".join(synonyms),
                },
            )
            self._record_response(resolved_user_id, text, response)
            return response

        if isinstance(command, HelpCommand):
            response = CommandResponse(
                success=True,
                command="help",
                message="GrammarDSL command reference.",
                data={
                    "commands": [
                        {
                            "usage": "check grammar <paragraph>",
                            "description": "Run grammar, spelling, and semantic heuristics, then return a corrected version of the paragraph."
                        },
                        {
                            "usage": "show tokens <command>",
                            "description": "Inspect the ANTLR lexer output for a DSL command and confirm whether the snippet parses successfully."
                        },
                        {
                            "usage": "revision plan",
                            "description": "Show your recurring mistake patterns and a personalized revision checklist based on past grammar checks."
                        },
                        {
                            "usage": "history",
                            "description": "Show the recent DSL commands you have already run in this session profile."
                        },
                        {
                            "usage": "reset history",
                            "description": "Clear the stored command history and recurring-mistake profile for the current logged-in user."
                        },
                        {
                            "usage": "spell <word>",
                            "description": "Check whether a word matches the current dictionary and suggest the closest spelling."
                        },
                        {
                            "usage": "verb <word>",
                            "description": "Look up V1/V2/V3 for a verb."
                        },
                        {
                            "usage": "synonym <word>",
                            "description": "Look up synonyms for a word."
                        },
                        {
                            "usage": "help",
                            "description": "Show the supported GrammarDSL commands."
                        }
                    ],
                    "coverage_matrix": self.repository.grammar_rules.get("coverage_matrix", []),
                    "pipeline_summary": self.repository.pipeline_summary,
                    "source_manifest": self.repository.source_manifest,
                    "rule_details": self.repository.phrase_index,
                },
            )
            self._record_response(resolved_user_id, text, response)
            return response

        response = CommandResponse(False, "unknown", "Unsupported command node.", {})
        self._record_response(resolved_user_id, text, response)
        return response

    def _with_pipeline_context(self, data: dict) -> dict:
        enriched = dict(data)
        enriched["pipeline_summary"] = self.repository.pipeline_summary
        enriched["source_manifest"] = self.repository.source_manifest
        return enriched

    def _build_multi_command_error(self, text: str) -> CommandResponse | None:
        normalized = " ".join(text.split())
        lowered = normalized.lower()
        if not lowered.startswith("check grammar "):
            return None

        matches = list(self.MULTI_COMMAND_PATTERN.finditer(text))
        if not matches:
            return None

        first_command = self._extract_first_command_line(text)
        return CommandResponse(
            success=False,
            command="invalid_multi_command",
            message="It looks like you pasted multiple DSL commands into one input. Run one command at a time so history and revision plans stay accurate.",
            data={
                "detected_commands": [match.group(1) for match in matches[:4]],
            },
            suggestions=[first_command] if first_command else [],
        )

    @staticmethod
    def _extract_first_command_line(text: str) -> str:
        for line in text.splitlines():
            cleaned = line.strip()
            if cleaned:
                return cleaned
        return text.strip()

    def _record_response(self, user_id: str, raw_input: str, response: CommandResponse) -> None:
        # Avoid cluttering the history with meta-commands or internal errors
        if response.command in {"history", "help", "reset history", "unknown"}:
            return

        try:
            payload = self._build_history_payload(response)
            self.profile_store.log_command(
                user_id=user_id,
                command_text=raw_input,
                command_name=response.command,
                success=response.success,
                message=response.message,
                **payload,
            )
        except Exception:
            # Silent fail for logging to ensure primary command execution isn't interrupted
            return

    def _build_history_payload(self, response: CommandResponse) -> dict:
        if response.command == "check grammar" and response.success:
            return self._analysis_log_payload(response.data, profile_eligible=True)

        return {
            "profile_eligible": False,
            "sentence_count": 0,
            "spelling_issue_count": 0,
            "grammar_error_count": 0,
            "semantic_warning_count": 0,
            "original_text": None,
            "corrected_text": None,
            "issues": [],
        }

    def _analysis_log_payload(self, analysis: dict, *, profile_eligible: bool) -> dict:
        spelling_issues = analysis.get("spelling_issues", [])
        grammar_errors = analysis.get("grammar_errors", [])
        semantic_warnings = analysis.get("semantic_warnings", [])

        issues = [
            {
                "rule_id": "SPELL-LEVENSHTEIN",
                "category": "Spelling",
                "severity": "warning",
                "message": f'Possible spelling issue: {item.get("token")} -> {item.get("suggestion")}',
                "evidence": item.get("token"),
                "suggestion": item.get("suggestion"),
                "replacement": ",".join(item.get("alternatives", [])),
            }
            for item in spelling_issues
        ]
        issues.extend(grammar_errors)
        issues.extend(semantic_warnings)

        return {
            "profile_eligible": profile_eligible,
            "sentence_count": int(analysis.get("sentence_count", 0)),
            "spelling_issue_count": len(spelling_issues),
            "grammar_error_count": len(grammar_errors),
            "semantic_warning_count": len(semantic_warnings),
            "original_text": analysis.get("original_text"),
            "corrected_text": analysis.get("corrected_text"),
            "issues": issues,
        }
