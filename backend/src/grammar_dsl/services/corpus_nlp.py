import random
import spacy
from typing import Any

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

CORPUS = [
    "The sun rises in the east every morning.",
    "Water boils at 100 degrees Celsius.",
    "She always drinks coffee before starting her shift.",
    "My brother works as a software engineer in Tokyo.",
    "Do they play basketball on weekends?",
    "Does the train arrive at 8 PM?",
    "I do not like eating spicy food.",
    "He doesn't understand the new policy.",
    "Birds migrate south during the winter season.",
    "The teacher explains the lesson very clearly.",
    
    "Alexander Graham Bell invented the telephone in 1876.",
    "We traveled to Paris for our honeymoon last year.",
    "She watched a fascinating documentary about space yesterday.",
    "The company launched its new product two weeks ago.",
    "Did you finish reading that mystery novel?",
    "Did the team win the championship game?",
    "I did not sleep well last night.",
    "They didn't receive the package on time.",
    "He built a beautiful wooden cabin in the woods.",
    "The choir sang beautifully at the concert.",
    
    "Are you studying for the final exam right now?",
    "Is she working on the new marketing campaign?",
    "I am currently reading a book about artificial intelligence.",
    "They are building a new shopping mall downtown.",
    "The chef is preparing a special dessert for the guests.",
    "We aren't watching television at the moment.",
    "He isn't listening to the radio anymore.",
    
    "Will you attend the conference next month?",
    "She will probably accept the job offer.",
    "I think it will rain tomorrow afternoon.",
    "They won't invest in that risky startup.",
    "He will not surrender without a fight.",
    
    "Have you ever visited the Great Wall of China?",
    "Has she completed the annual report yet?",
    "I have lived in this neighborhood for ten years.",
    "They have recently upgraded their computer systems.",
    "He hasn't replied to my email yet.",
    
    "By the time we arrived, the movie had already started.",
    "She had finished her homework before dinner.",
    "Had they met each other before the party?",
    
    "They will have completed the project by next Friday.",
    "Will you have graduated by this time next year?",
    "She will have arrived before the meeting starts.",
    
    "I have been waiting for the bus for thirty minutes.",
    "She has been studying English since she was a child.",
    "They have been working on the garden all morning.",
    
    "He had been driving for six hours before he finally took a break.",
    "We had been expecting the news for several weeks.",
    
    "This time tomorrow, I will be flying to London.",
    "Will they be playing football at 4 PM?",
    "She will be working late tonight.",
    
    "Next year, she will have been teaching for twenty years.",
    "By midnight, they will have been dancing for five hours.",

    "The committee meets every Tuesday to discuss finances.",
    "Do you know the way to the nearest hospital?",
    "She does not eat meat because she is a vegetarian.",
    "A massive earthquake shook the city yesterday.",
    "Did the CEO announce his resignation?",
    "He did not expect such a warm welcome.",
    "The stars shine brightly in the night sky.",
    "The committee meets every Tuesday to discuss finances.",
    "The train leaves the station at 6 AM.",
    "My parents visit my grandmother every weekend.",
    "The library opens at nine o'clock.",
    "Students submit homework before Friday.",
    "Our manager checks every report carefully.",
    "The bakery sells fresh bread every morning.",
    "The bus arrives on time most days.",
    "My cousin teaches math at a local school.",
    "The gardener waters the plants every evening.",
    "Doctors advise patients to exercise regularly.",
    "The museum closes at 5 PM.",
    "The goalkeeper saves difficult shots.",
    "The river flows through the valley.",
    "The radio plays news every hour.",
    "My sister drives to work every day.",
    "Tourists take photos near the fountain.",
    "The principal greets students at the gate.",
    "The store offers discounts in summer.",
    "Our team practices after class.",
    "The newspaper publishes new articles daily.",
    "The receptionist answers calls politely.",
    "The cat sleeps on the sofa every afternoon.",
    "The company exports products to neighboring countries.",
    "Water froze quickly in the bitter cold.",
    "Did you see the shooting star?",
    "She does not play the piano very well."
]

def generate_exercises_with_corpus(count: int, features: list[str]) -> list[dict[str, Any]]:
    if not nlp:
        return [{
            "type": "fill blank",
            "difficulty": "starter",
            "prompt": "NLP Error: spaCy model 'en_core_web_sm' is not loaded.",
            "expected_answer": "error",
            "accepted_variants": []
        }]
    
    pool = list(CORPUS)
    random.shuffle(pool)
    
    results = []
    
    requested_features = [f.lower() for f in features if f]
    if not requested_features:
        requested_features = ["present simple and affirmative"]

    for req_feat in requested_features:
        req_feat_lower = req_feat.lower()
        for sentence in pool:
            doc = nlp(sentence)

            if not _sentence_matches_features(doc, sentence, req_feat_lower):
                continue

            main_verb = _pick_main_verb(doc)
            if not main_verb:
                continue

            expected = main_verb.text
            lemma = main_verb.lemma_
            prompt = sentence.replace(expected, f"({lemma}) ____", 1)

            results.append({
                "type": "fill blank",
                "difficulty": "intermediate",
                "prompt": prompt,
                "expected_answer": expected,
                "accepted_variants": [expected]
            })
            pool.remove(sentence)
            break

    # Fill remaining slots while respecting requested features.
    # If the corpus is too small for strict uniqueness, allow repeats.
    req_cycle_idx = 0
    used_prompts: set[str] = {item["prompt"] for item in results}
    guarded_iterations = 0
    max_iterations = max(200, count * 20)
    while len(results) < count and guarded_iterations < max_iterations:
        guarded_iterations += 1
        req_feat_lower = requested_features[req_cycle_idx % len(requested_features)]
        req_cycle_idx += 1

        matching_sentences = []
        for sentence in CORPUS:
            doc = nlp(sentence)
            if _sentence_matches_features(doc, sentence, req_feat_lower):
                matching_sentences.append((sentence, doc))
        if not matching_sentences:
            continue

        unseen_matches = [entry for entry in matching_sentences if entry[0] not in used_prompts]
        if unseen_matches:
            sentence, doc = random.choice(unseen_matches)
        else:
            sentence, doc = random.choice(matching_sentences)
        main_verb = _pick_main_verb(doc)
        if not main_verb:
            continue

        expected = main_verb.text
        lemma = main_verb.lemma_
        prompt = sentence.replace(expected, f"({lemma}) ____", 1)
        results.append({
            "type": "fill blank",
            "difficulty": "intermediate",
            "prompt": prompt,
            "expected_answer": expected,
            "accepted_variants": [expected]
        })
        used_prompts.add(prompt)

    return results[:count]


def _pick_main_verb(doc):
    for token in doc:
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            return token
    for token in doc:
        if token.pos_ == "VERB":
            return token
    return None


def _sentence_matches_features(doc, sentence: str, req_feat_lower: str) -> bool:
    is_question = sentence.strip().endswith("?")
    has_not = any(t.lower_ in ("not", "n't") for t in doc)

    has_vbd = any(t.tag_ == "VBD" for t in doc)
    has_vbp_vbz = any(t.tag_ in ("VBP", "VBZ") for t in doc)
    has_vbg = any(t.tag_ == "VBG" for t in doc)
    has_will = any(t.lower_ == "will" for t in doc)
    has_have_aux = any(t.lower_ in {"have", "has", "had"} for t in doc)
    has_be_aux = any(t.lower_ in {"am", "is", "are", "was", "were"} for t in doc)

    wants_question = "interrogative" in req_feat_lower
    wants_negative = "negative" in req_feat_lower
    wants_affirmative = "affirmative" in req_feat_lower or (not wants_question and not wants_negative)

    if wants_question and not is_question:
        return False
    if wants_negative and not has_not:
        return False
    if wants_affirmative and (is_question or has_not):
        return False

    if "present perfect continuous" in req_feat_lower:
        return has_have_aux and has_be_aux and has_vbg and any(t.lower_ in {"have", "has"} for t in doc)

    if "past perfect continuous" in req_feat_lower:
        return has_have_aux and has_be_aux and has_vbg and any(t.lower_ == "had" for t in doc)

    if "future perfect continuous" in req_feat_lower:
        return has_will and has_have_aux and has_be_aux and has_vbg

    if "present perfect" in req_feat_lower:
        if not (has_have_aux and any(t.tag_ in ("VBN", "VBD") for t in doc) and not has_be_aux):
            return False
        return any(t.lower_ in {"have", "has"} for t in doc)

    if "past perfect" in req_feat_lower:
        return any(t.lower_ == "had" for t in doc) and any(t.tag_ in ("VBN", "VBD") for t in doc) and not has_be_aux

    if "future perfect" in req_feat_lower:
        return has_will and has_have_aux and not has_be_aux

    if "present continuous" in req_feat_lower:
        return has_be_aux and has_vbg and any(t.lower_ in {"am", "is", "are"} for t in doc)

    if "past continuous" in req_feat_lower:
        return has_be_aux and has_vbg and any(t.lower_ in {"was", "were"} for t in doc)

    if "future continuous" in req_feat_lower:
        return has_will and has_be_aux

    if "past simple" in req_feat_lower:
        return has_vbd and not has_will and not has_have_aux and not has_be_aux

    if "future simple" in req_feat_lower:
        return has_will and not has_have_aux and not has_be_aux

    if "present simple" in req_feat_lower:
        return has_vbp_vbz and not has_vbg and not has_will and not has_have_aux and not has_be_aux

    return True
