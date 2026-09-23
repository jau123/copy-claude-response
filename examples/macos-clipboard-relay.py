#!/usr/bin/env python3
"""Small localhost clipboard relay for remote SSH Claude Code sessions.

Run this on macOS, then expose it to the remote host with SSH RemoteForward.
The relay only listens on 127.0.0.1 and expects the first input line to match
the shared token file before writing the remaining payload to pbcopy.
"""

import argparse
import hmac
import os
import socketserver
import subprocess
from pathlib import Path


class ClipboardHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = bytearray()
        while len(data) <= self.server.max_bytes:
            chunk = self.request.recv(65536)
            if not chunk:
                break
            data.extend(chunk)

        if len(data) > self.server.max_bytes:
            self.request.sendall(b"ERR too large\n")
            return

        token, sep, payload = bytes(data).partition(b"\n")
        expected = self.server.token_file.read_text(encoding="utf-8").strip().encode()
        if not sep or not hmac.compare_digest(token.strip(), expected):
            self.request.sendall(b"ERR unauthorized\n")
            return

        subprocess.run(["/usr/bin/pbcopy"], input=payload, check=True)
        self.request.sendall(b"OK\n")


class ClipboardServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=49352)
    parser.add_argument(
        "--token-file",
        default="~/.copy-claude-response-relay-token",
        help="File containing the shared relay token",
    )
    parser.add_argument("--max-bytes", type=int, default=20 * 1024 * 1024)
    args = parser.parse_args()

    token_file = Path(os.path.expanduser(args.token_file))
    if not token_file.exists():
        raise SystemExit(f"token file not found: {token_file}")

    with ClipboardServer((args.host, args.port), ClipboardHandler) as server:
        server.token_file = token_file
        server.max_bytes = args.max_bytes
        server.serve_forever()


if __name__ == "__main__":
    main()
