from __future__ import annotations

from grammar_dsl.api import run_server
from grammar_dsl.engine.types import CommandResponse
from grammar_dsl.services import CommandService


def execute_input(text: str, user_id: str | None = None) -> CommandResponse:
    return CommandService().execute(text, user_id=user_id)


__all__ = ["execute_input", "run_server"]
