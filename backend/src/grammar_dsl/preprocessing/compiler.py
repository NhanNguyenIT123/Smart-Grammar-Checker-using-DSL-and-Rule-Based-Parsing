from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .source_packs import (
    BASE_SOURCE_MANIFEST,
    DOUBLING_EXCEPTIONS,
    EXERCISE_BLUEPRINTS,
    FEATURE_CATALOG,
    IMPORTED_CEFR_LEVELS,
    IMPORTED_UNLIKELY_PHRASES,
    IRREGULAR_VERBS,
    LEXICAL_POOLS,
    PIPELINE_STEPS,
    PIPELINE_VERSION,
    PROJECT_WORDS,
    RAW_SOURCE_MANIFEST,
    REALIZATION_RULES,
    REGULAR_VERBS,
    SEMANTIC_CLASSES,
    SYNONYM_GROUPS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "backend" / "src" / "grammar_dsl" / "data"
COMPILED_DIR = DATA_DIR / "compiled"
KNOWLEDGE_BASE_PATH = COMPILED_DIR / "knowledge_base.json"
PHRASE_INDEX_PATH = COMPILED_DIR / "phrase_index.json"
PIPELINE_REPORT_PATH = COMPILED_DIR / "pipeline_report.json"
SOURCE_MANIFEST_PATH = COMPILED_DIR / "source_manifest.json"
EXERCISE_BLUEPRINTS_PATH = COMPILED_DIR / "exercise_blueprints.json"
LEXICAL_POOLS_PATH = COMPILED_DIR / "lexical_pools.json"
REALIZATION_RULES_PATH = COMPILED_DIR / "realization_rules.json"
FEATURE_CATALOG_PATH = COMPILED_DIR / "feature_catalog.json"
GRAMMAR_RULES_PATH = DATA_DIR / "grammar_rules.json"
LEGACY_VERBS_PATH = DATA_DIR / "verbs.json"
LEGACY_SYNONYMS_PATH = DATA_DIR / "synonyms.json"
LEGACY_DICTIONARY_PATH = DATA_DIR / "dictionary.json"

WORD_LIMIT = 12000
BLOCKLIST = {
    "ain",
    "gonna",
    "kinda",
    "lol",
    "omg",
    "wanna",
    "wtf",
}


def compile_knowledge_base(write_legacy: bool = True) -> dict[str, Any]:
    grammar_rules = _merge_imported_rulepacks(_load_json(GRAMMAR_RULES_PATH))
    verbs = _build_verbs()
    synonyms = _build_synonyms()
    phrase_index = _build_phrase_index(grammar_rules)
    dictionary = _build_dictionary(verbs, synonyms, grammar_rules, phrase_index)

    pipeline_summary = {
        "pipeline_version": PIPELINE_VERSION,
        "compiled_at": datetime.now(timezone.utc).isoformat(),
        "preprocessing_steps": PIPELINE_STEPS,
        "sources": RAW_SOURCE_MANIFEST,
        "artifacts": [
            "knowledge_base.json",
            "phrase_index.json",
            "pipeline_report.json",
            "source_manifest.json",
            "exercise_blueprints.json",
            "lexical_pools.json",
            "realization_rules.json",
            "feature_catalog.json",
        ],
        "knowledge_stats": {
            "verb_entries": len(verbs),
            "synonym_entries": len(synonyms),
            "dictionary_entries": len(dictionary),
            "grammar_rules": len(phrase_index),
            "semantic_classes": len(SEMANTIC_CLASSES),
            "phrase_index_entries": len(phrase_index),
            "coverage_entries": len(grammar_rules.get("coverage_matrix", [])),
            "cefr_entries": sum(len(words) for words in IMPORTED_CEFR_LEVELS.values()),
            "imported_sources": max(0, len(RAW_SOURCE_MANIFEST) - len(BASE_SOURCE_MANIFEST)),
            "imported_collocation_rules": len(IMPORTED_UNLIKELY_PHRASES),
            "exercise_blueprints": len(EXERCISE_BLUEPRINTS),
            "feature_atoms": len(FEATURE_CATALOG),
        },
    }

    knowledge_base = {
        "metadata": {
            "name": "GrammarDSL Compiled Knowledge Base",
            "pipeline_version": PIPELINE_VERSION,
            "compiled_at": pipeline_summary["compiled_at"],
        },
        "verbs": verbs,
        "synonyms": synonyms,
        "dictionary": dictionary,
        "grammar_rules": grammar_rules,
        "semantic_classes": SEMANTIC_CLASSES,
        "cefr_vocabulary": IMPORTED_CEFR_LEVELS,
        "phrase_index": phrase_index,
        "feature_catalog": FEATURE_CATALOG,
        "exercise_blueprints": EXERCISE_BLUEPRINTS,
        "lexical_pools": LEXICAL_POOLS,
        "realization_rules": REALIZATION_RULES,
        "pipeline_summary": pipeline_summary,
        "source_manifest": RAW_SOURCE_MANIFEST,
    }

    _ensure_compiled_dir()
    _write_json(KNOWLEDGE_BASE_PATH, knowledge_base)
    _write_json(PHRASE_INDEX_PATH, phrase_index)
    _write_json(PIPELINE_REPORT_PATH, pipeline_summary)
    _write_json(SOURCE_MANIFEST_PATH, RAW_SOURCE_MANIFEST)
    _write_json(EXERCISE_BLUEPRINTS_PATH, EXERCISE_BLUEPRINTS)
    _write_json(LEXICAL_POOLS_PATH, LEXICAL_POOLS)
    _write_json(REALIZATION_RULES_PATH, REALIZATION_RULES)
    _write_json(FEATURE_CATALOG_PATH, FEATURE_CATALOG)

    if write_legacy:
        _write_json(LEGACY_VERBS_PATH, verbs)
        _write_json(LEGACY_SYNONYMS_PATH, synonyms)
        _write_json(LEGACY_DICTIONARY_PATH, dictionary)

    return knowledge_base


def load_pipeline_report() -> dict[str, Any]:
    if PIPELINE_REPORT_PATH.exists():
        return _load_json(PIPELINE_REPORT_PATH)

    if KNOWLEDGE_BASE_PATH.exists():
        return _load_json(KNOWLEDGE_BASE_PATH).get("pipeline_summary", {})

    return compile_knowledge_base(write_legacy=False).get("pipeline_summary", {})


def _build_verbs() -> dict[str, list[str]]:
    verbs = {base.lower(): [item.lower() for item in forms] for base, forms in IRREGULAR_VERBS.items()}
    for base in REGULAR_VERBS:
        normalized = base.strip().lower()
        if not normalized or normalized in verbs:
            continue
        verbs[normalized] = _regular_forms(normalized)
    return dict(sorted(verbs.items()))


def _merge_imported_rulepacks(grammar_rules: dict[str, Any]) -> dict[str, Any]:
    merged_rules = json.loads(json.dumps(grammar_rules))
    semantic_patterns = merged_rules.setdefault("semantic_patterns", {})
    existing_phrases = semantic_patterns.setdefault("unlikely_phrases", [])

    seen_phrases = {
        str(item.get("phrase", "")).strip().lower()
        for item in existing_phrases
        if isinstance(item, dict)
    }
    for rule in IMPORTED_UNLIKELY_PHRASES:
        phrase = str(rule.get("phrase", "")).strip().lower()
        if not phrase or phrase in seen_phrases:
            continue
        seen_phrases.add(phrase)
        existing_phrases.append(rule)

    return merged_rules


def _build_synonyms() -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for group in SYNONYM_GROUPS:
        normalized_group = [word.lower() for word in group]
        for word in normalized_group:
            mapping[word] = [candidate for candidate in normalized_group if candidate != word]
    return dict(sorted(mapping.items()))


def _build_phrase_index(grammar_rules: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    for tense_name, expressions in grammar_rules.get("time_expressions", {}).items():
        for expression in expressions:
            entries.append(
                {
                    "category": "time_expression",
                    "label": tense_name,
                    "phrase": expression,
                    "token_count": len(_split_phrase(expression)),
                }
            )

    for rule in grammar_rules.get("semantic_patterns", {}).get("unlikely_phrases", []):
        phrase = str(rule.get("phrase", "")).strip()
        if phrase:
            entries.append(
                {
                    "category": "semantic_phrase",
                    "label": "unlikely_phrase",
                    "phrase": phrase,
                    "token_count": len(_split_phrase(phrase)),
                }
            )

    for key, rule in grammar_rules.get("semantic_patterns", {}).get("verb_destination_expectations", {}).items():
        trigger = " ".join(rule.get("trigger", []))
        if trigger:
            entries.append(
                {
                    "category": "semantic_trigger",
                    "label": key,
                    "phrase": trigger,
                    "token_count": len(_split_phrase(trigger)),
                }
            )

    for key, rule in grammar_rules.get("semantic_patterns", {}).get("verb_object_expectations", {}).items():
        trigger = " ".join(rule.get("trigger", []))
        if trigger:
            entries.append(
                {
                    "category": "semantic_trigger",
                    "label": key,
                    "phrase": trigger,
                    "token_count": len(_split_phrase(trigger)),
                }
            )

    unique_entries = {f"{item['category']}::{item['label']}::{item['phrase']}": item for item in entries}
    return sorted(unique_entries.values(), key=lambda item: (-item["token_count"], item["category"], item["phrase"]))


def _build_dictionary(
    verbs: dict[str, list[str]],
    synonyms: dict[str, list[str]],
    grammar_rules: dict[str, Any],
    phrase_index: list[dict[str, Any]],
) -> list[str]:
    base_words = _load_common_words()
    merged = set(base_words)
    merged.update(PROJECT_WORDS)
    merged.update(_collect_strings(verbs))
    merged.update(_collect_strings(synonyms))
    merged.update(_collect_strings(grammar_rules))
    merged.update(_collect_strings(SEMANTIC_CLASSES))
    merged.update(_collect_strings(phrase_index))
    merged.update(_collect_strings(FEATURE_CATALOG))
    merged.update(_collect_strings(EXERCISE_BLUEPRINTS))
    merged.update(_collect_strings(LEXICAL_POOLS))
    merged.update(_collect_strings(REALIZATION_RULES))
    merged.update(
        {
            "check",
            "grammar",
            "generate",
            "exercise",
            "exercises",
            "create",
            "quiz",
            "submit",
            "answers",
            "show",
            "students",
            "with",
            "and",
            "or",
            "for",
            "score",
            "submitted",
            "passed",
            "failed",
            "history",
            "revision",
            "plan",
            "reset",
            "verb",
            "spell",
            "synonym",
            "help",
        }
    )
    return sorted(word for word in merged if word)


def _load_common_words() -> set[str]:
    try:
        from wordfreq import top_n_list  # type: ignore

        return {
            word.lower()
            for word in top_n_list("en", WORD_LIMIT)
            if word.isalpha() and len(word) > 1 and word.lower() not in BLOCKLIST
        }
    except Exception:
        if LEGACY_DICTIONARY_PATH.exists():
            return {word.lower() for word in _load_json(LEGACY_DICTIONARY_PATH)}
        return set()


def _regular_forms(base: str) -> list[str]:
    if base.endswith("y") and len(base) > 1 and base[-2] not in "aeiou":
        past = f"{base[:-1]}ied"
    elif base.endswith("e"):
        past = f"{base}d"
    elif _should_double_final_consonant(base):
        past = f"{base}{base[-1]}ed"
    else:
        past = f"{base}ed"
    return [base, past, past]


def _should_double_final_consonant(base: str) -> bool:
    normalized = base.lower()
    if normalized in DOUBLING_EXCEPTIONS:
        return True
    return len(normalized) <= 4 and _is_short_cvc(normalized)


def _is_short_cvc(word: str) -> bool:
    if len(word) < 3:
        return False
    vowels = "aeiou"
    return (
        word[-1] not in vowels
        and word[-1] not in {"w", "x", "y"}
        and word[-2] in vowels
        and word[-3] not in vowels
    )


def _collect_strings(value: Any) -> set[str]:
    results: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            results.update(_split_phrase(str(key)))
            results.update(_collect_strings(item))
        return results

    if isinstance(value, list):
        for item in value:
            results.update(_collect_strings(item))
        return results

    if isinstance(value, str):
        results.update(_split_phrase(value))
    return results


def _split_phrase(text: str) -> set[str]:
    return {
        token.lower()
        for token in (
            text.replace(",", " ")
            .replace('"', " ")
            .replace("/", " ")
            .replace("-", " ")
            .split()
        )
        if token.isalpha()
    }


def _ensure_compiled_dir() -> None:
    COMPILED_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
