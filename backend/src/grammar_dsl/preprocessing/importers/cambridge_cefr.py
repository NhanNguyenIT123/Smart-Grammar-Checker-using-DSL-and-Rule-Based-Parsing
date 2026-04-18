from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from .common import (
    build_metadata,
    load_existing_import,
    normalize_term,
    normalize_word,
    read_json,
    read_text,
    split_compound_terms,
    unique_sorted,
    write_import_pack,
)


LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2"}
POS_LINE_RE = re.compile(r"^(?P<lemma>[A-Za-z][A-Za-z' /-]*?)\s*\((?:[^)]*)\)\s*$")


def import_cambridge_cefr_pack(
    input_path: Path,
    level: str | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    imported = _load_cambridge_source(input_path, level)
    existing = load_existing_import("cambridge_cefr_pack.json", output_dir=output_dir)
    merged_levels = _merge_levels(existing.get("levels", {}), imported)

    dictionary_words = set()
    for terms in merged_levels.values():
        for term in terms:
            token = normalize_word(term)
            if token:
                dictionary_words.add(token)

    payload = {
        "metadata": build_metadata(
            source_id="src-cambridge-cefr-imported",
            source_type="lexicon",
            origin="cambridge-cefr",
            description="Imported learner-vocabulary lists normalized from Cambridge CEFR-aligned materials.",
            license_note="Keep the original Cambridge files in the vendor drop and review license terms before redistribution.",
            source_files=sorted({*existing.get("metadata", {}).get("source_files", []), input_path.name}),
            record_count=sum(len(terms) for terms in merged_levels.values()),
        ),
        "levels": merged_levels,
        "dictionary_words": unique_sorted(dictionary_words),
    }
    write_import_pack("cambridge_cefr_pack.json", payload, output_dir=output_dir)
    return payload


def _load_cambridge_source(input_path: Path, level: str | None) -> dict[str, list[str]]:
    suffix = input_path.suffix.lower()
    if suffix == ".json":
        return _normalize_level_map(_load_cambridge_json(input_path, level))
    if suffix in {".csv", ".tsv"}:
        return _normalize_level_map(_load_cambridge_table(input_path, level))
    if not level:
        raise ValueError("A CEFR level such as A2 or B1 is required when importing from a plain-text file.")
    return {level.upper(): _extract_terms_from_text(read_text(input_path))}


def _load_cambridge_json(input_path: Path, level: str | None) -> dict[str, list[str]]:
    payload = read_json(input_path)
    if isinstance(payload, dict):
        if "levels" in payload:
            return {str(key): list(value) for key, value in payload["levels"].items()}
        if level:
            items = payload.get("terms") or payload.get("words") or payload.get("entries") or []
            return {level.upper(): list(items)}
    raise ValueError("Unsupported Cambridge CEFR JSON format. Use {'levels': {'A2': [...]}} or provide --level with {'terms': [...]} data.")


def _load_cambridge_table(input_path: Path, level: str | None) -> dict[str, list[str]]:
    delimiter = "\t" if input_path.suffix.lower() == ".tsv" else ","
    rows = list(csv.DictReader(read_text(input_path).splitlines(), delimiter=delimiter))
    if not rows:
        return {}

    grouped: dict[str, list[str]] = {}
    for row in rows:
        raw_level = (row.get("level") or level or "").upper()
        if raw_level not in LEVELS:
            continue
        term = row.get("term") or row.get("word") or row.get("entry")
        if not term:
            continue
        grouped.setdefault(raw_level, []).append(term)
    return grouped


def _extract_terms_from_text(text: str) -> list[str]:
    terms: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or _should_skip_text_line(line):
            continue

        match = POS_LINE_RE.match(line)
        candidate = match.group("lemma") if match else line
        for part in split_compound_terms(candidate):
            normalized = normalize_term(part)
            if normalized and len(normalized.split()) <= 3:
                terms.append(normalized)
    return unique_sorted(terms)


def _should_skip_text_line(line: str) -> bool:
    if line.startswith(("©", "•", "_")):
        return True
    if line in LEVELS or len(line) == 1:
        return True
    if line.lower().startswith(("page ", "introduction", "summary of points", "vocabulary list", "background to the list")):
        return True
    if sum(character.isdigit() for character in line) > 3:
        return True
    if ":" in line or "." in line:
        return True
    if len(line.split()) > 6:
        return True
    return False


def _normalize_level_map(raw_levels: dict[str, list[str]]) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {}
    for raw_level, terms in raw_levels.items():
        level = str(raw_level).upper()
        if level not in LEVELS:
            continue
        cleaned_terms: list[str] = []
        for term in terms:
            if not isinstance(term, str):
                continue
            for part in split_compound_terms(term):
                normalized_term = normalize_term(part)
                if normalized_term and len(normalized_term.split()) <= 3:
                    cleaned_terms.append(normalized_term)
        normalized[level] = unique_sorted(cleaned_terms)
    return dict(sorted((level, terms) for level, terms in normalized.items() if terms))


def _merge_levels(existing: dict[str, list[str]], incoming: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {str(level).upper(): list(terms) for level, terms in existing.items()}
    for level, terms in incoming.items():
        merged[level] = unique_sorted([*merged.get(level, []), *terms])
    return dict(sorted((level, terms) for level, terms in merged.items() if terms))
