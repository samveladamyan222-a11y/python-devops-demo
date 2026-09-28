from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os
import platform
import sys
import time
from datetime import datetime, timezone


APP_NAME = "Python DevOps Platform"
APP_VERSION = "3.0.0"
SERVICE_NAME = "python-devops-demo"

PORT = int(os.environ.get("PORT", "8000"))
START_TIME = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(SERVICE_NAME)


HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Python DevOps Platform</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #07111f;
    color: #f8fafc;
    line-height: 1.6;
}

a {
    color: inherit;
    text-decoration: none;
}

.container {
    width: min(1180px, calc(100% - 40px));
    margin: 0 auto;
}


/* NAVBAR */

.navbar {
    position: sticky;
    top: 0;
    z-index: 1000;

    background: rgba(7, 17, 31, 0.88);
    backdrop-filter: blur(16px);

    border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}

.nav-inner {
    min-height: 72px;

    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
}

.logo {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.logo span {
    color: #38bdf8;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 24px;

    color: #cbd5e1;
    font-size: 14px;
}

.nav-links a:hover {
    color: #38bdf8;
}


/* HERO */

.hero {
    padding: 100px 0 80px;

    background:
        radial-gradient(
            circle at 20% 20%,
            rgba(56, 189, 248, 0.16),
            transparent 35%
        ),
        radial-gradient(
            circle at 80% 30%,
            rgba(99, 102, 241, 0.14),
            transparent 35%
        );
}

.hero-grid {
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 60px;
    align-items: center;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 9px;

    padding: 8px 13px;

    border-radius: 999px;

    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.25);

    color: #86efac;

    font-size: 13px;
    font-weight: 700;

    margin-bottom: 25px;
}

.badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 12px #22c55e;
}

.hero h1 {
    font-size: clamp(45px, 7vw, 78px);
    line-height: 0.98;
    letter-spacing: -4px;

    max-width: 800px;

    margin-bottom: 28px;
}

.hero h1 span {
    color: #38bdf8;
}

.hero-description {
    max-width: 650px;

    color: #94a3b8;

    font-size: 19px;

    margin-bottom: 35px;
}

.buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
}

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    min-height: 48px;

    padding: 0 22px;

    border-radius: 11px;

    font-weight: 700;
    font-size: 14px;

    transition: 0.2s ease;
}

.btn-primary {
    background: #38bdf8;
    color: #03111c;
}

.btn-primary:hover {
    transform: translateY(-2px);
    background: #7dd3fc;
}

.btn-secondary {
    border: 1px solid #334155;
    color: #e2e8f0;
}

.btn-secondary:hover {
    background: #111c2d;
}


/* TERMINAL */

.terminal {
    background: #020617;

    border: 1px solid #1e293b;

    border-radius: 18px;

    overflow: hidden;

    box-shadow:
        0 25px 80px rgba(0, 0, 0, 0.35);
}

.terminal-header {
    display: flex;
    align-items: center;
    gap: 7px;

    padding: 13px 16px;

    background: #0f172a;

    border-bottom: 1px solid #1e293b;
}

.terminal-dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
    background: #475569;
}

.terminal-title {
    margin-left: 8px;
    color: #64748b;
    font-size: 12px;
}

.terminal-body {
    padding: 25px;

    font-family:
        "SFMono-Regular",
        Consolas,
        monospace;

    font-size: 13px;

    color: #cbd5e1;
}

.line {
    margin-bottom: 12px;
}

.green {
    color: #4ade80;
}

.blue {
    color: #38bdf8;
}

.purple {
    color: #a78bfa;
}

.gray {
    color: #64748b;
}


/* SECTIONS */

section {
    padding: 95px 0;
}

.section-header {
    max-width: 700px;
    margin-bottom: 50px;
}

.section-label {
    color: #38bdf8;

    font-size: 13px;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: 2px;

    margin-bottom: 12px;
}

.section-title {
    font-size: clamp(32px, 5vw, 50px);

    line-height: 1.05;

    letter-spacing: -2px;

    margin-bottom: 18px;
}

.section-description {
    color: #94a3b8;
    font-size: 17px;
}


/* CARDS */

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    padding: 28px;

    background: #0b1729;

    border: 1px solid #1e293b;

    border-radius: 18px;

    transition: 0.25s ease;
}

.card:hover {
    transform: translateY(-5px);

    border-color: rgba(56, 189, 248, 0.4);

    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.2);
}

.card-icon {
    font-size: 28px;
    margin-bottom: 18px;
}

.card h3 {
    font-size: 19px;
    margin-bottom: 10px;
}

.card p {
    color: #94a3b8;
    font-size: 14px;
}


/* STACK */

.stack {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.tech {
    padding: 10px 15px;

    border: 1px solid #334155;

    background: #0b1729;

    border-radius: 10px;

    color: #cbd5e1;

    font-size: 14px;
}


/* PROJECT */

.project {
    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 25px;
}

.project-box {
    background: #0b1729;

    border: 1px solid #1e293b;

    border-radius: 18px;

    padding: 30px;
}

.project-box h3 {
    font-size: 23px;
    margin-bottom: 12px;
}

.project-box p {
    color: #94a3b8;
    margin-bottom: 20px;
}


/* STATUS */

.status-grid {
    display: grid;

    grid-template-columns: repeat(4, 1fr);

    gap: 15px;
}

.status-card {
    padding: 22px;

    background: #0b1729;

    border: 1px solid #1e293b;

    border-radius: 15px;
}

.status-card small {
    color: #64748b;

    display: block;

    margin-bottom: 6px;
}

.status-value {
    font-weight: 800;
    font-size: 18px;
}

.online {
    color: #4ade80;
}


/* CONTACT */

.contact {
    text-align: center;

    padding: 70px 30px;

    border-radius: 25px;

    background:
        radial-gradient(
            circle at center,
            rgba(56, 189, 248, 0.14),
            transparent 60%
        );

    border: 1px solid #1e293b;
}

.contact p {
    max-width: 650px;

    margin: 0 auto 30px;

    color: #94a3b8;
}


/* FOOTER */

footer {
    padding: 35px 0;

    border-top: 1px solid #1e293b;

    color: #64748b;

    font-size: 13px;
}

.footer-inner {
    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 20px;
}


/* MOBILE */

@media (max-width: 900px) {

    .hero-grid {
        grid-template-columns: 1fr;
    }

    .cards {
        grid-template-columns: 1fr;
    }

    .status-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .project {
        grid-template-columns: 1fr;
    }

    .nav-links {
        display: none;
    }

}

@media (max-width: 600px) {

    .container {
        width: min(100% - 28px, 1180px);
    }

    .hero {
        padding-top: 70px;
    }

    .hero h1 {
        letter-spacing: -2px;
    }

    section {
        padding: 70px 0;
    }

    .status-grid {
        grid-template-columns: 1fr;
    }

    .footer-inner {
        flex-direction: column;
        align-items: flex-start;
    }

}

</style>
</head>


<body>


<nav class="navbar">

<div class="container nav-inner">

<a href="/" class="logo">
Python<span>DevOps</span>
</a>

<div class="nav-links">

<a href="#about">About</a>
<a href="#services">Services</a>
<a href="#projects">Projects</a>
<a href="#status">Status</a>

</div>

</div>

</nav>


<main>


<section class="hero">

<div class="container hero-grid">


<div>

<div class="badge">

<span class="badge-dot"></span>

SYSTEM OPERATIONAL

</div>


<h1>

Python infrastructure.

<span>Built to run.</span>

</h1>


<p class="hero-description">

A production-style Python DevOps platform demonstrating
containerization, automated testing, CI/CD, APIs and cloud deployment.

</p>


<div class="buttons">

<a class="btn btn-primary" href="#projects">
View project
</a>

<a class="btn btn-secondary" href="#services">
Explore services
</a>

</div>

</div>


<div class="terminal">

<div class="terminal-header">

<span class="terminal-dot"></span>
<span class="terminal-dot"></span>
<span class="terminal-dot"></span>

<span class="terminal-title">
server@devops
</span>

</div>


<div class="terminal-body">

<div class="line">
<span class="gray">$</span>
<span class="blue">python</span> app.py
</div>

<div class="line green">
✓ Server started
</div>

<div class="line">
PORT=<span class="purple">dynamic</span>
</div>

<div class="line">
ENV=<span class="purple">production</span>
</div>

<div class="line green">
✓ API available
</div>

<div class="line green">
✓ Docker ready
</div>

<div class="line green">
✓ CI/CD configured
</div>

<div class="line green">
✓ Cloud deployment active
</div>

<div class="line">
<span class="gray">$</span> systemctl status application
</div>

<div class="line green">
● active (running)
</div>

</div>

</div>


</div>

</section>


<section id="about">

<div class="container">

<div class="section-header">

<div class="section-label">
01 / About
</div>

<h2 class="section-title">
Modern DevOps workflow
</h2>

<p class="section-description">

This project demonstrates a complete path from source code
to a live cloud application.

</p>

</div>


<div class="cards">

<div class="card">

<div class="card-icon">🐍</div>

<h3>Python</h3>

<p>
Lightweight HTTP application with JSON APIs,
health endpoints and production-friendly configuration.
</p>

</div>


<div class="card">

<div class="card-icon">🐳</div>

<h3>Docker</h3>

<p>
The application is packaged into a reproducible
container image for consistent deployments.
</p>

</div>


<div class="card">

<div class="card-icon">⚙️</div>

<h3>CI/CD</h3>

<p>
Automated testing and Docker image builds
can run through GitHub Actions.
</p>

</div>

</div>

</div>

</section>


<section id="services">

<div class="container">

<div class="section-header">

<div class="section-label">
02 / Services
</div>

<h2 class="section-title">
What this platform demonstrates
</h2>

<p class="section-description">
Core capabilities used in modern small-scale DevOps deployments.
</p>

</div>


<div class="cards">

<div class="card">

<div class="card-icon">🚀</div>

<h3>Deployment</h3>

<p>
Deploy Python applications to cloud infrastructure
using containerized workflows.
</p>

</div>


<div class="card">

<div class="card-icon">🔄</div>

<h3>CI/CD</h3>

<p>
Automate testing, Docker builds and delivery
after changes are pushed to GitHub.
</p>

</div>


<div class="card">

<div class="card-icon">📊</div>

<h3>Monitoring</h3>

<p>
Expose health and information endpoints
that can be monitored by infrastructure tools.
</p>

</div>


<div class="card">

<div class="card-icon">🔐</div>

<h3>Configuration</h3>

<p>
Use environment variables and production-safe
configuration instead of hardcoded infrastructure values.
</p>

</div>


<div class="card">

<div class="card-icon">🧪</div>

<h3>Testing</h3>

<p>
Automated tests verify the application's important
HTTP endpoints before deployment.
</p>

</div>


<div class="card">

<div class="card-icon">☁️</div>

<h3>Cloud Ready</h3>

<p>
Designed to run with cloud platforms that provide
a dynamic PORT environment variable.
</p>

</div>

</div>

</div>

</section>


<section>

<div class="container">

<div class="section-header">

<div class="section-label">
03 / Technology
</div>

<h2 class="section-title">
Technology stack
</h2>

</div>


<div class="stack">

<div class="tech">Python</div>
<div class="tech">HTTP Server</div>
<div class="tech">REST API</div>
<div class="tech">Docker</div>
<div class="tech">GitHub</div>
<div class="tech">GitHub Actions</div>
<div class="tech">GHCR</div>
<div class="tech">Render</div>
<div class="tech">CI/CD</div>
<div class="tech">Linux</div>

</div>

</div>

</section>


<section id="projects">

<div class="container">

<div class="section-header">

<div class="section-label">
04 / Project
</div>

<h2 class="section-title">
Python DevOps Demo
</h2>

<p class="section-description">

A complete demonstration project connecting development,
testing, containerization and cloud deployment.

</p>

</div>


<div class="project">

<div class="project-box">

<h3>Application</h3>

<p>
Python backend serving a responsive web interface
and machine-readable API endpoints.
</p>

<div class="stack">

<div class="tech">Python</div>
<div class="tech">JSON API</div>
<div class="tech">HTTP</div>

</div>

</div>


<div class="project-box">

<h3>Infrastructure</h3>

<p>
Docker container connected to GitHub-based workflows
and deployed to a public cloud service.
</p>

<div class="stack">

<div class="tech">Docker</div>
<div class="tech">GitHub Actions</div>
<div class="tech">Render</div>

</div>

</div>

</div>

</div>

</section>


<section id="status">

<div class="container">

<div class="section-header">

<div class="section-label">
05 / Live status
</div>

<h2 class="section-title">
System status
</h2>

<p class="section-description">

The values below are loaded from the running application.

</p>

</div>


<div class="status-grid">

<div class="status-card">

<small>Application</small>

<div class="status-value">
Python DevOps Platform
</div>

</div>


<div class="status-card">

<small>Version</small>

<div class="status-value">
3.0.0
</div>

</div>


<div class="status-card">

<small>Service</small>

<div class="status-value">
python-devops-demo
</div>

</div>


<div class="status-card">

<small>Health</small>

<div class="status-value online" id="health">
Checking...
</div>

</div>

</div>

</div>

</section>


<section>

<div class="container">

<div class="contact">

<div class="section-label">
06 / API
</div>

<h2 class="section-title">
Developer API
</h2>

<p>
This application exposes machine-readable endpoints
for health checks, status information and runtime details.
</p>

<div class="buttons" style="justify-content:center;">

<a class="btn btn-primary" href="/api/status">
API Status
</a>

<a class="btn btn-secondary" href="/api/info">
System Info
</a>

</div>

</div>

</div>

</section>


</main>


<footer>

<div class="container footer-inner">

<div>
© 2026 Python DevOps Platform
</div>

<div>
Python • Docker • CI/CD • Cloud
</div>

</div>

</footer>


<script>

async function checkHealth() {

    const element = document.getElementById("health");

    try {

        const response = await fetch("/health");

        if (response.ok) {

            element.textContent = "ONLINE";
            element.className = "status-value online";

        } else {

            element.textContent = "DEGRADED";

        }

    } catch (error) {

        element.textContent = "OFFLINE";

    }

}

checkHealth();

setInterval(checkHealth, 30000);

</script>


</body>
</html>
"""


def json_response(data):
    return json.dumps(
        data,
        ensure_ascii=False
    ).encode("utf-8")


def send_bytes(handler, status, content_type, body):
    handler.send_response(status)

    handler.send_header(
        "Content-Type",
        content_type
    )

    handler.send_header(
        "Content-Length",
        str(len(body))
    )

    handler.send_header(
        "Cache-Control",
        "no-store"
    )

    handler.end_headers()

    if handler.command != "HEAD":
        handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):

    server_version = "PythonDevOps/3.0"

    def log_message(self, format_string, *args):
        logger.info(
            "%s - %s",
            self.address_string(),
            format_string % args
        )

    def do_HEAD(self):

        path = self.path.split("?")[0]

        if path == "/":
            send_bytes(
                self,
                200,
                "text/html; charset=utf-8",
                HTML.encode("utf-8")
            )

        elif path == "/health":
            send_bytes(
                self,
                200,
                "text/plain; charset=utf-8",
                b"ok"
            )

        elif path == "/api/status":

            data = {
                "status": "ok",
                "service": SERVICE_NAME,
                "version": APP_VERSION
            }

            send_bytes(
                self,
                200,
                "application/json; charset=utf-8",
                json_response(data)
            )

        elif path == "/api/info":

            data = {
                "application": APP_NAME,
                "service": SERVICE_NAME,
                "version": APP_VERSION,
                "python": platform.python_version(),
                "platform": platform.system(),
                "architecture": platform.machine(),
                "environment": os.environ.get(
                    "RENDER",
                    "local"
                )
            }

            send_bytes(
                self,
                200,
                "application/json; charset=utf-8",
                json_response(data)
            )

        else:
            send_bytes(
                self,
                404,
                "text/plain; charset=utf-8",
                b"Not Found"
            )

    def do_GET(self):

        path = self.path.split("?")[0]

        if path == "/":

            send_bytes(
                self,
                200,
                "text/html; charset=utf-8",
                HTML.encode("utf-8")
            )

        elif path == "/health":

            send_bytes(
                self,
                200,
                "text/plain; charset=utf-8",
                b"ok"
            )

        elif path == "/api/status":

            uptime = int(
                time.time() - START_TIME
            )

            data = {
                "status": "ok",
                "service": SERVICE_NAME,
                "version": APP_VERSION,
                "uptime_seconds": uptime,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat()
            }

            send_bytes(
                self,
                200,
                "application/json; charset=utf-8",
                json_response(data)
            )

        elif path == "/api/info":

            data = {
                "application": APP_NAME,
                "service": SERVICE_NAME,
                "version": APP_VERSION,
                "python": platform.python_version(),
                "platform": platform.system(),
                "architecture": platform.machine(),
                "port": PORT,
                "environment": os.environ.get(
                    "RENDER",
                    "local"
                )
            }

            send_bytes(
                self,
                200,
                "application/json; charset=utf-8",
                json_response(data)
            )

        else:

            body = b"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>404 - Not Found</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background: #07111f;
                        color: white;
                        text-align: center;
                        padding: 100px 20px;
                    }
                    a {
                        color: #38bdf8;
                    }
                </style>
            </head>
            <body>
                <h1>404</h1>
                <p>The requested page was not found.</p>
                <p><a href="/">Return home</a></p>
            </body>
            </html>
            """

            send_bytes(
                self,
                404,
                "text/html; charset=utf-8",
                body
            )


def main():

    server = HTTPServer(
        ("0.0.0.0", PORT),
        Handler
    )

    logger.info(
        "Starting %s version %s on port %s",
        APP_NAME,
        APP_VERSION,
        PORT
    )

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        logger.info("Server stopped")

    finally:

        server.server_close()


if __name__ == "__main__":
    main()
