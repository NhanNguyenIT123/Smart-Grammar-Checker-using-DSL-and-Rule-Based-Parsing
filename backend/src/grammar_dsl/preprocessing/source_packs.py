from __future__ import annotations

import json
from pathlib import Path
from typing import Any


RAW_DIR = Path(__file__).resolve().parent / "raw"
IMPORTED_DIR = RAW_DIR / "imported"


def _load_raw_json(filename: str) -> Any:
    path = RAW_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _load_optional_import(filename: str) -> dict[str, Any]:
    path = IMPORTED_DIR / filename
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    return payload if isinstance(payload, dict) else {}


def _merge_semantic_classes(*mappings: dict[str, list[str]]) -> dict[str, list[str]]:
    merged: dict[str, set[str]] = {}
    for mapping in mappings:
        for key, values in mapping.items():
            merged.setdefault(str(key), set()).update(str(value).lower() for value in values)
    return {key: sorted(values) for key, values in sorted(merged.items())}


def _normalize_imported_groups(payload: dict[str, Any]) -> list[tuple[str, ...]]:
    groups: list[tuple[str, ...]] = []
    for group in payload.get("synonym_groups", []):
        if not isinstance(group, list):
            continue
        tokens = tuple(sorted({str(word).lower() for word in group if str(word).strip()}))
        if len(tokens) >= 2:
            groups.append(tokens)
    return groups


def _normalize_imported_dictionary_words(payload: dict[str, Any]) -> set[str]:
    return {str(word).lower() for word in payload.get("dictionary_words", []) if str(word).strip()}


def _normalize_imported_semantic_classes(payload: dict[str, Any]) -> dict[str, list[str]]:
    mapping = payload.get("semantic_classes", {})
    if not isinstance(mapping, dict):
        return {}
    normalized: dict[str, list[str]] = {}
    for key, values in mapping.items():
        if not isinstance(values, list):
            continue
        normalized[str(key).lower()] = [str(value).lower() for value in values if str(value).strip()]
    return normalized


def _normalize_imported_cefr(payload: dict[str, Any]) -> dict[str, list[str]]:
    levels = payload.get("levels", {})
    if not isinstance(levels, dict):
        return {}
    normalized: dict[str, list[str]] = {}
    for key, values in levels.items():
        if not isinstance(values, list):
            continue
        normalized[str(key).upper()] = sorted({str(value).lower() for value in values if str(value).strip()})
    return normalized


SCOWL_IMPORTED_PACK = _load_optional_import("scowl_pack.json")
OEWN_IMPORTED_PACK = _load_optional_import("oewn_pack.json")
CAMBRIDGE_CEFR_IMPORTED_PACK = _load_optional_import("cambridge_cefr_pack.json")
COLLOCATION_IMPORTED_PACK = _load_optional_import("collocation_pack.json")
IMPORTED_PACKS = [
    payload
    for payload in [
        SCOWL_IMPORTED_PACK,
        OEWN_IMPORTED_PACK,
        CAMBRIDGE_CEFR_IMPORTED_PACK,
        COLLOCATION_IMPORTED_PACK,
    ]
    if payload
]


PIPELINE_CONFIG = _load_raw_json("pipeline_config.json")
VERBS_SEED = _load_raw_json("verbs_seed.json")

PIPELINE_VERSION = str(PIPELINE_CONFIG["pipeline_version"])
PIPELINE_STEPS = [str(step) for step in PIPELINE_CONFIG["preprocessing_steps"]]
BASE_SOURCE_MANIFEST = list(_load_raw_json("source_manifest.json"))
RAW_SOURCE_MANIFEST = [
    *BASE_SOURCE_MANIFEST,
    *[payload["metadata"] for payload in IMPORTED_PACKS if isinstance(payload.get("metadata"), dict)],
]
IRREGULAR_VERBS = {
    str(base).lower(): [str(item).lower() for item in forms]
    for base, forms in VERBS_SEED["irregular_verbs"].items()
}
REGULAR_VERBS = [str(verb).lower() for verb in VERBS_SEED["regular_verbs"]]
DOUBLING_EXCEPTIONS = {str(verb).lower() for verb in VERBS_SEED["doubling_exceptions"]}
BASE_SYNONYM_GROUPS = [tuple(str(word).lower() for word in group) for group in _load_raw_json("synonym_groups.json")]
BASE_PROJECT_WORDS = {str(word).lower() for word in _load_raw_json("project_words.json")}
BASE_SEMANTIC_CLASSES = {
    str(category): [str(word).lower() for word in words]
    for category, words in _load_raw_json("semantic_classes.json").items()
}
IMPORTED_SYNONYM_GROUPS = [
    group
    for payload in IMPORTED_PACKS
    for group in _normalize_imported_groups(payload)
]
IMPORTED_DICTIONARY_WORDS = {
    word
    for payload in IMPORTED_PACKS
    for word in _normalize_imported_dictionary_words(payload)
}
IMPORTED_CEFR_LEVELS = {
    key: values
    for payload in IMPORTED_PACKS
    for key, values in _normalize_imported_cefr(payload).items()
}
IMPORTED_UNLIKELY_PHRASES = [
    item
    for item in COLLOCATION_IMPORTED_PACK.get("unlikely_phrases", [])
    if isinstance(item, dict) and item.get("phrase")
]

SYNONYM_GROUPS = [*BASE_SYNONYM_GROUPS, *IMPORTED_SYNONYM_GROUPS]
PROJECT_WORDS = BASE_PROJECT_WORDS | IMPORTED_DICTIONARY_WORDS
SEMANTIC_CLASSES = _merge_semantic_classes(
    BASE_SEMANTIC_CLASSES,
    *[_normalize_imported_semantic_classes(payload) for payload in IMPORTED_PACKS],
)
