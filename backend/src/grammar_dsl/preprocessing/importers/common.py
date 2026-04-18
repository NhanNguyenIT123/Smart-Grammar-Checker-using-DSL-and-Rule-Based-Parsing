from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


RAW_DIR = Path(__file__).resolve().parents[1] / "raw"
IMPORTED_DIR = RAW_DIR / "imported"

WORD_RE = re.compile(r"^[a-z][a-z' -]*[a-z]$|^[a-z]$")


def ensure_imported_dir(output_dir: Path | None = None) -> Path:
    target = output_dir or IMPORTED_DIR
    target.mkdir(parents=True, exist_ok=True)
    return target


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def normalize_term(raw: str, allow_spaces: bool = True) -> str | None:
    text = raw.strip().lower()
    text = text.replace("’", "'").replace("–", "-").replace("—", "-")
    text = text.strip(".,;:!?()[]{}\"")
    text = re.sub(r"\s+", " ", text)
    if not text:
        return None
    if not allow_spaces and " " in text:
        return None
    if not WORD_RE.fullmatch(text):
        return None
    return text


def normalize_word(raw: str) -> str | None:
    return normalize_term(raw, allow_spaces=False)


def unique_sorted(values: list[str] | set[str]) -> list[str]:
    return sorted({value for value in values if value})


def split_compound_terms(raw: str) -> list[str]:
    parts = [segment.strip() for segment in raw.split("/") if segment.strip()]
    if len(parts) <= 1:
        return [raw]
    return parts


def build_metadata(
    *,
    source_id: str,
    source_type: str,
    origin: str,
    description: str,
    license_note: str,
    source_files: list[str],
    record_count: int,
) -> dict[str, Any]:
    return {
        "id": source_id,
        "type": source_type,
        "origin": origin,
        "description": description,
        "license": license_note,
        "source_files": source_files,
        "record_count": record_count,
    }


def load_existing_import(filename: str, output_dir: Path | None = None) -> dict[str, Any]:
    path = (output_dir or IMPORTED_DIR) / filename
    if not path.exists():
        return {}
    return read_json(path)


def write_import_pack(filename: str, payload: dict[str, Any], output_dir: Path | None = None) -> Path:
    target_dir = ensure_imported_dir(output_dir)
    path = target_dir / filename
    write_json(path, payload)
    return path
