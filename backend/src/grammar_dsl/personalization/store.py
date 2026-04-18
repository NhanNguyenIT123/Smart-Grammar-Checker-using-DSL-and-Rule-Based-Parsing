from __future__ import annotations

import hashlib
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
    },
    {
        "username": "brian",
        "password": "brian123",
        "display_name": "Brian Tran",
        "focus_hint": "Often needs help with collocations and semantic awkwardness.",
    },
    {
        "username": "clara",
        "password": "clara123",
        "display_name": "Clara Le",
        "focus_hint": "Often struggles with agreement and verb-preposition patterns.",
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
                SELECT username, display_name
                FROM users
                WHERE username = ?
                  AND password_hash = ?
                """,
                (normalized_username, self._hash_password(password)),
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            return None

        return {
            "username": row["username"],
            "display_name": row["display_name"],
        }

    def get_user_by_username(self, username: str | None) -> dict[str, str] | None:
        normalized_username = (username or "").strip().lower()
        if not normalized_username:
            return None

        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT username, display_name
                FROM users
                WHERE username = ?
                """,
                (normalized_username,),
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            return None

        return {
            "username": row["username"],
            "display_name": row["display_name"],
        }

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
                SELECT users.username, users.display_name
                FROM user_sessions
                JOIN users ON users.username = user_sessions.username
                WHERE user_sessions.session_token = ?
                """,
                (token,),
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            return None

        return {
            "username": row["username"],
            "display_name": row["display_name"],
        }

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
                SELECT username, display_name, demo_password, focus_hint
                FROM users
                ORDER BY username
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
            }
            for row in rows
        ]

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

                CREATE INDEX IF NOT EXISTS idx_command_runs_user_created
                ON command_runs(user_id, id DESC);

                CREATE INDEX IF NOT EXISTS idx_user_sessions_username
                ON user_sessions(username);

                CREATE INDEX IF NOT EXISTS idx_run_issues_run_id
                ON run_issues(run_id);
                """
            )
            connection.executemany(
                """
                INSERT OR IGNORE INTO users (
                    username,
                    display_name,
                    password_hash,
                    demo_password,
                    focus_hint
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        account["username"],
                        account["display_name"],
                        self._hash_password(account["password"]),
                        account["password"],
                        account["focus_hint"],
                    )
                    for account in DEMO_ACCOUNTS
                ],
            )
            connection.commit()
        finally:
            connection.close()
