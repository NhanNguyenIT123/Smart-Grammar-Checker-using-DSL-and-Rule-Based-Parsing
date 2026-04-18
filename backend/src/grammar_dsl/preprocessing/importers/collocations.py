from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .common import (
    build_metadata,
    normalize_term,
    read_json,
    read_text,
    unique_sorted,
    write_import_pack,
)

INFLECTABLE_VERBS = {"do", "give", "have", "make", "pay", "say", "take", "tell", "work"}


def import_collocation_pack(input_path: Path, output_dir: Path | None = None) -> dict[str, Any]:
    entries = _load_collocation_entries(input_path)
    normalized_entries = _normalize_collocation_entries(entries)

    dictionary_words = set()
    for entry in normalized_entries:
        dictionary_words.update(entry["phrase"].split())
        if entry.get("replacement"):
            dictionary_words.update(str(entry["replacement"]).split())

    payload = {
        "metadata": build_metadata(
            source_id="src-collocation-imported",
            source_type="rulepack",
            origin="collocation-export",
            description="Imported collocation corrections normalized into semantic warning rules.",
            license_note="Review the upstream corpus or collocation source terms before redistributing raw exports.",
            source_files=[input_path.name],
            record_count=len(normalized_entries),
        ),
        "unlikely_phrases": normalized_entries,
        "dictionary_words": unique_sorted(dictionary_words),
    }
    write_import_pack("collocation_pack.json", payload, output_dir=output_dir)
    return payload


def _load_collocation_entries(input_path: Path) -> list[dict[str, Any]]:
    suffix = input_path.suffix.lower()
    if suffix == ".json":
        payload = read_json(input_path)
        if isinstance(payload, dict):
            if "entries" in payload and isinstance(payload["entries"], list):
                return [item for item in payload["entries"] if isinstance(item, dict)]
            if "unlikely_phrases" in payload and isinstance(payload["unlikely_phrases"], list):
                return [item for item in payload["unlikely_phrases"] if isinstance(item, dict)]
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        return []

    delimiter = "\t" if suffix == ".tsv" else ","
    rows = list(csv.DictReader(read_text(input_path).splitlines(), delimiter=delimiter))
    if rows:
        return [dict(row) for row in rows]

    entries: list[dict[str, Any]] = []
    for raw_line in read_text(input_path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 2:
            continue
        entries.append(
            {
                "incorrect_phrase": parts[0],
                "preferred_phrase": parts[1],
                "message": parts[2] if len(parts) > 2 else "",
            }
        )
    return entries


def _normalize_collocation_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_entries: list[dict[str, Any]] = []
    seen_phrases: set[str] = set()

    for entry in entries:
        incorrect_phrase = normalize_term(
            str(
                entry.get("incorrect_phrase")
                or entry.get("phrase")
                or entry.get("incorrect")
                or entry.get("source_phrase")
                or ""
            )
        )
        preferred_phrase = normalize_term(
            str(
                entry.get("preferred_phrase")
                or entry.get("replacement")
                or entry.get("preferred")
                or entry.get("target_phrase")
                or ""
            )
        )

        if not incorrect_phrase or not preferred_phrase or incorrect_phrase == preferred_phrase:
            continue
        explicit_message = str(entry.get("message") or "").strip()
        message = explicit_message or (
            f'The collocation "{incorrect_phrase}" sounds unusual here. '
            f'English more commonly uses "{preferred_phrase}".'
        )

        source_label = str(entry.get("source_label") or entry.get("source") or "imported-collocation")
        for variant in _expand_entry_variants(
            incorrect_phrase=incorrect_phrase,
            preferred_phrase=preferred_phrase,
            message=message,
            source_label=source_label,
        ):
            if variant["phrase"] in seen_phrases:
                continue
            seen_phrases.add(variant["phrase"])
            normalized_entries.append(variant)

    return normalized_entries


def _expand_entry_variants(
    *,
    incorrect_phrase: str,
    preferred_phrase: str,
    message: str,
    source_label: str,
) -> list[dict[str, Any]]:
    variants = [
        {
            "phrase": incorrect_phrase,
            "message": message,
            "suggestion": f'Use "{preferred_phrase}" instead.',
            "replacement": preferred_phrase,
            "source_label": source_label,
        }
    ]

    incorrect_tokens = incorrect_phrase.split()
    preferred_tokens = preferred_phrase.split()
    if not incorrect_tokens or not preferred_tokens:
        return variants

    if incorrect_tokens[0] in INFLECTABLE_VERBS and preferred_tokens[0] in INFLECTABLE_VERBS:
        inflected_incorrect = " ".join([_third_person_singular(incorrect_tokens[0]), *incorrect_tokens[1:]])
        inflected_preferred = " ".join([_third_person_singular(preferred_tokens[0]), *preferred_tokens[1:]])
        variants.append(
            {
                "phrase": inflected_incorrect,
                "message": message.replace(f'"{incorrect_phrase}"', f'"{inflected_incorrect}"').replace(
                    f'"{preferred_phrase}"',
                    f'"{inflected_preferred}"',
                ),
                "suggestion": f'Use "{inflected_preferred}" instead.',
                "replacement": inflected_preferred,
                "source_label": source_label,
            }
        )

    return variants


def _third_person_singular(base: str) -> str:
    if base == "have":
        return "has"
    if base == "do":
        return "does"
    if base.endswith("y") and len(base) > 1 and base[-2] not in "aeiou":
        return f"{base[:-1]}ies"
    if base.endswith(("s", "sh", "ch", "x", "z", "o")):
        return f"{base}es"
    return f"{base}s"
