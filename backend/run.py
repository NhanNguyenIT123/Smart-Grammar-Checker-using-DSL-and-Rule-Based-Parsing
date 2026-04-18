from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

for candidate in (str(PROJECT_ROOT), str(BACKEND_SRC)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


def run_tests() -> int:
    return subprocess.call(
        [sys.executable, "-m", "unittest", "discover", "-s", "backend/tests"],
        cwd=PROJECT_ROOT,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="GrammarDSL project runner.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("gen", help="Generate ANTLR lexer/parser/listener/visitor.")
    subparsers.add_parser("bootstrap-starter", help="Import the bundled starter vendor batch and compile the knowledge base.")
    subparsers.add_parser("compile", help="Compile raw knowledge sources into runtime artifacts.")
    subparsers.add_parser("report", help="Print the latest preprocessing pipeline report.")
    subparsers.add_parser("smoke", help="Run sample DSL commands.")
    subparsers.add_parser("test", help="Run backend unit tests.")
    import_scowl_parser = subparsers.add_parser("import-scowl", help="Import a SCOWL word list into preprocessing/raw/imported.")
    import_scowl_parser.add_argument("--input", required=True)

    import_oewn_parser = subparsers.add_parser("import-oewn", help="Import an Open English WordNet export into preprocessing/raw/imported.")
    import_oewn_parser.add_argument("--input", required=True)

    import_cefr_parser = subparsers.add_parser("import-cefr", help="Import a Cambridge CEFR vocabulary export into preprocessing/raw/imported.")
    import_cefr_parser.add_argument("--input", required=True)
    import_cefr_parser.add_argument("--level", help="Required for plain-text imports. Example: A2 or B1.")

    import_collocations_parser = subparsers.add_parser("import-collocations", help="Import a collocation export into preprocessing/raw/imported.")
    import_collocations_parser.add_argument("--input", required=True)

    serve_parser = subparsers.add_parser("serve", help="Start the backend HTTP server.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)

    exec_parser = subparsers.add_parser("exec", help="Execute a single DSL command.")
    exec_parser.add_argument("input", nargs="+")

    args = parser.parse_args()

    if args.command == "gen":
        from scripts.generate_antlr import generate_antlr

        generate_antlr()
        return 0

    if args.command == "bootstrap-starter":
        from scripts.bootstrap_starter_knowledge import bootstrap_starter_knowledge

        result = bootstrap_starter_knowledge()
        summary = result["pipeline_summary"]
        print(
            f'Starter batch imported and compiled to pipeline v{summary["pipeline_version"]} '
            f'with {summary["knowledge_stats"]["dictionary_entries"]} dictionary entries.'
        )
        return 0

    if args.command == "compile":
        from grammar_dsl.preprocessing import compile_knowledge_base

        knowledge_base = compile_knowledge_base(write_legacy=True)
        summary = knowledge_base["pipeline_summary"]
        print(
            f'Compiled knowledge base v{summary["pipeline_version"]} '
            f'with {summary["knowledge_stats"]["dictionary_entries"]} dictionary entries.'
        )
        return 0

    if args.command == "report":
        from grammar_dsl.preprocessing import load_pipeline_report

        print(json.dumps(load_pipeline_report(), indent=2))
        return 0

    if args.command == "import-scowl":
        from grammar_dsl.preprocessing.importers import import_scowl_pack

        payload = import_scowl_pack(Path(args.input))
        print(json.dumps(payload["metadata"], indent=2))
        return 0

    if args.command == "import-oewn":
        from grammar_dsl.preprocessing.importers import import_open_english_wordnet_pack

        payload = import_open_english_wordnet_pack(Path(args.input))
        print(json.dumps(payload["metadata"], indent=2))
        return 0

    if args.command == "import-cefr":
        from grammar_dsl.preprocessing.importers import import_cambridge_cefr_pack

        payload = import_cambridge_cefr_pack(Path(args.input), level=args.level)
        print(json.dumps(payload["metadata"], indent=2))
        return 0

    if args.command == "import-collocations":
        from grammar_dsl.preprocessing.importers import import_collocation_pack

        payload = import_collocation_pack(Path(args.input))
        print(json.dumps(payload["metadata"], indent=2))
        return 0

    if args.command == "smoke":
        from scripts.smoke_test import run_smoke_test

        return run_smoke_test()

    if args.command == "test":
        return run_tests()

    if args.command == "serve":
        from grammar_dsl.main import run_server

        run_server(host=args.host, port=args.port)
        return 0

    if args.command == "exec":
        from grammar_dsl.main import execute_input

        response = execute_input(" ".join(args.input))
        print(json.dumps(asdict(response), indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
