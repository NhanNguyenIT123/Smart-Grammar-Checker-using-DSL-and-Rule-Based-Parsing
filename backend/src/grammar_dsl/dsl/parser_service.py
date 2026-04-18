from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream

from .error_listener import ThrowingErrorListener
from .generated.GrammarDSLLexer import GrammarDSLLexer
from .generated.GrammarDSLParser import GrammarDSLParser
from .visitor.ast_builder import ASTBuilder


class ParserService:
    def __init__(self) -> None:
        self.builder = ASTBuilder()

    def parse(self, text: str):
        input_stream = InputStream(text.strip())
        error_listener = ThrowingErrorListener()

        lexer = GrammarDSLLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)

        token_stream = CommonTokenStream(lexer)
        parser = GrammarDSLParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        tree = parser.command()
        return self.builder.visit(tree)

