from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_SRC = PROJECT_ROOT / "backend" / "src"

if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from grammar_dsl.personalization import UserProfileStore  # noqa: E402


class UserProfileStoreTests(unittest.TestCase):
    def create_store(self) -> tuple[UserProfileStore, Path]:
        db_path = Path(tempfile.gettempdir()) / f"grammardsl-store-test-{uuid4().hex}.sqlite3"
        return UserProfileStore(db_path), db_path

    def test_demo_accounts_are_seeded(self) -> None:
        store, db_path = self.create_store()
        try:
            accounts = store.get_demo_accounts()
            usernames = [account["username"] for account in accounts]
            self.assertIn("alice", usernames)
            self.assertIn("brian", usernames)
            self.assertIn("clara", usernames)
        finally:
            if db_path.exists():
                db_path.unlink()

    def test_authenticate_user_and_session_round_trip(self) -> None:
        store, db_path = self.create_store()
        try:
            user = store.authenticate_user("alice", "alice123")
            self.assertIsNotNone(user)
            token = store.create_session("alice")
            resolved = store.get_user_by_session(token)
            self.assertIsNotNone(resolved)
            self.assertEqual(resolved["username"], "alice")

            store.delete_session(token)
            self.assertIsNone(store.get_user_by_session(token))
        finally:
            if db_path.exists():
                db_path.unlink()


if __name__ == "__main__":
    unittest.main()
