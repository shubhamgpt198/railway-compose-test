#!/usr/bin/env python3
"""Tiny JSON API for the compose deploy test."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8000"))


def _json(data: dict) -> bytes:
    return (json.dumps(data) + "\n").encode()


def _log(message: str) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    print(f"[api {now}] {message}", flush=True)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        _log(f"{self.address_string()} {fmt % args}")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        path = self.path.split("?", 1)[0]
        _log(
            f"{self.command} {path} from {self.address_string()} -> {status} "
            f"({len(body)} bytes)"
        )
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        _log(f"received {self.command} {self.path} from {self.address_string()}")
        if path == "/api/health":
            self._send(200, _json({"status": "ok", "service": "api"}), "application/json")
            return
        if path == "/api/hello":
            self._send(
                200,
                _json({"message": "hello from the backend", "port": PORT}),
                "application/json",
            )
            return
        self._send(404, _json({"detail": "not found"}), "application/json")


def main() -> None:
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    _log(f"listening on 0.0.0.0:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
