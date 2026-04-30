from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path
from typing import Any
from uuid import uuid4


DEMO_ACCOUNTS = [
    {
        "username": "alice",
        "password": "alice123",
        "display_name": "Alice Nguyen",
        "focus_hint": "Often mixes tense and spelling in short paragraphs.",
        "role": "student",
    },
    {
        "username": "brian",
        "password": "brian123",
        "display_name": "Brian Tran",
        "focus_hint": "Teaches collocations and semantic awkwardness.",
        "role": "tutor",
    },
    {
        "username": "clara",
        "password": "clara123",
        "display_name": "Clara Le",
        "focus_hint": "Often struggles with agreement and verb-preposition patterns.",
        "role": "student",
    },
    {
        "username": "david",
        "password": "david123",
        "display_name": "David Ho",
        "focus_hint": "Often needs more work with object pronouns and tense forms.",
        "role": "student",
    },
    {
        "username": "emma",
        "password": "emma123",
        "display_name": "Emma Pham",
        "focus_hint": "Teaches sentence forms and writing drills.",
        "role": "tutor",
    },
]


class UserProfileStore:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path) if db_path is not None else self._default_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def log_command(
        self,
        *,
        user_id: str,
        command_text: str,
        command_name: str,
        success: bool,
        message: str,
        profile_eligible: bool = False,
        sentence_count: int = 0,
        spelling_issue_count: int = 0,
        grammar_error_count: int = 0,
        semantic_warning_count: int = 0,
        original_text: str | None = None,
        corrected_text: str | None = None,
        issues: list[dict[str, Any]] | None = None,
    ) -> int:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO command_runs (
                    user_id,
                    command_text,
                    command_name,
                    success,
                    message,
                    profile_eligible,
                    sentence_count,
                    spelling_issue_count,
                    grammar_error_count,
                    semantic_warning_count,
                    original_text,
                    corrected_text
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    command_text,
                    command_name,
                    1 if success else 0,
                    message,
                    1 if profile_eligible else 0,
                    sentence_count,
                    spelling_issue_count,
                    grammar_error_count,
                    semantic_warning_count,
                    original_text,
                    corrected_text,
                ),
            )
            run_id = int(cursor.lastrowid)

            if issues:
                cursor.executemany(
                    """
                    INSERT INTO run_issues (
                        run_id,
                        rule_id,
                        category,
                        severity,
                        message,
                        evidence,
                        suggestion,
                        replacement
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            run_id,
                            issue.get("rule_id"),
                            issue.get("category", "Unknown"),
                            issue.get("severity", "error"),
                            issue.get("message", ""),
                            issue.get("evidence"),
                            issue.get("suggestion"),
                            issue.get("replacement"),
                        )
                        for issue in issues
                    ],
                )

            connection.commit()
            return run_id
        finally:
            connection.close()

    def authenticate_user(self, username: str, password: str) -> dict[str, str] | None:
        normalized_username = username.strip().lower()
        if not normalized_username or not password:
            return None

        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT username, display_name, role
                FROM users
                WHERE username = ?
                  AND password_hash = ?
                """,
                (normalized_username, self._hash_password(password)),
            ).fetchone()
        finally:
            connection.close()

        return self._row_to_user(row)

    def get_user_by_username(self, username: str | None) -> dict[str, str] | None:
        normalized_username = (username or "").strip().lower()
        if not normalized_username:
            return None

        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT username, display_name, role
                FROM users
                WHERE username = ?
                """,
                (normalized_username,),
            ).fetchone()
        finally:
            connection.close()

        return self._row_to_user(row)

    def create_session(self, username: str) -> str:
        token = uuid4().hex
        connection = self._connect()
        try:
            connection.execute(
                """
                INSERT INTO user_sessions (session_token, username)
                VALUES (?, ?)
                """,
                (token, username.strip().lower()),
            )
            connection.commit()
        finally:
            connection.close()
        return token

    def get_user_by_session(self, session_token: str | None) -> dict[str, str] | None:
        token = (session_token or "").strip()
        if not token:
            return None

        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT users.username, users.display_name, users.role
                FROM user_sessions
                JOIN users ON users.username = user_sessions.username
                WHERE user_sessions.session_token = ?
                """,
                (token,),
            ).fetchone()
        finally:
            connection.close()

        return self._row_to_user(row)

    def delete_session(self, session_token: str | None) -> None:
        token = (session_token or "").strip()
        if not token:
            return

        connection = self._connect()
        try:
            connection.execute(
                "DELETE FROM user_sessions WHERE session_token = ?",
                (token,),
            )
            connection.commit()
        finally:
            connection.close()

    def get_demo_accounts(self) -> list[dict[str, str]]:
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT username, display_name, demo_password, focus_hint, role
                FROM users
                ORDER BY role DESC, username
                """
            ).fetchall()
        finally:
            connection.close()

        return [
            {
                "username": row["username"],
                "password": row["demo_password"],
                "display_name": row["display_name"],
                "focus_hint": row["focus_hint"],
                "role": row["role"],
            }
            for row in rows
        ]

    def create_demo_student(self, *, username: str, password: str, display_name: str, focus_hint: str) -> dict[str, str]:
        normalized_username = username.strip().lower()
        if not normalized_username:
            raise ValueError("Username is required.")

        connection = self._connect()
        try:
            existing = connection.execute(
                "SELECT username FROM users WHERE username = ?",
                (normalized_username,),
            ).fetchone()
            if existing is not None:
                raise ValueError("This username is already taken in demo mode.")

            connection.execute(
                """
                INSERT INTO users (username, display_name, password_hash, demo_password, focus_hint, role)
                VALUES (?, ?, ?, ?, ?, 'student')
                """,
                (
                    normalized_username,
                    display_name.strip() or normalized_username.title(),
                    self._hash_password(password),
                    password,
                    focus_hint.strip() or "New learner profile.",
                ),
            )
            connection.commit()
        finally:
            connection.close()

        user = self.get_user_by_username(normalized_username)
        if user is None:
            raise ValueError("Could not create the student account.")
        return user

    def clear_user_history(self, user_id: str) -> int:
        normalized_user = (user_id or "").strip().lower()
        if not normalized_user:
            return 0

        connection = self._connect()
        try:
            cursor = connection.execute(
                "DELETE FROM command_runs WHERE user_id = ?",
                (normalized_user,),
            )
            connection.commit()
            return int(cursor.rowcount if cursor.rowcount is not None else 0)
        finally:
            connection.close()

    def get_command_history(self, user_id: str, limit: int = 12) -> dict[str, Any]:
        connection = self._connect()
        try:
            total_commands = int(
                connection.execute(
                    "SELECT COUNT(*) FROM command_runs WHERE user_id = ?",
                    (user_id,),
                ).fetchone()[0]
            )

            rows = connection.execute(
                """
                SELECT
                    id,
                    created_at,
                    command_text,
                    command_name,
                    success,
                    message,
                    sentence_count,
                    spelling_issue_count,
                    grammar_error_count,
                    semantic_warning_count
                FROM command_runs
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        finally:
            connection.close()

        entries = [
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "command": row["command_text"],
                "command_name": row["command_name"],
                "success": bool(row["success"]),
                "message": row["message"],
                "sentence_count": row["sentence_count"],
                "spelling_issue_count": row["spelling_issue_count"],
                "grammar_error_count": row["grammar_error_count"],
                "semantic_warning_count": row["semantic_warning_count"],
                "issue_count": row["spelling_issue_count"] + row["grammar_error_count"] + row["semantic_warning_count"],
            }
            for row in rows
        ]

        return {
            "total_commands": total_commands,
            "entries": entries,
        }

    def get_revision_source_data(self, user_id: str, run_limit: int = 15) -> dict[str, Any]:
        connection = self._connect()
        try:
            run_rows = connection.execute(
                """
                SELECT
                    id,
                    created_at,
                    command_text,
                    original_text,
                    corrected_text,
                    sentence_count,
                    spelling_issue_count,
                    grammar_error_count,
                    semantic_warning_count
                FROM command_runs
                WHERE user_id = ?
                  AND profile_eligible = 1
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, run_limit),
            ).fetchall()

            if not run_rows:
                return {
                    "runs": [],
                    "issues": [],
                }

            run_ids = [int(row["id"]) for row in run_rows]
            placeholders = ",".join("?" for _ in run_ids)
            issue_rows = connection.execute(
                f"""
                SELECT
                    id,
                    run_id,
                    rule_id,
                    category,
                    severity,
                    message,
                    evidence,
                    suggestion,
                    replacement
                FROM run_issues
                WHERE run_id IN ({placeholders})
                ORDER BY run_id DESC, id ASC
                """,
                run_ids,
            ).fetchall()
        finally:
            connection.close()

        return {
            "runs": [
                {
                    "id": row["id"],
                    "created_at": row["created_at"],
                    "command": row["command_text"],
                    "original_text": row["original_text"],
                    "corrected_text": row["corrected_text"],
                    "sentence_count": row["sentence_count"],
                    "spelling_issue_count": row["spelling_issue_count"],
                    "grammar_error_count": row["grammar_error_count"],
                    "semantic_warning_count": row["semantic_warning_count"],
                }
                for row in run_rows
            ],
            "issues": [
                {
                    "id": row["id"],
                    "run_id": row["run_id"],
                    "rule_id": row["rule_id"],
                    "category": row["category"],
                    "severity": row["severity"],
                    "message": row["message"],
                    "evidence": row["evidence"],
                    "suggestion": row["suggestion"],
                    "replacement": row["replacement"],
                }
                for row in issue_rows
            ],
        }

    def create_class(self, tutor_username: str, name: str) -> dict[str, Any]:
        normalized_tutor = tutor_username.strip().lower()
        if not name.strip():
            raise ValueError("Class name is required.")

        connection = self._connect()
        try:
            join_code = self._generate_join_code(connection)
            cursor = connection.execute(
                """
                INSERT INTO classes (name, join_code, tutor_username)
                VALUES (?, ?, ?)
                """,
                (name.strip(), join_code, normalized_tutor),
            )
            class_id = int(cursor.lastrowid)
            connection.commit()
        finally:
            connection.close()

        detail = self.get_class_detail(class_id, normalized_tutor, "tutor")
        if detail is None:
            raise ValueError("Could not create class.")
        return detail

    def join_class(self, student_username: str, join_code: str) -> dict[str, Any]:
        normalized_student = student_username.strip().lower()
        normalized_code = join_code.strip().upper()
        if not normalized_code:
            raise ValueError("Join code is required.")

        connection = self._connect()
        try:
            class_row = connection.execute(
                "SELECT id FROM classes WHERE join_code = ?",
                (normalized_code,),
            ).fetchone()
            if class_row is None:
                raise ValueError("Join code not found.")

            connection.execute(
                """
                INSERT OR IGNORE INTO class_members (class_id, student_username)
                VALUES (?, ?)
                """,
                (int(class_row["id"]), normalized_student),
            )
            connection.commit()
            class_id = int(class_row["id"])
        finally:
            connection.close()

        detail = self.get_class_detail(class_id, normalized_student, "student")
        if detail is None:
            raise ValueError("Could not join class.")
        return detail

    def list_classes_for_user(self, username: str, role: str) -> list[dict[str, Any]]:
        normalized_username = username.strip().lower()
        connection = self._connect()
        try:
            if role == "tutor":
                rows = connection.execute(
                    """
                    SELECT
                        classes.id,
                        classes.name,
                        classes.join_code,
                        classes.created_at,
                        classes.tutor_username,
                        users.display_name AS tutor_display_name,
                        COUNT(DISTINCT class_members.student_username) AS roster_count,
                        COUNT(DISTINCT quizzes.id) AS quiz_count
                    FROM classes
                    JOIN users ON users.username = classes.tutor_username
                    LEFT JOIN class_members ON class_members.class_id = classes.id
                    LEFT JOIN quizzes ON quizzes.class_id = classes.id
                    WHERE classes.tutor_username = ?
                    GROUP BY classes.id
                    ORDER BY classes.id DESC
                    """,
                    (normalized_username,),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT
                        classes.id,
                        classes.name,
                        classes.join_code,
                        classes.created_at,
                        classes.tutor_username,
                        users.display_name AS tutor_display_name,
                        COUNT(DISTINCT class_members.student_username) AS roster_count,
                        COUNT(DISTINCT quizzes.id) AS quiz_count
                    FROM class_members
                    JOIN classes ON classes.id = class_members.class_id
                    JOIN users ON users.username = classes.tutor_username
                    LEFT JOIN quizzes ON quizzes.class_id = classes.id
                    WHERE class_members.student_username = ?
                    GROUP BY classes.id
                    ORDER BY classes.id DESC
                    """,
                    (normalized_username,),
                ).fetchall()
        finally:
            connection.close()

        return [self._class_summary_row_to_dict(row, include_join_code=role == "tutor") for row in rows]

    def get_class_detail(self, class_id: int, username: str, role: str) -> dict[str, Any] | None:
        normalized_username = username.strip().lower()
        connection = self._connect()
        try:
            class_row = connection.execute(
                """
                SELECT
                    classes.id,
                    classes.name,
                    classes.join_code,
                    classes.created_at,
                    classes.tutor_username,
                    users.display_name AS tutor_display_name
                FROM classes
                JOIN users ON users.username = classes.tutor_username
                WHERE classes.id = ?
                """,
                (class_id,),
            ).fetchone()
            if class_row is None:
                return None

            if role == "tutor" and class_row["tutor_username"] != normalized_username:
                return None
            if role != "tutor":
                member_row = connection.execute(
                    """
                    SELECT 1
                    FROM class_members
                    WHERE class_id = ? AND student_username = ?
                    """,
                    (class_id, normalized_username),
                ).fetchone()
                if member_row is None:
                    return None

            roster_rows = connection.execute(
                """
                SELECT users.username, users.display_name, users.focus_hint, users.role
                FROM class_members
                JOIN users ON users.username = class_members.student_username
                WHERE class_members.class_id = ?
                ORDER BY users.display_name
                """,
                (class_id,),
            ).fetchall()

            quiz_count = int(
                connection.execute(
                    "SELECT COUNT(*) FROM quizzes WHERE class_id = ?",
                    (class_id,),
                ).fetchone()[0]
            )
        finally:
            connection.close()

        return {
            "id": int(class_row["id"]),
            "name": class_row["name"],
            "join_code": class_row["join_code"] if role == "tutor" else None,
            "created_at": class_row["created_at"],
            "tutor_username": class_row["tutor_username"],
            "tutor_display_name": class_row["tutor_display_name"],
            "roster_count": len(roster_rows),
            "quiz_count": quiz_count,
            "students": [
                {
                    "username": row["username"],
                    "display_name": row["display_name"],
                    "focus_hint": row["focus_hint"],
                    "role": row["role"],
                }
                for row in roster_rows
            ],
        }

    def list_quizzes_for_class(self, class_id: int, username: str, role: str) -> list[dict[str, Any]]:
        if self.get_class_detail(class_id, username, role) is None:
            return []

        normalized_username = username.strip().lower()
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT
                    quizzes.id,
                    quizzes.title,
                    quizzes.feature_expr_text,
                    quizzes.exercise_count,
                    quizzes.created_at,
                    quizzes.created_by
                FROM quizzes
                WHERE quizzes.class_id = ?
                ORDER BY quizzes.id DESC
                """,
                (class_id,),
            ).fetchall()

            attempts_by_quiz: dict[int, sqlite3.Row] = {}
            if role == "student":
                attempt_rows = connection.execute(
                    """
                    SELECT quiz_id, score, max_score, submitted_at
                    FROM quiz_attempts
                    WHERE student_username = ?
                    """,
                    (normalized_username,),
                ).fetchall()
                attempts_by_quiz = {int(row["quiz_id"]): row for row in attempt_rows}
        finally:
            connection.close()

        quizzes = []
        for row in rows:
            attempt_row = attempts_by_quiz.get(int(row["id"]))
            quizzes.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "feature_expr_text": row["feature_expr_text"],
                    "exercise_count": row["exercise_count"],
                    "created_at": row["created_at"],
                    "created_by": row["created_by"],
                    "attempt_status": "submitted" if attempt_row is not None else "not_submitted",
                    "score": attempt_row["score"] if attempt_row is not None else None,
                    "max_score": attempt_row["max_score"] if attempt_row is not None else None,
                    "submitted_at": attempt_row["submitted_at"] if attempt_row is not None else None,
                }
            )
        return quizzes

    def create_quiz(
        self,
        *,
        class_id: int,
        created_by: str,
        title: str,
        feature_expr_text: str,
        exercise_count: int,
        exercise_payload: list[dict[str, Any]],
        answer_key_payload: list[dict[str, Any]],
    ) -> dict[str, Any]:
        connection = self._connect()
        try:
            cursor = connection.execute(
                """
                INSERT INTO quizzes (
                    class_id,
                    title,
                    feature_expr_text,
                    exercise_count,
                    exercise_payload,
                    answer_key_payload,
                    created_by
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    class_id,
                    title.strip(),
                    feature_expr_text,
                    exercise_count,
                    json.dumps(exercise_payload, ensure_ascii=False),
                    json.dumps(answer_key_payload, ensure_ascii=False),
                    created_by.strip().lower(),
                ),
            )
            quiz_id = int(cursor.lastrowid)
            connection.commit()
        finally:
            connection.close()

        detail = self.get_quiz_detail(quiz_id, created_by, "tutor")
        if detail is None:
            raise ValueError("Could not create quiz.")
        return detail

    def get_quiz_detail(self, quiz_id: int, username: str, role: str) -> dict[str, Any] | None:
        normalized_username = username.strip().lower()
        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT
                    quizzes.id,
                    quizzes.class_id,
                    quizzes.title,
                    quizzes.feature_expr_text,
                    quizzes.exercise_count,
                    quizzes.exercise_payload,
                    quizzes.answer_key_payload,
                    quizzes.created_by,
                    quizzes.created_at,
                    classes.tutor_username
                FROM quizzes
                JOIN classes ON classes.id = quizzes.class_id
                WHERE quizzes.id = ?
                """,
                (quiz_id,),
            ).fetchone()
            if row is None:
                return None

            if role == "tutor":
                if row["tutor_username"] != normalized_username:
                    return None
            else:
                member = connection.execute(
                    """
                    SELECT 1
                    FROM class_members
                    WHERE class_id = ? AND student_username = ?
                    """,
                    (int(row["class_id"]), normalized_username),
                ).fetchone()
                if member is None:
                    return None

            attempt_row = connection.execute(
                """
                SELECT id, score, max_score, submitted_at, submission_payload
                FROM quiz_attempts
                WHERE quiz_id = ? AND student_username = ?
                """,
                (quiz_id, normalized_username),
            ).fetchone()
        finally:
            connection.close()

        return {
            "id": int(row["id"]),
            "class_id": int(row["class_id"]),
            "title": row["title"],
            "feature_expr_text": row["feature_expr_text"],
            "exercise_count": row["exercise_count"],
            "exercise_payload": self._json_loads(row["exercise_payload"], []),
            "answer_key_payload": self._json_loads(row["answer_key_payload"], []),
            "created_by": row["created_by"],
            "created_at": row["created_at"],
            "attempt": None
            if attempt_row is None
            else {
                "id": int(attempt_row["id"]),
                "score": attempt_row["score"],
                "max_score": attempt_row["max_score"],
                "submitted_at": attempt_row["submitted_at"],
                "submission_payload": self._json_loads(attempt_row["submission_payload"], {}),
            },
        }

    def save_quiz_attempt(
        self,
        *,
        quiz_id: int,
        student_username: str,
        score: float,
        max_score: float,
        submission_payload: dict[str, Any],
        item_results: list[dict[str, Any]],
    ) -> dict[str, Any]:
        normalized_username = student_username.strip().lower()
        connection = self._connect()
        try:
            existing = connection.execute(
                """
                SELECT id
                FROM quiz_attempts
                WHERE quiz_id = ? AND student_username = ?
                """,
                (quiz_id, normalized_username),
            ).fetchone()

            if existing is not None:
                raise ValueError("You have already submitted this quiz. Quizzes are limited to a single attempt.")

            cursor = connection.execute(
                """
                INSERT INTO quiz_attempts (quiz_id, student_username, score, max_score, submission_payload)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    quiz_id,
                    normalized_username,
                    score,
                    max_score,
                    json.dumps(submission_payload, ensure_ascii=False),
                ),
            )
            attempt_id = int(cursor.lastrowid)

            connection.executemany(
                """
                INSERT INTO attempt_items (
                    attempt_id,
                    item_index,
                    prompt,
                    answer_text,
                    expected_answer,
                    accepted_variants,
                    score,
                    feedback
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        attempt_id,
                        result.get("item_index"),
                        result.get("prompt"),
                        result.get("answer_text"),
                        result.get("expected_answer"),
                        json.dumps(result.get("accepted_variants", []), ensure_ascii=False),
                        result.get("score", 0),
                        json.dumps(result.get("feedback", ""), ensure_ascii=False) if isinstance(result.get("feedback"), dict) else result.get("feedback", ""),
                    )
                    for result in item_results
                ],
            )
            connection.commit()
        finally:
            connection.close()

        return {
            "attempt_id": attempt_id,
            "quiz_id": quiz_id,
            "student_username": normalized_username,
            "score": score,
            "max_score": max_score,
            "submission_payload": submission_payload,
        }

    def get_quiz_attempts(self, quiz_id: int, username: str) -> list[dict[str, Any]]:
        connection = self._connect()
        try:
            quiz_row = connection.execute(
                """
                SELECT quizzes.class_id, classes.tutor_username
                FROM quizzes
                JOIN classes ON classes.id = quizzes.class_id
                WHERE quizzes.id = ?
                """,
                (quiz_id,),
            ).fetchone()
            if quiz_row is None or quiz_row["tutor_username"] != username.strip().lower():
                return []

            member_rows = connection.execute(
                """
                SELECT users.username, users.display_name
                FROM class_members
                JOIN users ON users.username = class_members.student_username
                WHERE class_members.class_id = ?
                ORDER BY users.display_name
                """,
                (int(quiz_row["class_id"]),),
            ).fetchall()

            attempts = connection.execute(
                """
                SELECT id, student_username, score, max_score, submitted_at, submission_payload
                FROM quiz_attempts
                WHERE quiz_id = ?
                """,
                (quiz_id,),
            ).fetchall()
        finally:
            connection.close()

        attempts_by_user = {row["student_username"]: row for row in attempts}
        rows = []
        for member in member_rows:
            attempt = attempts_by_user.get(member["username"])
            rows.append(
                {
                    "student_name": member["display_name"],
                    "username": member["username"],
                    "score": attempt["score"] if attempt is not None else None,
                    "max_score": attempt["max_score"] if attempt is not None else None,
                    "status": "submitted" if attempt is not None else "not submitted",
                    "submitted_at": attempt["submitted_at"] if attempt is not None else None,
                    "submission_payload": self._json_loads(attempt["submission_payload"], None) if attempt is not None else None,
                }
            )
        return rows

    @staticmethod
    def _default_db_path() -> Path:
        temp_root = Path(tempfile.gettempdir()) / "grammardsl"
        return temp_root / "profile_history.sqlite3"

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = MEMORY")
        connection.execute("PRAGMA synchronous = NORMAL")
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def _json_loads(raw: str | None, fallback: Any) -> Any:
        if not raw:
            return fallback
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return fallback

    @staticmethod
    def _row_to_user(row: sqlite3.Row | None) -> dict[str, str] | None:
        if row is None:
            return None
        return {
            "username": row["username"],
            "display_name": row["display_name"],
            "role": row["role"],
        }

    @staticmethod
    def _class_summary_row_to_dict(row: sqlite3.Row, *, include_join_code: bool) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "name": row["name"],
            "join_code": row["join_code"] if include_join_code else None,
            "created_at": row["created_at"],
            "tutor_username": row["tutor_username"],
            "tutor_display_name": row["tutor_display_name"],
            "roster_count": int(row["roster_count"]),
            "quiz_count": int(row["quiz_count"]),
        }

    @staticmethod
    def _generate_join_code(connection: sqlite3.Connection) -> str:
        while True:
            candidate = uuid4().hex[:6].upper()
            existing = connection.execute(
                "SELECT 1 FROM classes WHERE join_code = ?",
                (candidate,),
            ).fetchone()
            if existing is None:
                return candidate

    def _initialize(self) -> None:
        connection = self._connect()
        try:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    demo_password TEXT NOT NULL,
                    focus_hint TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'student',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_token TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS command_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    command_text TEXT NOT NULL,
                    command_name TEXT NOT NULL,
                    success INTEGER NOT NULL DEFAULT 1,
                    message TEXT NOT NULL,
                    profile_eligible INTEGER NOT NULL DEFAULT 0,
                    sentence_count INTEGER NOT NULL DEFAULT 0,
                    spelling_issue_count INTEGER NOT NULL DEFAULT 0,
                    grammar_error_count INTEGER NOT NULL DEFAULT 0,
                    semantic_warning_count INTEGER NOT NULL DEFAULT 0,
                    original_text TEXT,
                    corrected_text TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS run_issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    rule_id TEXT,
                    category TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    evidence TEXT,
                    suggestion TEXT,
                    replacement TEXT,
                    FOREIGN KEY(run_id) REFERENCES command_runs(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    join_code TEXT NOT NULL UNIQUE,
                    tutor_username TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(tutor_username) REFERENCES users(username) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS class_members (
                    class_id INTEGER NOT NULL,
                    student_username TEXT NOT NULL,
                    joined_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (class_id, student_username),
                    FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE,
                    FOREIGN KEY(student_username) REFERENCES users(username) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS quizzes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    feature_expr_text TEXT NOT NULL,
                    exercise_count INTEGER NOT NULL,
                    exercise_payload TEXT NOT NULL,
                    answer_key_payload TEXT NOT NULL,
                    created_by TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(class_id) REFERENCES classes(id) ON DELETE CASCADE,
                    FOREIGN KEY(created_by) REFERENCES users(username) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quiz_id INTEGER NOT NULL,
                    student_username TEXT NOT NULL,
                    score REAL NOT NULL,
                    max_score REAL NOT NULL,
                    submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    submission_payload TEXT NOT NULL,
                    FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
                    FOREIGN KEY(student_username) REFERENCES users(username) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS attempt_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id INTEGER NOT NULL,
                    item_index INTEGER NOT NULL,
                    prompt TEXT NOT NULL,
                    answer_text TEXT NOT NULL,
                    expected_answer TEXT NOT NULL,
                    accepted_variants TEXT NOT NULL,
                    score REAL NOT NULL,
                    feedback TEXT NOT NULL,
                    FOREIGN KEY(attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_command_runs_user_created
                ON command_runs(user_id, id DESC);

                CREATE INDEX IF NOT EXISTS idx_user_sessions_username
                ON user_sessions(username);

                CREATE INDEX IF NOT EXISTS idx_run_issues_run_id
                ON run_issues(run_id);

                CREATE UNIQUE INDEX IF NOT EXISTS idx_quiz_attempts_quiz_student
                ON quiz_attempts(quiz_id, student_username);
                """
            )

            existing_columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(users)").fetchall()
            }
            if "role" not in existing_columns:
                connection.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'student'")

            for account in DEMO_ACCOUNTS:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO users (
                        username,
                        display_name,
                        password_hash,
                        demo_password,
                        focus_hint,
                        role
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        account["username"],
                        account["display_name"],
                        self._hash_password(account["password"]),
                        account["password"],
                        account["focus_hint"],
                        account["role"],
                    ),
                )
                connection.execute(
                    """
                    UPDATE users
                    SET display_name = ?, demo_password = ?, focus_hint = ?, role = ?
                    WHERE username = ?
                    """,
                    (
                        account["display_name"],
                        account["password"],
                        account["focus_hint"],
                        account["role"],
                        account["username"],
                    ),
                )

            connection.commit()
        finally:
            connection.close()
