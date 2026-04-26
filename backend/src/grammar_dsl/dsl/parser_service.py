from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream

from .exceptions import DSLParseError
from .error_listener import ThrowingErrorListener
from .generated.GrammarDSLLexer import GrammarDSLLexer
from .generated.GrammarDSLParser import GrammarDSLParser
from .visitor.ast_builder import ASTBuilder


class ParserService:
    def __init__(self) -> None:
        self.builder = ASTBuilder()

    def tokenize(self, text: str) -> list[dict]:
        lexer = self._build_lexer(text)
        stream = CommonTokenStream(lexer)
        stream.fill()

        symbolic_names = getattr(lexer, "symbolicNames", [])
        tokens: list[dict] = []
        for raw_token in stream.tokens:
            if raw_token.type == -1:
                continue

            token_name = (
                symbolic_names[raw_token.type]
                if 0 <= raw_token.type < len(symbolic_names)
                else str(raw_token.type)
            )
            tokens.append(
                {
                    "index": len(tokens),
                    "type": token_name,
                    "lexeme": raw_token.text,
                    "line": raw_token.line,
                    "column": raw_token.column,
                }
            )
        return tokens

    def inspect(self, text: str) -> dict:
        tokens = self.tokenize(text)
        inspection = {
            "source_text": text.strip(),
            "tokens": tokens,
            "token_count": len(tokens),
            "parsable": False,
            "command_type": None,
            "parse_error": None,
        }

        try:
            node = self.parse(text)
            inspection["parsable"] = True
            inspection["command_type"] = type(node).__name__
        except DSLParseError as error:
            inspection["parse_error"] = str(error)

        return inspection

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

    @staticmethod
    def _build_lexer(text: str) -> GrammarDSLLexer:
        input_stream = InputStream(text.strip())
        error_listener = ThrowingErrorListener()
        lexer = GrammarDSLLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        return lexer

