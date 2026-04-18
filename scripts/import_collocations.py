from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

for candidate in (str(PROJECT_ROOT), str(BACKEND_SRC)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import a collocation export into preprocessing/raw/imported.")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    from grammar_dsl.preprocessing.importers import import_collocation_pack

    payload = import_collocation_pack(Path(args.input))
    print(json.dumps(payload["metadata"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
