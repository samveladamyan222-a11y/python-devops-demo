import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

APP_NAME = "python-devops-demo"
APP_VERSION = "2.0.0"

START_TIME = time.time()
REQUEST_COUNT = 0

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

PORT = int(os.environ.get("PORT", "8000"))


# ==========================================
# HELPERS
# ==========================================

def uptime_seconds():
    return int(time.time() - START_TIME)


def current_timestamp():
    return datetime.now(timezone.utc).isoformat()


def json_response(data):
    return json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    ).encode("utf-8")


def environment_name():
    return os.environ.get(
        "ENVIRONMENT",
        os.environ.get(
            "ENV",
            "production"
        )
    )


# ==========================================
# REQUEST HANDLER
# ==========================================

class DevOpsHandler(BaseHTTPRequestHandler):

    server_version = "PythonDevOps/2.0"

    # --------------------------------------
    # COMMON RESPONSE HEADERS
    # --------------------------------------

    def send_common_headers(
        self,
        content_type="text/html; charset=utf-8",
        content_length=None
    ):
        self.send_header(
            "Content-Type",
            content_type
        )

        if content_length is not None:
            self.send_header(
                "Content-Length",
                str(content_length)
            )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.send_header(
            "X-Content-Type-Options",
            "nosniff"
        )

        self.send_header(
            "X-Frame-Options",
            "SAMEORIGIN"
        )

        self.send_header(
            "Referrer-Policy",
            "strict-origin-when-cross-origin"
        )

        self.end_headers()

    # --------------------------------------
    # SEND BYTES
    # --------------------------------------

    def send_bytes(
        self,
        content,
        content_type="text/html; charset=utf-8",
        status=200
    ):

        self.send_response(status)

        self.send_common_headers(
            content_type=content_type,
            content_length=len(content)
        )

        if self.command != "HEAD":
            self.wfile.write(content)

    # --------------------------------------
    # SEND JSON
    # --------------------------------------

    def send_json(
        self,
        data,
        status=200
    ):

        content = json_response(data)

        self.send_bytes(
            content,
            content_type="application/json; charset=utf-8",
            status=status
        )

    # --------------------------------------
    # GET
    # --------------------------------------

    def do_GET(self):

        global REQUEST_COUNT

        REQUEST_COUNT += 1

        path = urlparse(
            self.path
        ).path

        # ==============================
        # HOME PAGE
        # ==============================

       if path == "/":
    self.send_json(
        {
            "status": "ok",
            "service": APP_NAME,
            "message": "Python DevOps Demo is running"
        }
    )
    return
           

        # ==============================
        # HEALTH CHECK
        # ==============================

        if path == "/health":

            self.send_json(
                {
                    "status": "ok",
                    "service": APP_NAME,
                    "version": APP_VERSION,
                    "timestamp": current_timestamp(),
                    "uptime_seconds": uptime_seconds()
                }
            )

            return

        # ==============================
        # API STATUS
        # ==============================

        if path == "/api/status":

            self.send_json(
                {
                    "status": "ok",
                    "service": APP_NAME,
                    "version": APP_VERSION,
                    "port": PORT,
                    "uptime_seconds": uptime_seconds(),
                    "request_count": REQUEST_COUNT,
                    "timestamp": current_timestamp()
                }
            )

            return

        # ==============================
        # API INFO
        # ==============================

        if path == "/api/info":

            self.send_json(
                {
                    "application": APP_NAME,
                    "service": APP_NAME,
                    "version": APP_VERSION,
                    "python_version": (
                        f"{sys.version_info.major}."
                        f"{sys.version_info.minor}."
                        f"{sys.version_info.micro}"
                    ),
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "architecture": platform.machine(),
                    "environment": environment_name(),
                    "hostname": platform.node(),
                    "port": PORT,
                    "uptime_seconds": uptime_seconds(),
                    "timestamp": current_timestamp()
                }
            )

            return

        # ==============================
        # API METRICS
        # ==============================

        if path == "/api/metrics":

            self.send_json(
                {
                    "requests": REQUEST_COUNT,
                    "uptime_seconds": uptime_seconds(),
                    "started_at": datetime.fromtimestamp(
                        START_TIME,
                        tz=timezone.utc
                    ).isoformat(),
                    "timestamp": current_timestamp()
                }
            )

            return

        # ==============================
        # STATIC FILES
        # ==============================

        if path.startswith("/static/"):

            relative_path = path[
                len("/static/"):
            ]

            file_path = (
                STATIC_DIR /
                relative_path
            ).resolve()

            # Security protection:
            # prevent access outside static/
            try:
                file_path.relative_to(
                    STATIC_DIR.resolve()
                )
            except ValueError:

                self.send_json(
                    {
                        "status": "error",
                        "message": "Forbidden"
                    },
                    status=403
                )

                return

            content_type = (
                self.get_content_type(
                    file_path
                )
            )

            self.serve_file(
                file_path,
                content_type
            )

            return

        # ==============================
        # 404
        # ==============================

        if path.startswith("/api/"):

            self.send_json(
                {
                    "status": "error",
                    "message": "API endpoint not found",
                    "path": path
                },
                status=404
            )

            return

        self.send_json(
            {
                "status": "error",
                "message": "Not found",
                "path": path
            },
            status=404
        )

    # --------------------------------------
    # HEAD
    # --------------------------------------

    def do_HEAD(self):

        path = urlparse(
            self.path
        ).path

        if path == "/":

            self.serve_file(
                TEMPLATE_DIR / "index.html",
                "text/html; charset=utf-8"
            )

            return

        if path.startswith("/static/"):

            relative_path = path[
                len("/static/"):
            ]

            file_path = (
                STATIC_DIR /
                relative_path
            ).resolve()

            try:
                file_path.relative_to(
                    STATIC_DIR.resolve()
                )
            except ValueError:

                self.send_response(403)
                self.end_headers()
                return

            self.serve_file(
                file_path,
                self.get_content_type(
                    file_path
                )
            )

            return

        self.send_response(404)
        self.end_headers()

    # --------------------------------------
    # FILE SERVER
    # --------------------------------------

    def serve_file(
        self,
        file_path,
        content_type
    ):

        file_path = Path(file_path)

        if not file_path.exists():

            self.send_json(
                {
                    "status": "error",
                    "message": "File not found"
                },
                status=404
            )

            return

        if not file_path.is_file():

            self.send_json(
                {
                    "status": "error",
                    "message": "Not a file"
                },
                status=404
            )

            return

        try:

            content = file_path.read_bytes()

        except OSError:

            self.send_json(
                {
                    "status": "error",
                    "message": "Unable to read file"
                },
                status=500
            )

            return

        self.send_bytes(
            content,
            content_type=content_type,
            status=200
        )

    # --------------------------------------
    # CONTENT TYPE
    # --------------------------------------

    @staticmethod
    def get_content_type(file_path):

        suffix = (
            Path(file_path)
            .suffix
            .lower()
        )

        content_types = {

            ".html":
                "text/html; charset=utf-8",

            ".css":
                "text/css; charset=utf-8",

            ".js":
                "application/javascript; charset=utf-8",

            ".json":
                "application/json; charset=utf-8",

            ".txt":
                "text/plain; charset=utf-8",

            ".svg":
                "image/svg+xml",

            ".png":
                "image/png",

            ".jpg":
                "image/jpeg",

            ".jpeg":
                "image/jpeg",

            ".webp":
                "image/webp",

            ".ico":
                "image/x-icon"
        }

        return content_types.get(
            suffix,
            "application/octet-stream"
        )

    # --------------------------------------
    # LOGGING
    # --------------------------------------

    def log_message(
        self,
        format_string,
        *args
    ):

        print(
            f"[HTTP] {self.address_string()} "
            f"- {format_string % args}",
            flush=True
        )


# ==========================================
# SERVER STARTUP
# ==========================================

def main():

    print(
        "=" * 60,
        flush=True
    )

    print(
        "Python DevOps Demo",
        flush=True
    )

    print(
        "=" * 60,
        flush=True
    )

    print(
        f"Application: {APP_NAME}",
        flush=True
    )

    print(
        f"Version: {APP_VERSION}",
        flush=True
    )

    print(
        f"Python: {sys.version.split()[0]}",
        flush=True
    )

    print(
        f"Platform: {platform.system()}",
        flush=True
    )

    print(
        f"Environment: {environment_name()}",
        flush=True
    )

    print(
        f"Port: {PORT}",
        flush=True
    )

    print(
        "Health: /health",
        flush=True
    )

    print(
        "Status: /api/status",
        flush=True
    )

    print(
        "Info: /api/info",
        flush=True
    )

    print(
        "Metrics: /api/metrics",
        flush=True
    )

    print(
        "=" * 60,
        flush=True
    )

    server = ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        DevOpsHandler
    )

    try:

        print(
            f"Server listening on 0.0.0.0:{PORT}",
            flush=True
        )

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nServer stopped.",
            flush=True
        )

    finally:

        server.server_close()


if __name__ == "__main__":
    main()

    

      
