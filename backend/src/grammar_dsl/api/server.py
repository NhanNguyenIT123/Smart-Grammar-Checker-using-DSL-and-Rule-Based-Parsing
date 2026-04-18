from __future__ import annotations

import json
from http.cookies import SimpleCookie
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from grammar_dsl.data import clear_repository_cache
from grammar_dsl.personalization import UserProfileStore
from grammar_dsl.preprocessing import load_pipeline_report
from grammar_dsl.services import CommandService


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

        if self.path == "/api/help":
            if current_user is None:
                self._write_json(401, {"message": "Please log in first."})
                return
            service = self._build_service()
            self._write_json(200, asdict(service.execute("help", user_id=current_user["username"])))
            return

        if self.path == "/api/pipeline":
            self._write_json(200, load_pipeline_report())
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
                self._write_json(
                    200,
                    {
                        "success": True,
                        "message": "Demo registration is disabled. Use one of the sample accounts to log in.",
                    },
                )
                return

            if self.path != "/api/command":
                self._write_json(404, {"message": "Not found"})
                return

            store = self._build_store()
            current_user = self._resolve_current_user(store)
            if current_user is None:
                self._write_json(401, {"message": "Please log in first."})
                return

            service = self._build_service()
            response = service.execute(str(payload.get("input", "")), user_id=current_user["username"])
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


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), GrammarDSLRequestHandler)
    print(f"GrammarDSL server is running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
