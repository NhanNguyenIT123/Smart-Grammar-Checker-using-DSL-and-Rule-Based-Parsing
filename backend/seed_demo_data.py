import sqlite3
import json
import os
import hashlib
from datetime import datetime

import tempfile
from pathlib import Path

def get_db_path():
    temp_root = Path(tempfile.gettempdir()) / "grammardsl"
    return temp_root / "profile_history.sqlite3"

DB_PATH = get_db_path()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def seed():
    # Ensure directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect and initialize schema if empty
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Simple check for users table, if not exists, we can't seed
    try:
        cursor.execute("SELECT 1 FROM users LIMIT 1")
    except sqlite3.OperationalError:
        print("Database schema not found. Initializing via UserProfileStore...")
        # We need to import the store to get the initialization logic
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
        from grammar_dsl.personalization.store import UserProfileStore
        UserProfileStore(DB_PATH) # This creates tables
        # Re-connect after initialization
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

    print("Cleaning up old data...")
    cursor.execute("DELETE FROM attempt_items")
    cursor.execute("DELETE FROM quiz_attempts")
    cursor.execute("DELETE FROM quizzes")
    cursor.execute("DELETE FROM class_members")
    cursor.execute("DELETE FROM user_sessions")
    cursor.execute("DELETE FROM command_runs")
    cursor.execute("DELETE FROM run_issues")
    cursor.execute("DELETE FROM classes")
    cursor.execute("DELETE FROM users")
    conn.commit()

    # 1. Create Students
    students = [
        ("clara", "Clara Le", "clara123", "Often struggles with agreement and verb-preposition patterns.", "student"),
        ("david", "David Ho", "david123", "Often needs more work with object pronouns and tense forms.", "student"),
        ("sarah_smith", "Sarah Smith", "sarah123", "Interested in creative writing.", "student"),
        ("alice", "Alice Nguyen", "alice123", "Often mixes tense and spelling in short paragraphs.", "student"), # Alice stays unsubmitted
    ]

    for username, display_name, password, hint, role in students:
        cursor.execute("""
            INSERT OR REPLACE INTO users (username, display_name, password_hash, demo_password, focus_hint, role) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, display_name, hash_password(password), password, hint, role))

    # 2. Ensure Tutor exists
    cursor.execute("""
        INSERT OR REPLACE INTO users (username, display_name, password_hash, demo_password, focus_hint, role) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("brian", "Brian Tran", hash_password("brian123"), "brian123", "Teaches collocations and semantic awkwardness.", "tutor"))

    # 3. Create or Get Class
    join_code = "C0C4E1" 
    cursor.execute("SELECT id FROM classes WHERE join_code = ? LIMIT 1", (join_code,))
    class_row = cursor.fetchone()
    if not class_row:
        cursor.execute("INSERT INTO classes (name, join_code, tutor_username) VALUES (?, ?, ?)", 
                       ("Grammar Clinic A", join_code, "brian"))
        class_id = cursor.lastrowid
    else:
        class_id = class_row["id"]

    # 4. Join students to class
    for username, _, _, _, _ in students:
        cursor.execute("INSERT OR IGNORE INTO class_members (class_id, student_username) VALUES (?, ?)", (class_id, username))

    # 5. Create Multiple Quizzes
    quizzes_to_seed = [
        {
            "title": "Mixed Tense Mastery",
            "features": "mixed tenses",
            "exercises": [
                {"id": 1, "prompt": "She (drink) ____ coffee every morning.", "expected_answer": "drinks", "type": "fill_blank", "difficulty": "intermediate"},
                {"id": 2, "prompt": "They (watch) ____ a movie yesterday.", "expected_answer": "watched", "type": "fill_blank", "difficulty": "intermediate"},
                {"id": 3, "prompt": "I (be) ____ waiting for an hour.", "expected_answer": "have been", "type": "fill_blank", "difficulty": "intermediate"},
                {"id": 4, "prompt": "By next year, he (finish) ____ his degree.", "expected_answer": "will have finished", "type": "fill_blank", "difficulty": "intermediate"},
                {"id": 5, "prompt": "We (not like) ____ spicy food.", "expected_answer": "do not like", "type": "fill_blank", "difficulty": "intermediate"},
            ],
            "attempts": [
                ("clara", 5, 5, ["drinks", "watched", "have been", "will have finished", "do not like"]),
                ("david", 3, 5, ["drink", "watched", "am waiting", "will have finished", "do not like"]),
                ("sarah_smith", 1, 5, ["drinking", "watch", "was", "finish", "do not like"]),
            ]
        },
        {
            "title": "Present Continuous Drill",
            "features": "present continuous",
            "exercises": [
                {"id": 1, "prompt": "Look! The cat (sleep) ____ on your laptop.", "expected_answer": "is sleeping", "type": "fill_blank", "difficulty": "starter"},
                {"id": 2, "prompt": "Listen! Someone (knock) ____ at the door.", "expected_answer": "is knocking", "type": "fill_blank", "difficulty": "starter"},
                {"id": 3, "prompt": "We (have) ____ dinner right now.", "expected_answer": "are having", "type": "fill_blank", "difficulty": "starter"},
            ],
            "attempts": [
                ("clara", 3, 3, ["is sleeping", "is knocking", "are having"]),
                ("david", 2, 3, ["is sleeping", "knocks", "are having"]),
                ("sarah_smith", 1, 3, ["sleeps", "is knocking", "is have"]),
            ]
        },
        {
            "title": "Future Tense Basics",
            "features": "future simple",
            "exercises": [
                {"id": 1, "prompt": "I think it (rain) ____ tomorrow.", "expected_answer": "will rain", "type": "fill_blank", "difficulty": "starter"},
                {"id": 2, "prompt": "They (not arrive) ____ before 8 PM.", "expected_answer": "will not arrive", "type": "fill_blank", "difficulty": "starter"},
            ],
            "attempts": [
                ("clara", 2, 2, ["will rain", "will not arrive"]),
                ("david", 1, 2, ["rains", "will not arrive"]),
                ("sarah_smith", 0, 2, ["is rain", "arrives"]),
            ]
        }
    ]

    for q_data in quizzes_to_seed:
        cursor.execute("""
            INSERT INTO quizzes (class_id, title, feature_expr_text, exercise_count, exercise_payload, answer_key_payload, created_by) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (class_id, q_data["title"], q_data["features"], len(q_data["exercises"]), 
              json.dumps(q_data["exercises"]), json.dumps(q_data["exercises"]), "brian"))
        quiz_id = cursor.lastrowid

        for student_username, score, max_score, answers in q_data["attempts"]:
            item_results = []
            for i, ans in enumerate(answers):
                ex = q_data["exercises"][i]
                is_correct = ans.strip().lower() == ex["expected_answer"].strip().lower()
                item_results.append({
                    "item_index": i + 1,
                    "prompt": ex["prompt"],
                    "student_answer": ans,
                    "expected_answer": ex["expected_answer"],
                    "is_correct": is_correct,
                    "feedback": "Great job!" if is_correct else f"Incorrect. The right form is '{ex['expected_answer']}'."
                })
            
            payload = {
                "grading": {
                    "score": score,
                    "max_score": max_score,
                    "item_results": item_results
                }
            }
            
            cursor.execute("""
                INSERT INTO quiz_attempts (quiz_id, student_username, score, max_score, submission_payload) 
                VALUES (?, ?, ?, ?, ?)
            """, (quiz_id, student_username, score, max_score, json.dumps(payload)))
            attempt_id = cursor.lastrowid
            
            for it in item_results:
                cursor.execute("""
                    INSERT INTO attempt_items (attempt_id, item_index, prompt, answer_text, expected_answer, accepted_variants, score, feedback) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (attempt_id, it["item_index"], it["prompt"], it["student_answer"], it["expected_answer"], 
                      json.dumps([it["expected_answer"]]), 1.0 if it["is_correct"] else 0.0, it["feedback"]))

    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(quizzes_to_seed)} quizzes with demo data into {DB_PATH}")

if __name__ == "__main__":
    seed()
