"""Lightweight, zero-dependency in-process ASGI Test Client for FastAPI testing."""

import asyncio
import json
from typing import Dict, Any, Optional, Tuple


class ASGIResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body: bytes):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def json(self) -> Any:
        return json.loads(self.body.decode("utf-8"))

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")


class ASGITestClient:
    """Invokes ASGI applications asynchronously in-process without network overhead."""

    def __init__(self, app):
        self.app = app

    def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Any] = None,
        content: Optional[bytes] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ASGIResponse:
        return asyncio.run(self._async_request(method, path, headers, json_data, content, query_params))

    async def _async_request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Any] = None,
        content: Optional[bytes] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> ASGIResponse:
        req_headers = {k.lower(): v for k, v in (headers or {}).items()}
        
        body_bytes = b""
        if json_data is not None:
            body_bytes = json.dumps(json_data).encode("utf-8")
            req_headers["content-type"] = "application/json"
        elif content is not None:
            body_bytes = content

        req_headers["content-length"] = str(len(body_bytes))

        # Query string
        query_string = b""
        if query_params:
            from urllib.parse import urlencode
            query_string = urlencode(query_params).encode("ascii")

        raw_headers = [
            (k.encode("latin1"), v.encode("latin1"))
            for k, v in req_headers.items()
        ]

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method.upper(),
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": query_string,
            "headers": raw_headers,
            "client": ("127.0.0.1", 54321),
            "server": ("testserver", 80),
        }

        response_status = 200
        response_headers = {}
        response_chunks = []

        request_sent = False

        async def receive():
            nonlocal request_sent
            if not request_sent:
                request_sent = True
                return {
                    "type": "http.request",
                    "body": body_bytes,
                    "more_body": False
                }
            # Return disconnect on subsequent reads
            return {"type": "http.disconnect"}

        async def send(message):
            nonlocal response_status, response_headers, response_chunks
            if message["type"] == "http.response.start":
                response_status = message["status"]
                for k, v in message.get("headers", []):
                    response_headers[k.decode("latin1").lower()] = v.decode("latin1")
            elif message["type"] == "http.response.body":
                response_chunks.append(message.get("body", b""))

        await self.app(scope, receive, send)
        full_body = b"".join(response_chunks)
        return ASGIResponse(response_status, response_headers, full_body)

    def get(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> ASGIResponse:
        return self.request("GET", path, headers=headers, query_params=params)

    def post(self, path: str, headers: Optional[Dict[str, str]] = None, json: Optional[Any] = None, data: Optional[bytes] = None) -> ASGIResponse:
        return self.request("POST", path, headers=headers, json_data=json, content=data)

    def delete(self, path: str, headers: Optional[Dict[str, str]] = None) -> ASGIResponse:
        return self.request("DELETE", path, headers=headers)
