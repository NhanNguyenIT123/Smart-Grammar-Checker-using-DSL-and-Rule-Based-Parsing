from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .common import (
    build_metadata,
    normalize_term,
    normalize_word,
    read_json,
    read_text,
    unique_sorted,
    write_import_pack,
)


def import_open_english_wordnet_pack(input_path: Path, output_dir: Path | None = None) -> dict[str, Any]:
    synonym_groups, semantic_classes = _load_oewn_source(input_path)
    normalized_groups = _normalize_groups(synonym_groups)
    normalized_semantic_classes = _normalize_semantic_classes(semantic_classes)

    dictionary_words = set()
    for group in normalized_groups:
        dictionary_words.update(group)
    for words in normalized_semantic_classes.values():
        dictionary_words.update(words)

    payload = {
        "metadata": build_metadata(
            source_id="src-open-english-wordnet-imported",
            source_type="lexicon",
            origin="open-english-wordnet",
            description="Imported synonym and semantic-class candidates normalized from an Open English WordNet export.",
            license_note="Check the downloaded OEWN package metadata before redistribution.",
            source_files=[input_path.name],
            record_count=len(normalized_groups),
        ),
        "synonym_groups": normalized_groups,
        "semantic_classes": normalized_semantic_classes,
        "dictionary_words": unique_sorted(dictionary_words),
    }
    write_import_pack("oewn_pack.json", payload, output_dir=output_dir)
    return payload


def _load_oewn_source(input_path: Path) -> tuple[list[list[str]], dict[str, list[str]]]:
    suffix = input_path.suffix.lower()
    if suffix == ".json":
        return _load_oewn_json(input_path)
    return _load_oewn_delimited(input_path)


def _load_oewn_json(input_path: Path) -> tuple[list[list[str]], dict[str, list[str]]]:
    payload = read_json(input_path)
    synonym_groups: list[list[str]] = []
    semantic_classes: dict[str, list[str]] = {}

    if isinstance(payload, dict):
        if "synonym_groups" in payload:
            synonym_groups.extend(payload.get("synonym_groups", []))
        if "semantic_classes" in payload:
            semantic_classes.update(payload.get("semantic_classes", {}))
        for entry in payload.get("entries", []):
            lemma = entry.get("lemma")
            synonyms = entry.get("synonyms", [])
            semantic_class = entry.get("semantic_class")
            row = [lemma, *synonyms]
            synonym_groups.append([item for item in row if item])
            if semantic_class and lemma:
                semantic_classes.setdefault(str(semantic_class), []).append(str(lemma))
    elif isinstance(payload, list):
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            lemma = entry.get("lemma")
            synonyms = entry.get("synonyms", [])
            semantic_class = entry.get("semantic_class")
            row = [lemma, *synonyms]
            synonym_groups.append([item for item in row if item])
            if semantic_class and lemma:
                semantic_classes.setdefault(str(semantic_class), []).append(str(lemma))

    return synonym_groups, semantic_classes


def _load_oewn_delimited(input_path: Path) -> tuple[list[list[str]], dict[str, list[str]]]:
    synonym_groups: list[list[str]] = []
    semantic_classes: dict[str, list[str]] = {}
    lines = read_text(input_path).splitlines()
    delimiter = "\t" if any("\t" in line for line in lines[:5]) else ","
    reader = csv.DictReader(lines, delimiter=delimiter)

    if reader.fieldnames:
        for row in reader:
            lemma = row.get("lemma") or row.get("word") or row.get("headword")
            synonyms = row.get("synonyms") or row.get("group") or ""
            semantic_class = row.get("semantic_class") or row.get("class") or row.get("lexname")
            group = [lemma, *_split_synonyms(synonyms)]
            synonym_groups.append([item for item in group if item])
            if semantic_class and lemma:
                semantic_classes.setdefault(str(semantic_class), []).append(str(lemma))
        return synonym_groups, semantic_classes

    for line in lines:
        parts = [part.strip() for part in line.split(delimiter)]
        if len(parts) < 2:
            continue
        lemma = parts[0]
        synonyms = _split_synonyms(parts[1])
        semantic_class = parts[2] if len(parts) > 2 else None
        synonym_groups.append([item for item in [lemma, *synonyms] if item])
        if semantic_class and lemma:
            semantic_classes.setdefault(str(semantic_class), []).append(str(lemma))

    return synonym_groups, semantic_classes


def _split_synonyms(raw: str) -> list[str]:
    for separator in ("|", ";", ","):
        if separator in raw:
            return [item.strip() for item in raw.split(separator) if item.strip()]
    return [raw.strip()] if raw.strip() else []


def _normalize_groups(groups: list[list[str]]) -> list[list[str]]:
    normalized: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    for group in groups:
        tokens = unique_sorted(
            token
            for raw in group
            if isinstance(raw, str)
            for token in [normalize_word(raw)]
            if token
        )
        if len(tokens) < 2:
            continue
        key = tuple(tokens)
        if key in seen:
            continue
        seen.add(key)
        normalized.append(tokens)
    return normalized


def _normalize_semantic_classes(classes: dict[str, list[str]]) -> dict[str, list[str]]:
    normalized: dict[str, list[str]] = {}
    for raw_category, words in classes.items():
        category = normalize_term(str(raw_category), allow_spaces=False)
        if not category:
            continue
        normalized_words = unique_sorted(
            token
            for raw_word in words
            if isinstance(raw_word, str)
            for token in [normalize_word(raw_word)]
            if token
        )
        if normalized_words:
            normalized[category] = normalized_words
    return dict(sorted(normalized.items()))
