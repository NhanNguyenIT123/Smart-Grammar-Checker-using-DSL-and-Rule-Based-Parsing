from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.services import CommandService  # noqa: E402


def run_smoke_test() -> int:
    service = CommandService()
    samples = [
        "help",
        "spell generte",
        "spell generate",
        "verb know",
        "synonym smart",
        "explain grammar He go to school every day.",
        "check grammar I go to chracter yesterday.",
        "check grammar He go to school every day.",
        "check grammar However I am writing the parser now.",
        "revision plan",
        "history",
    ]

    for sample in samples:
        print("=" * 72)
        print(sample)
        response = service.execute(sample)
        print(json.dumps(asdict(response), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(run_smoke_test())
