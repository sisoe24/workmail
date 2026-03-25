from __future__ import annotations

from http.server import BaseHTTPRequestHandler

from workmail.api import handle_clock_request


class handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        status, response_body = handle_clock_request(
            method="POST",
            headers=self.headers,
            body=body,
        )
        self._send_json(status, response_body)

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        status, response_body = handle_clock_request(
            method="GET",
            headers=self.headers,
            body=b"",
        )
        self._send_json(status, response_body)

    def _send_json(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
