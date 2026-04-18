from antlr4.error.ErrorListener import ErrorListener

from .exceptions import DSLParseError


class ThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # type: ignore[override]
        raise DSLParseError(f"line {line}:{column} {msg}")

