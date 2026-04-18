from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_FILE = PROJECT_ROOT / "backend" / "src" / "grammar_dsl" / "dsl" / "grammar" / "GrammarDSL.g4"
OUTPUT_DIR = PROJECT_ROOT / "backend" / "src" / "grammar_dsl" / "dsl" / "generated"


def locate_antlr_jar() -> Path:
    candidates = [
        os.environ.get("ANTLR4_JAR"),
        os.environ.get("ANTLR_JAR"),
        str(Path.home() / "Downloads" / "antlr4-4.9.2-complete.jar"),
        str(Path.home() / ".m2" / "repository" / "org" / "antlr" / "antlr4" / "4.9.2" / "antlr4-4.9.2-complete.jar"),
        str(Path.home() / ".m2" / "repository" / "org" / "antlr" / "antlr4" / "4.13.2" / "antlr4-4.13.2-complete.jar")
    ]

    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        if path.exists():
            return path

    raise FileNotFoundError("Could not locate an ANTLR jar. Set ANTLR4_JAR or ANTLR_JAR.")


def clean_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_antlr() -> None:
    jar_path = locate_antlr_jar()
    clean_output_dir()

    command = [
        "java",
        "-jar",
        str(jar_path),
        "-Dlanguage=Python3",
        "-visitor",
        "-Xexact-output-dir",
        "-o",
        str(OUTPUT_DIR),
        str(GRAMMAR_FILE)
    ]

    print(f"Using ANTLR jar: {jar_path}")
    subprocess.run(command, check=True, cwd=PROJECT_ROOT)
    print("Generated parser artifacts:")
    for path in sorted(OUTPUT_DIR.iterdir()):
        print(f" - {path.name}")


if __name__ == "__main__":
    try:
        generate_antlr()
    except Exception as error:
        print(f"Generation failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
