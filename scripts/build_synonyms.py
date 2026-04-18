from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.preprocessing.compiler import compile_knowledge_base  # noqa: E402


def main() -> None:
    knowledge_base = compile_knowledge_base(write_legacy=True)
    print(f'Wrote {len(knowledge_base["synonyms"])} synonym entries via the knowledge compiler.')


if __name__ == "__main__":
    main()
