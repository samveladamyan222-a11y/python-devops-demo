import json
import os
import threading
import time
import urllib.request

import app


def start_test_server():
    server = app.ThreadingHTTPServer(
        ("127.0.0.1", 0),
        app.DevOpsHandler,
    )

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    return server, thread


def get_json(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.status, json.loads(response.read().decode())


def test_health():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]
        status, data = get_json(
            f"http://127.0.0.1:{port}/health"
        )

        assert status == 200
        assert data["status"] == "ok"
        assert data["service"] == app.APP_NAME
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_api_status():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]
        status, data = get_json(
            f"http://127.0.0.1:{port}/api/status"
        )

        assert status == 200
        assert data["status"] == "ok"
        assert data["version"] == app.APP_VERSION
        assert "uptime_seconds" in data
        assert "request_count" in data
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_api_info():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]
        status, data = get_json(
            f"http://127.0.0.1:{port}/api/info"
        )

        assert status == 200
        assert data["application"] == app.APP_NAME
        assert "python_version" in data
        assert "platform" in data
        assert "architecture" in data
        assert "environment" in data
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_api_metrics():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]
        status, data = get_json(
            f"http://127.0.0.1:{port}/api/metrics"
        )

        assert status == 200
        assert "requests" in data
        assert "uptime_seconds" in data
        assert "started_at" in data
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_home_page():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]

        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/",
            timeout=5,
        ) as response:
            body = response.read().decode()

        assert response.status == 200
        assert "<html" in body.lower()
        assert "Python DevOps" in body
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_static_css():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]

        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/static/style.css",
            timeout=5,
        ) as response:
            body = response.read().decode()

        assert response.status == 200
        assert len(body) > 100
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_static_js():
    server, thread = start_test_server()

    try:
        port = server.server_address[1]

        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/static/app.js",
            timeout=5,
        ) as response:
            body = response.read().decode()

        assert response.status == 200
        assert len(body) > 100
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
