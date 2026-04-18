from __future__ import annotations

from grammar_dsl.dsl.ast.nodes import (
    GrammarCheckCommand,
    HistoryCommand,
    HelpCommand,
    ResetHistoryCommand,
    RevisionPlanCommand,
    SpellLookupCommand,
    SynonymLookupCommand,
    VerbLookupCommand,
)
from grammar_dsl.dsl.generated.GrammarDSLVisitor import GrammarDSLVisitor


PUNCTUATION = {".", ",", "?", "!", ";", ":", ")"}
STICKY_TOKENS = {"'", "’", "‘", "-", "–", "—", "\"", "“", "”"}


def merge_tokens(tokens: list[str]) -> str:
    if not tokens:
        return ""

    result = tokens[0]
    for index, token in enumerate(tokens[1:], start=1):
        previous = tokens[index - 1]
        if token in PUNCTUATION:
            result += token
        elif token in STICKY_TOKENS or previous in STICKY_TOKENS:
            result += token
        else:
            result += f" {token}"
    return result


class ASTBuilder(GrammarDSLVisitor):
    def visitCommand(self, ctx):  # type: ignore[override]
        for child in ctx.getChildren():
            value = self.visit(child)
            if value is not None:
                return value
        return None

    def visitGrammarCheckCmd(self, ctx):  # type: ignore[override]
        return GrammarCheckCommand(paragraph=self.visit(ctx.paragraph()))



    def visitRevisionPlanCmd(self, ctx):  # type: ignore[override]
        return RevisionPlanCommand()

    def visitHistoryCmd(self, ctx):  # type: ignore[override]
        limit = 12
        if hasattr(ctx, "limit") and ctx.limit:
            try:
                limit = int(ctx.limit.text)
            except (ValueError, TypeError, AttributeError):
                pass
        return HistoryCommand(limit=limit)

    def visitResetHistoryCmd(self, ctx):  # type: ignore[override]
        return ResetHistoryCommand()

    def visitVerbCmd(self, ctx):  # type: ignore[override]
        return VerbLookupCommand(word=self.visit(ctx.lookupWord()))

    def visitSpellCmd(self, ctx):  # type: ignore[override]
        return SpellLookupCommand(word=self.visit(ctx.lookupWord()))

    def visitSynonymCmd(self, ctx):  # type: ignore[override]
        return SynonymLookupCommand(word=self.visit(ctx.lookupWord()))

    def visitHelpCmd(self, ctx):  # type: ignore[override]
        return HelpCommand()

    def visitParagraph(self, ctx):  # type: ignore[override]
        tokens = [child.getText() for child in ctx.getChildren()]
        return merge_tokens(tokens)

    def visitLookupWord(self, ctx):  # type: ignore[override]
        return ctx.getText().lower()
