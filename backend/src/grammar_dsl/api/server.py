from __future__ import annotations

import json
import re
from dataclasses import asdict
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from grammar_dsl.data import clear_repository_cache
from grammar_dsl.personalization import UserProfileStore
from grammar_dsl.preprocessing import load_pipeline_report
from grammar_dsl.services import CommandService


CLASS_DETAIL_PATTERN = re.compile(r"^/api/classes/(?P<class_id>\d+)$")
CLASS_QUIZZES_PATTERN = re.compile(r"^/api/classes/(?P<class_id>\d+)/quizzes$")
QUIZ_DETAIL_PATTERN = re.compile(r"^/api/quizzes/(?P<quiz_id>\d+)$")
QUIZ_ATTEMPTS_PATTERN = re.compile(r"^/api/quizzes/(?P<quiz_id>\d+)/attempts$")


class GrammarDSLRequestHandler(BaseHTTPRequestHandler):
    @staticmethod
    def _build_service() -> CommandService:
        clear_repository_cache()
        return CommandService()

    @staticmethod
    def _build_store() -> UserProfileStore:
        return UserProfileStore()

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        store = self._build_store()
        current_user = self._resolve_current_user(store)

        if self.path == "/api/health":
            self._write_json(200, {"status": "ok"})
            return

        if self.path == "/api/auth/me":
            self._write_json(
                200,
                {
                    "authenticated": current_user is not None,
                    "user": current_user,
                    "demo_accounts": store.get_demo_accounts(),
                },
            )
            return

        if self.path == "/api/pipeline":
            self._write_json(200, load_pipeline_report())
            return

        if self.path == "/api/help":
            if current_user is None:
                self._write_json(401, {"message": "Please log in first."})
                return
            service = self._build_service()
            response = service.execute("help", user_id=current_user["username"])
            self._write_json(200, asdict(response))
            return

        if self.path == "/api/classes":
            self._require_user_or_write(current_user)
            if current_user is None:
                return
            classes = store.list_classes_for_user(current_user["username"], current_user["role"])
            self._write_json(200, {"classes": classes})
            return

        class_detail_match = CLASS_DETAIL_PATTERN.match(self.path)
        if class_detail_match:
            self._require_user_or_write(current_user)
            if current_user is None:
                return
            class_id = int(class_detail_match.group("class_id"))
            detail = store.get_class_detail(class_id, current_user["username"], current_user["role"])
            if detail is None:
                self._write_json(404, {"message": "Class not found for the current user."})
                return
            self._write_json(200, detail)
            return

        class_quizzes_match = CLASS_QUIZZES_PATTERN.match(self.path)
        if class_quizzes_match:
            self._require_user_or_write(current_user)
            if current_user is None:
                return
            class_id = int(class_quizzes_match.group("class_id"))
            quizzes = store.list_quizzes_for_class(class_id, current_user["username"], current_user["role"])
            self._write_json(200, {"quizzes": quizzes})
            return

        quiz_detail_match = QUIZ_DETAIL_PATTERN.match(self.path)
        if quiz_detail_match:
            self._require_user_or_write(current_user)
            if current_user is None:
                return
            quiz_id = int(quiz_detail_match.group("quiz_id"))
            detail = store.get_quiz_detail(quiz_id, current_user["username"], current_user["role"])
            if detail is None:
                self._write_json(404, {"message": "Quiz not found for the current user."})
                return
            self._write_json(200, detail)
            return

        quiz_attempts_match = QUIZ_ATTEMPTS_PATTERN.match(self.path)
        if quiz_attempts_match:
            self._require_user_or_write(current_user)
            if current_user is None:
                return
            quiz_id = int(quiz_attempts_match.group("quiz_id"))
            if current_user["role"] != "tutor":
                self._write_json(403, {"message": "Only tutors can access quiz attempts."})
                return
            attempts = store.get_quiz_attempts(quiz_id, current_user["username"])
            self._write_json(200, {"rows": attempts})
            return

        self._write_json(404, {"message": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}

            if self.path == "/api/auth/login":
                self._handle_login(payload)
                return

            if self.path == "/api/auth/logout":
                self._handle_logout()
                return

            if self.path == "/api/auth/register":
                self._handle_register(payload)
                return

            store = self._build_store()
            current_user = self._resolve_current_user(store)

            if self.path == "/api/classes":
                self._require_user_or_write(current_user)
                if current_user is None:
                    return
                if current_user["role"] != "tutor":
                    self._write_json(403, {"message": "Only tutors can create classes."})
                    return
                name = str(payload.get("name", "")).strip()
                if not name:
                    self._write_json(400, {"message": "Class name is required."})
                    return
                created = store.create_class(name=name, tutor_username=current_user["username"])
                self._write_json(200, {"class": created})
                return

            if self.path == "/api/classes/join":
                self._require_user_or_write(current_user)
                if current_user is None:
                    return
                if current_user["role"] != "student":
                    self._write_json(403, {"message": "Only students can join classes."})
                    return
                join_code = str(payload.get("joinCode", "")).strip()
                if not join_code:
                    self._write_json(400, {"message": "Join code is required."})
                    return
                joined = store.join_class(join_code=join_code, student_username=current_user["username"])
                if joined is None:
                    self._write_json(404, {"message": "Join code not found."})
                    return
                self._write_json(200, {"class": joined})
                return

            if self.path != "/api/command":
                self._write_json(404, {"message": "Not found"})
                return

            self._require_user_or_write(current_user)
            if current_user is None:
                return

            service = self._build_service()
            response = service.execute(
                str(payload.get("input", "")),
                user_id=current_user["username"],
                context=payload.get("context") or {},
            )
            self._write_json(200 if response.success else 400, asdict(response))
        except json.JSONDecodeError:
            self._write_json(400, {"message": "Invalid JSON payload."})
        except Exception as error:  # pragma: no cover
            self._write_json(500, {"message": f"Internal server error: {error}"})

    def log_message(self, format, *args):  # type: ignore[override]
        return

    def _write_json(self, status_code: int, payload: dict, *, set_cookie: str | None = None) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if set_cookie:
            self.send_header("Set-Cookie", set_cookie)
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-GrammarDSL-User-Id")
        self.send_header("Access-Control-Allow-Credentials", "true")

    def _resolve_current_user(self, store: UserProfileStore) -> dict[str, str] | None:
        header_user = store.get_user_by_username(self.headers.get("X-GrammarDSL-User-Id"))
        if header_user is not None:
            return header_user

        cookie_header = self.headers.get("Cookie", "")
        if not cookie_header:
            return None

        cookies = SimpleCookie()
        cookies.load(cookie_header)
        session_cookie = cookies.get("grammardsl_session")
        if session_cookie is None:
            return None

        return store.get_user_by_session(session_cookie.value)

    def _handle_login(self, payload: dict) -> None:
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        store = self._build_store()
        user = store.authenticate_user(username, password)
        if user is None:
            self._write_json(401, {"message": "Invalid username or password."})
            return

        session_token = store.create_session(user["username"])
        cookie = f"grammardsl_session={session_token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=31536000"
        self._write_json(
            200,
            {
                "success": True,
                "message": f'Logged in as {user["display_name"]}.',
                "user": user,
            },
            set_cookie=cookie,
        )

    def _handle_logout(self) -> None:
        cookie_header = self.headers.get("Cookie", "")
        if cookie_header:
            cookies = SimpleCookie()
            cookies.load(cookie_header)
            session_cookie = cookies.get("grammardsl_session")
            if session_cookie is not None:
                store = self._build_store()
                store.delete_session(session_cookie.value)

        self._write_json(
            200,
            {
                "success": True,
                "message": "Logged out successfully.",
            },
            set_cookie="grammardsl_session=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0",
        )

    def _handle_register(self, payload: dict) -> None:
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        display_name = str(payload.get("displayName", "")).strip()
        if not username or not password:
            self._write_json(400, {"message": "Username and password are required."})
            return
        store = self._build_store()
        try:
            user = store.create_demo_student(username=username, password=password, display_name=display_name or username)
        except ValueError as error:
            self._write_json(400, {"message": str(error)})
            return
        self._write_json(
            200,
            {
                "success": True,
                "message": "Demo student account created. You can log in right away.",
                "user": user,
            },
        )

    def _require_user_or_write(self, current_user: dict[str, str] | None) -> None:
        if current_user is None:
            self._write_json(401, {"message": "Please log in first."})


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), GrammarDSLRequestHandler)
    print(f"GrammarDSL server is running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
