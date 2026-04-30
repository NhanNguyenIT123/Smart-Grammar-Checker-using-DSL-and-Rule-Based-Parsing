from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Any

from grammar_dsl.dsl.ast import AndExpr, FeatureExpr, OrExpr
from grammar_dsl.engine import VerbEngine


class ExerciseGenerator:
    DEFAULT_SENTENCE_FORM = "affirmative"
    SENTENCE_FORMS = {"affirmative", "negative", "interrogative"}
    TENSE_FEATURES = {
        "present simple",
        "past simple",
        "future simple",
        "present continuous",
    }

    def __init__(self, repository, verb_engine: VerbEngine) -> None:
        self.repository = repository
        self.verb_engine = verb_engine
        self.feature_catalog = {entry["id"]: entry for entry in repository.feature_catalog}
        self.blueprints = repository.exercise_blueprints or []
        self.lexical_pools = repository.lexical_pools or {}
        self.realization_rules = repository.realization_rules or {}

    def generate(
        self,
        feature_expr,
        requested_count: int | None = None,
        singular_form_requested: bool = False,
    ) -> dict[str, Any]:
        bundles = [self._normalize_bundle(bundle) for bundle in self._expand_feature_expr(feature_expr)]
        bundles = self._dedupe_bundles(bundles)
        requested_total = 1 if singular_form_requested or requested_count is None else requested_count

        feature_labels = sorted({feature for bundle in bundles for feature in bundle})
        feature_strings = [" AND ".join(sorted(bundle)) for bundle in bundles]

        if self._should_use_corpus_generator(bundles):
            from grammar_dsl.services.corpus_nlp import generate_exercises_with_corpus

            llm_items = generate_exercises_with_corpus(requested_total, feature_strings)
            items: list[dict[str, Any]] = []
            for idx, item in enumerate(llm_items, start=1):
                items.append(
                    {
                        "id": f"llm-{idx}",
                        "blueprint_id": "llm_generated",
                        "type": item.get("type", "fill blank"),
                        "difficulty": item.get("difficulty", "intermediate"),
                        "features": feature_labels,
                        "prompt": item.get("prompt", ""),
                        "expected_answer": item.get("expected_answer", ""),
                        "accepted_variants": item.get("accepted_variants", [item.get("expected_answer", "")]),
                        "answer_preview": item.get("expected_answer", ""),
                    }
                )
        else:
            selected = self._select_blueprints(bundles, requested_total)
            items = [self._realize_item(blueprint, index) for index, blueprint in enumerate(selected, start=1)]

        seed_text = "|".join(item["id"] for item in items)
        exercise_set_id = f"set-{hashlib.sha1(seed_text.encode('utf-8')).hexdigest()[:10]}"
        return {
            "exercise_set_id": exercise_set_id,
            "requested_count": requested_total,
            "items": items,
            "features": feature_labels,
            "feature_bundles": [sorted(bundle) for bundle in bundles],
        }

    def _expand_feature_expr(self, expr) -> list[set[str]]:
        if isinstance(expr, FeatureExpr):
            return [{expr.name}]
        if isinstance(expr, AndExpr):
            left = self._expand_feature_expr(expr.left)
            right = self._expand_feature_expr(expr.right)
            return [left_bundle | right_bundle for left_bundle in left for right_bundle in right]
        if isinstance(expr, OrExpr):
            return self._expand_feature_expr(expr.left) + self._expand_feature_expr(expr.right)
        raise ValueError("Unsupported feature expression.")

    def _normalize_bundle(self, bundle: set[str]) -> set[str]:
        normalized = {item.lower() for item in bundle if item}
        if normalized & self.TENSE_FEATURES and not (normalized & self.SENTENCE_FORMS):
            normalized.add(self.DEFAULT_SENTENCE_FORM)
        return normalized

    @staticmethod
    def _dedupe_bundles(bundles: list[set[str]]) -> list[set[str]]:
        seen: set[tuple[str, ...]] = set()
        unique: list[set[str]] = []
        for bundle in bundles:
            key = tuple(sorted(bundle))
            if key in seen:
                continue
            seen.add(key)
            unique.append(bundle)
        return unique

    def _should_use_corpus_generator(self, bundles: list[set[str]]) -> bool:
        for bundle in bundles:
            if not (bundle & self.TENSE_FEATURES):
                return False
            unsupported = bundle - self.TENSE_FEATURES - self.SENTENCE_FORMS
            if unsupported:
                return False
        return True

    def _select_blueprints(self, bundles: list[set[str]], requested_total: int) -> list[dict[str, Any]]:
        bundle_matches: list[list[dict[str, Any]]] = []
        for bundle in bundles:
            matches = [
                blueprint
                for blueprint in self.blueprints
                if set(blueprint.get("required_features", [])) <= bundle
            ]
            if not matches:
                continue
            matches.sort(key=lambda item: item["id"])
            bundle_matches.append(matches)

        if not bundle_matches:
            return []

        selected: list[dict[str, Any]] = []
        pointer = 0
        while len(selected) < requested_total:
            matches = bundle_matches[pointer % len(bundle_matches)]
            blueprint = matches[(len(selected) // len(bundle_matches)) % len(matches)]
            selected.append(blueprint)
            pointer += 1
        return selected

    def _realize_item(self, blueprint: dict[str, Any], item_number: int) -> dict[str, Any]:
        family = blueprint.get("family")
        if family == "tense-fill":
            payload = self._build_tense_fill(blueprint)
        elif family == "tense-transform":
            payload = self._build_tense_transform(blueprint)
        elif family == "agreement":
            payload = self._build_agreement_correction(blueprint)
        elif family == "object-pronoun":
            payload = self._build_object_pronoun_correction(blueprint)
        elif family == "verb-preposition":
            payload = self._build_verb_preposition_fill(blueprint)
        elif family == "svo":
            payload = self._build_svo_fill(blueprint)
        else:
            raise ValueError(f"Unsupported exercise family: {family}")

        payload.update(
            {
                "id": f"{blueprint['id']}-{item_number}",
                "blueprint_id": blueprint["id"],
                "type": blueprint.get("item_type", "prompt"),
                "difficulty": blueprint.get("difficulty", "starter"),
                "features": blueprint.get("required_features", []),
            }
        )
        return payload

    def _build_tense_fill(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        tense = self._pick_feature(blueprint, self.TENSE_FEATURES)
        subject = self._pick_subject(tense, blueprint)
        verb_base = self._pick_from_pool("transitive_verbs", blueprint)
        obj = self._pick_from_pool("objects", blueprint)
        time_marker = self._pick_time_marker(tense, blueprint)
        answer = self._affirmative_sentence(tense, subject, verb_base, obj, time_marker)
        expected = self._affirmative_verb_phrase(tense, subject, verb_base)
        prompt = self._fill_sentence_template(subject["surface"], "____", obj, time_marker)
        return {
            "prompt": f"Fill in the missing verb form: {prompt}",
            "expected_answer": expected,
            "accepted_variants": [expected],
            "answer_preview": answer,
        }

    def _build_tense_transform(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        features = set(blueprint.get("required_features", []))
        tense = self._pick_feature(blueprint, self.TENSE_FEATURES)
        subject = self._pick_subject(tense, blueprint)
        verb_base = self._pick_from_pool("transitive_verbs", blueprint)
        obj = self._pick_from_pool("objects", blueprint)
        time_marker = self._pick_time_marker(tense, blueprint)
        affirmative = self._affirmative_sentence(tense, subject, verb_base, obj, time_marker)

        if "negative" in features:
            accepted = self._negative_variants(tense, subject, verb_base, obj, time_marker)
            prompt = f"Rewrite this sentence in the negative form: {affirmative}"
        else:
            accepted = self._question_variants(tense, subject, verb_base, obj, time_marker)
            prompt = f"Rewrite this sentence as a question: {affirmative}"

        return {
            "prompt": prompt,
            "expected_answer": accepted[0],
            "accepted_variants": accepted,
            "answer_preview": accepted[0],
        }

    def _build_agreement_correction(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        agreement_nouns = self.lexical_pools.get("agreement_nouns", {})
        singular_subjects = agreement_nouns.get("singular", [])
        plural_subjects = agreement_nouns.get("plural", [])
        verb_base = self._pick_from_pool("transitive_verbs", blueprint)
        obj = self._pick_from_pool("objects", blueprint)

        if item_number_seed(blueprint["id"]) % 2 == 0 and plural_subjects:
            subject = plural_subjects[0]
            wrong = f"{subject} {self.verb_engine.third_person_singular(verb_base)} {obj} every day."
            correct = f"{subject} {verb_base} {obj} every day."
        else:
            subject = singular_subjects[0] if singular_subjects else "The student"
            wrong = f"{subject} {verb_base} {obj} every day."
            correct = f"{subject} {self.verb_engine.third_person_singular(verb_base)} {obj} every day."

        return {
            "prompt": f"Correct the subject-verb agreement error: {wrong}",
            "expected_answer": correct,
            "accepted_variants": [correct],
            "answer_preview": correct,
        }

    def _build_object_pronoun_correction(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        pair = self._pick_from_pool("pronoun_pairs", blueprint)
        subject = "I"
        verb = "like"
        wrong = f"{subject} {verb} {pair['subject']}."
        correct = f"{subject} {verb} {pair['object']}."
        return {
            "prompt": f"Correct the pronoun form: {wrong}",
            "expected_answer": correct,
            "accepted_variants": [correct],
            "answer_preview": correct,
        }

    def _build_verb_preposition_fill(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        pair = self._pick_from_pool("verb_preposition_pairs", blueprint)
        prompt = f"Fill in the missing preposition: {pair['subject']} {pair['verb']} ____ {pair['tail']}."
        expected = pair["preposition"]
        return {
            "prompt": prompt,
            "expected_answer": expected,
            "accepted_variants": [expected],
            "answer_preview": f"{pair['subject']} {pair['verb']} {expected} {pair['tail']}.",
        }

    def _build_svo_fill(self, blueprint: dict[str, Any]) -> dict[str, Any]:
        svo_patterns = self.lexical_pools.get("svo_patterns", {})
        bucket = "missing_subject" if item_number_seed(blueprint["id"]) % 2 == 0 else "missing_verb"
        pattern = svo_patterns.get(bucket, [{}])[0]
        return {
            "prompt": f"Fill in the missing word to complete the sentence: {pattern.get('prompt', '____')}",
            "expected_answer": pattern.get("answer", ""),
            "accepted_variants": [pattern.get("answer", "")],
            "answer_preview": pattern.get("prompt", "").replace("____", pattern.get("answer", "")),
        }

    def _pick_feature(self, blueprint: dict[str, Any], allowed: set[str]) -> str:
        for feature in blueprint.get("required_features", []):
            if feature in allowed:
                return feature
        raise ValueError("No supported tense feature found.")

    def _pick_subject(self, tense: str, blueprint: dict[str, Any]) -> dict[str, Any]:
        subjects = self.lexical_pools.get("subjects", {})
        seed = item_number_seed(blueprint["id"])
        if tense == "present continuous":
            ordered_groups = ["first_person", "singular", "plural", "second_person"]
        elif tense == "present simple":
            ordered_groups = ["singular", "plural", "first_person", "second_person"]
        else:
            ordered_groups = ["first_person", "singular", "plural", "second_person"]

        candidates: list[dict[str, Any]] = []
        for group in ordered_groups:
            candidates.extend(subjects.get(group, []))
        if not candidates:
            return {"surface": "I", "subject_key": "i", "number": "singular"}
        return candidates[seed % len(candidates)]

    def _pick_from_pool(self, name: str, blueprint: dict[str, Any]):
        pool = self.lexical_pools.get(name, [])
        if not pool:
            raise ValueError(f"Missing lexical pool: {name}")
        return pool[item_number_seed(blueprint["id"] + name) % len(pool)]

    def _pick_time_marker(self, tense: str, blueprint: dict[str, Any]) -> str:
        markers = self.lexical_pools.get("time_markers", {}).get(tense, [])
        if not markers:
            return ""
        return markers[item_number_seed(blueprint["id"] + tense) % len(markers)]

    def _affirmative_sentence(
        self,
        tense: str,
        subject: dict[str, Any],
        verb_base: str,
        obj: str,
        time_marker: str,
    ) -> str:
        subject_surface = subject["surface"]
        subject_key = subject["subject_key"]
        verb_phrase = self._affirmative_verb_phrase(tense, subject, verb_base)
        return self._fill_sentence_template(subject_surface, verb_phrase, obj, time_marker)

    def _affirmative_verb_phrase(self, tense: str, subject: dict[str, Any], verb_base: str) -> str:
        subject_key = subject["subject_key"]
        if tense == "present continuous":
            return self.verb_engine.suggest_for_tense(verb_base, "present_continuous", subject_key)
        if tense == "future simple":
            return self.verb_engine.suggest_for_tense(verb_base, "future_simple", subject_key)
        if tense == "past simple":
            return self.verb_engine.suggest_for_tense(verb_base, "past_simple", subject_key)
        return self.verb_engine.suggest_for_tense(verb_base, "present_simple", subject_key)

    def _negative_variants(self, tense: str, subject: dict[str, Any], verb_base: str, obj: str, time_marker: str) -> list[str]:
        subject_key = subject["subject_key"]
        subject_surface = subject["surface"]
        templates = self.realization_rules.get("negative_variants", {})
        template_key = tense
        if tense == "present simple" and subject_key in {"he", "she", "it"}:
            template_key = "present simple-third-person"
        selected = templates.get(template_key, [])
        return [
            self._fill_template(
                template,
                subject_surface=subject_surface,
                subject_key=subject_key,
                verb_base=verb_base,
                obj=obj,
                time_marker=time_marker,
            )
            for template in selected
        ]

    def _question_variants(self, tense: str, subject: dict[str, Any], verb_base: str, obj: str, time_marker: str) -> list[str]:
        subject_key = subject["subject_key"]
        subject_surface = subject["surface"]
        rules = self.realization_rules.get("question_variants", {})
        template_key = tense
        if tense == "present simple" and subject_key in {"he", "she", "it"}:
            template_key = "present simple-third-person"
        template = rules.get(template_key)
        if not template:
            return []
        return [
            self._fill_template(
                template,
                subject_surface=subject_surface,
                subject_key=subject_key,
                verb_base=verb_base,
                obj=obj,
                time_marker=time_marker,
            )
        ]

    def _fill_template(
        self,
        template: str,
        *,
        subject_surface: str,
        subject_key: str,
        verb_base: str,
        obj: str,
        time_marker: str,
    ) -> str:
        be_forms = self.realization_rules.get("be_forms", {}).get(subject_key, {})
        mapping = {
            "subject": subject_surface,
            "subject_lower": subject_surface.lower(),
            "verb_base": verb_base,
            "verb_gerund": self.verb_engine.gerund(verb_base),
            "object": obj,
            "time_marker": time_marker,
            "be_positive": be_forms.get("positive", "is"),
            "be_negative": be_forms.get("negative", "is not"),
            "be_contracted_negative": be_forms.get("contracted_negative", "isn't"),
            "be_question": be_forms.get("question", "Is"),
        }
        filled = template.format(**mapping)
        return " ".join(filled.replace(" .", ".").replace(" ?", "?").split())

    @staticmethod
    def _fill_sentence_template(subject_surface: str, verb_phrase: str, obj: str, time_marker: str) -> str:
        core = f"{subject_surface} {verb_phrase} {obj}"
        if time_marker:
            core = f"{core} {time_marker}"
        return f"{core}."


def item_number_seed(text: str) -> int:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)
