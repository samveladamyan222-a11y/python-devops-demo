from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import json
import logging
import os
import platform


# ============================================================
# CONFIGURATION
# ============================================================

APP_NAME = "Python DevOps Platform"
APP_VERSION = "2.0.0"
SERVICE_NAME = "python-devops-demo"

PORT = int(os.environ.get("PORT", "8000"))


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# HTML WEBSITE
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <meta
        name="description"
        content="Professional Python, Docker and DevOps portfolio platform."
    >

    <meta
        name="theme-color"
        content="#0b1020"
    >

    <title>Python DevOps Platform</title>

    <style>

        /* =====================================================
           RESET
           ===================================================== */

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
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

            background:
                radial-gradient(
                    circle at top left,
                    #172554 0,
                    #0b1020 40%,
                    #050816 100%
                );

            color: #ffffff;
            min-height: 100vh;
            line-height: 1.6;
        }


        a {
            color: inherit;
            text-decoration: none;
        }


        button {
            font-family: inherit;
        }


        /* =====================================================
           NAVIGATION
           ===================================================== */

        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;

            backdrop-filter: blur(18px);

            background:
                rgba(5, 8, 22, 0.78);

            border-bottom:
                1px solid rgba(255, 255, 255, 0.08);
        }


        .nav-container {
            width: min(1180px, 92%);
            margin: auto;

            min-height: 72px;

            display: flex;
            align-items: center;
            justify-content: space-between;
        }


        .logo {
            font-size: 21px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }


        .logo span {
            color: #60a5fa;
        }


        .nav-links {
            display: flex;
            gap: 28px;
            list-style: none;
        }


        .nav-links a {
            color: #cbd5e1;
            font-size: 14px;
            transition: 0.25s;
        }


        .nav-links a:hover {
            color: #ffffff;
        }


        /* =====================================================
           GENERAL
           ===================================================== */

        .container {
            width: min(1180px, 92%);
            margin: auto;
        }


        section {
            padding: 100px 0;
        }


        .section-label {
            color: #60a5fa;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }


        .section-title {
            font-size: clamp(32px, 5vw, 48px);
            line-height: 1.1;
            margin-bottom: 18px;
        }


        .section-description {
            max-width: 680px;
            color: #94a3b8;
            font-size: 17px;
        }


        /* =====================================================
           HERO
           ===================================================== */

        .hero {
            min-height: calc(100vh - 72px);

            display: flex;
            align-items: center;

            position: relative;
            overflow: hidden;
        }


        .hero::before {
            content: "";

            position: absolute;

            width: 500px;
            height: 500px;

            right: -180px;
            top: -150px;

            background: #2563eb;

            filter: blur(150px);

            opacity: 0.18;
        }


        .hero-grid {
            display: grid;

            grid-template-columns:
                1.15fr
                0.85fr;

            gap: 60px;

            align-items: center;
        }


        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 9px;

            padding: 9px 15px;

            border-radius: 999px;

            background:
                rgba(34, 197, 94, 0.10);

            border:
                1px solid rgba(34, 197, 94, 0.25);

            color: #86efac;

            font-size: 13px;
            font-weight: 700;

            margin-bottom: 25px;
        }


        .status-dot {
            width: 8px;
            height: 8px;

            border-radius: 50%;

            background: #22c55e;

            box-shadow:
                0 0 14px #22c55e;
        }


        .hero h1 {
            font-size: clamp(48px, 7vw, 82px);

            line-height: 0.98;

            letter-spacing: -4px;

            margin-bottom: 25px;
        }


        .hero h1 span {
            background:
                linear-gradient(
                    90deg,
                    #60a5fa,
                    #a78bfa
                );

            -webkit-background-clip: text;
            background-clip: text;

            color: transparent;
        }


        .hero-text {
            color: #94a3b8;

            font-size: 19px;

            max-width: 650px;

            margin-bottom: 35px;
        }


        .hero-buttons {
            display: flex;
            gap: 14px;
            flex-wrap: wrap;
        }


        .btn {
            display: inline-flex;

            align-items: center;
            justify-content: center;

            min-height: 48px;

            padding: 0 22px;

            border-radius: 12px;

            font-weight: 700;

            font-size: 14px;

            transition:
                transform 0.2s,
                background 0.2s,
                border 0.2s;
        }


        .btn:hover {
            transform: translateY(-2px);
        }


        .btn-primary {
            background: #2563eb;
            color: #ffffff;

            box-shadow:
                0 12px 30px
                rgba(37, 99, 235, 0.25);
        }


        .btn-primary:hover {
            background: #3b82f6;
        }


        .btn-secondary {
            background:
                rgba(255, 255, 255, 0.05);

            border:
                1px solid rgba(255, 255, 255, 0.12);

            color: #ffffff;
        }


        .btn-secondary:hover {
            background:
                rgba(255, 255, 255, 0.09);
        }


        /* =====================================================
           TERMINAL CARD
           ===================================================== */

        .terminal {
            border:
                1px solid rgba(255, 255, 255, 0.10);

            background:
                rgba(15, 23, 42, 0.78);

            border-radius: 20px;

            overflow: hidden;

            box-shadow:
                0 30px 80px
                rgba(0, 0, 0, 0.35);
        }


        .terminal-header {
            height: 46px;

            display: flex;
            align-items: center;

            gap: 7px;

            padding: 0 16px;

            border-bottom:
                1px solid rgba(255, 255, 255, 0.07);
        }


        .terminal-dot {
            width: 10px;
            height: 10px;

            border-radius: 50%;

            background: #64748b;
        }


        .terminal-body {
            padding: 25px;

            font-family:
                "Courier New",
                monospace;

            font-size: 14px;

            color: #cbd5e1;

            min-height: 300px;
        }


        .terminal-line {
            margin-bottom: 12px;
        }


        .terminal-green {
            color: #4ade80;
        }


        .terminal-blue {
            color: #60a5fa;
        }


        .terminal-purple {
            color: #c084fc;
        }


        .terminal-gray {
            color: #64748b;
        }


        /* =====================================================
           STATS
           ===================================================== */

        .stats {
            display: grid;

            grid-template-columns:
                repeat(4, 1fr);

            gap: 18px;

            margin-top: 55px;
        }


        .stat-card {
            padding: 24px;

            border-radius: 18px;

            background:
                rgba(255, 255, 255, 0.045);

            border:
                1px solid rgba(255, 255, 255, 0.08);
        }


        .stat-number {
            font-size: 30px;
            font-weight: 800;

            margin-bottom: 5px;
        }


        .stat-text {
            color: #94a3b8;
            font-size: 13px;
        }


        /* =====================================================
           ABOUT
           ===================================================== */

        .about-grid {
            display: grid;

            grid-template-columns:
                1fr
                1fr;

            gap: 60px;

            margin-top: 45px;
        }


        .about-text {
            color: #94a3b8;
            font-size: 17px;
        }


        .about-text p {
            margin-bottom: 18px;
        }


        .skills {
            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 14px;
        }


        .skill {
            padding: 20px;

            border-radius: 16px;

            background:
                rgba(255, 255, 255, 0.045);

            border:
                1px solid rgba(255, 255, 255, 0.08);
        }


        .skill strong {
            display: block;
            margin-bottom: 5px;
        }


        .skill span {
            color: #94a3b8;
            font-size: 13px;
        }


        /* =====================================================
           SERVICES
           ===================================================== */

        .cards {
            display: grid;

            grid-template-columns:
                repeat(3, 1fr);

            gap: 18px;

            margin-top: 45px;
        }


        .card {
            padding: 30px;

            border-radius: 20px;

            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.065),
                    rgba(255, 255, 255, 0.025)
                );

            border:
                1px solid rgba(255, 255, 255, 0.08);

            transition:
                transform 0.25s,
                border 0.25s;
        }


        .card:hover {
            transform: translateY(-5px);

            border-color:
                rgba(96, 165, 250, 0.35);
        }


        .card-icon {
            font-size: 30px;
            margin-bottom: 20px;
        }


        .card h3 {
            margin-bottom: 10px;
            font-size: 20px;
        }


        .card p {
            color: #94a3b8;
            font-size: 14px;
        }


        /* =====================================================
           PROJECTS
           ===================================================== */

        .projects {
            display: grid;

            grid-template-columns:
                repeat(2, 1fr);

            gap: 18px;

            margin-top: 45px;
        }


        .project {
            padding: 28px;

            border-radius: 20px;

            background:
                rgba(255, 255, 255, 0.045);

            border:
                1px solid rgba(255, 255, 255, 0.08);
        }


        .project-top {
            display: flex;
            justify-content: space-between;

            gap: 15px;

            margin-bottom: 18px;
        }


        .project h3 {
            font-size: 21px;
        }


        .project-status {
            color: #86efac;

            font-size: 12px;
            font-weight: 700;
        }


        .project p {
            color: #94a3b8;

            font-size: 14px;

            margin-bottom: 20px;
        }


        .tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }


        .tag {
            padding: 6px 10px;

            border-radius: 8px;

            background:
                rgba(96, 165, 250, 0.10);

            color: #93c5fd;

            font-size: 11px;

            border:
                1px solid rgba(96, 165, 250, 0.15);
        }


        /* =====================================================
           STATUS
           ===================================================== */

        .status-panel {
            margin-top: 45px;

            padding: 30px;

            border-radius: 20px;

            background:
                rgba(255, 255, 255, 0.045);

            border:
                1px solid rgba(255, 255, 255, 0.08);
        }


        .status-row {
            display: flex;

            align-items: center;
            justify-content: space-between;

            padding: 16px 0;

            border-bottom:
                1px solid rgba(255, 255, 255, 0.07);
        }


        .status-row:last-child {
            border-bottom: none;
        }


        .status-name {
            color: #cbd5e1;
        }


        .status-value {
            color: #4ade80;
            font-weight: 700;
        }


        /* =====================================================
           CONTACT
           ===================================================== */

        .contact-box {
            margin-top: 45px;

            padding: 45px;

            border-radius: 24px;

            text-align: center;

            background:
                linear-gradient(
                    135deg,
                    rgba(37, 99, 235, 0.16),
                    rgba(124, 58, 237, 0.12)
                );

            border:
                1px solid rgba(96, 165, 250, 0.16);
        }


        .contact-box h2 {
            font-size: 34px;
            margin-bottom: 12px;
        }


        .contact-box p {
            color: #94a3b8;
            margin-bottom: 25px;
        }


        /* =====================================================
           FOOTER
           ===================================================== */

        footer {
            padding: 35px 0;

            border-top:
                1px solid rgba(255, 255, 255, 0.07);

            color: #64748b;

            font-size: 13px;
        }


        .footer-content {
            display: flex;

            justify-content: space-between;
            align-items: center;

            gap: 20px;
        }


        /* =====================================================
           RESPONSIVE
           ===================================================== */

        @media (max-width: 900px) {

            .hero-grid,
            .about-grid {
                grid-template-columns: 1fr;
            }


            .cards {
                grid-template-columns: 1fr 1fr;
            }


            .projects {
                grid-template-columns: 1fr;
            }


            .stats {
                grid-template-columns: 1fr 1fr;
            }

        }


        @media (max-width: 650px) {

            section {
                padding: 75px 0;
            }


            .nav-links {
                display: none;
            }


            .hero h1 {
                letter-spacing: -2px;
            }


            .cards,
            .skills,
            .stats {
                grid-template-columns: 1fr;
            }


            .contact-box {
                padding: 30px 20px;
            }


            .footer-content {
                flex-direction: column;
                text-align: center;
            }

        }

    </style>

</head>


<body>


<!-- =========================================================
     NAVIGATION
     ========================================================= -->

<nav class="navbar">

    <div class="nav-container">

        <a href="#home" class="logo">
            Dev<span>Ops</span>.Platform
        </a>

        <ul class="nav-links">

            <li>
                <a href="#about">About</a>
            </li>

            <li>
                <a href="#services">Services</a>
            </li>

            <li>
                <a href="#projects">Projects</a>
            </li>

            <li>
                <a href="#status">Status</a>
            </li>

            <li>
                <a href="#contact">Contact</a>
            </li>

        </ul>

    </div>

</nav>


<!-- =========================================================
     HERO
     ========================================================= -->

<main>

<section id="home" class="hero">

    <div class="container">

        <div class="hero-grid">

            <div>

                <div class="status-badge">

                    <span class="status-dot"></span>

                    SYSTEM ONLINE

                </div>


                <h1>

                    Build.

                    <br>

                    Deploy.

                    <br>

                    <span>Scale.</span>

                </h1>


                <p class="hero-text">

                    A professional Python and DevOps platform
                    built with Docker, GitHub Actions and
                    cloud deployment technology.

                </p>


                <div class="hero-buttons">

                    <a
                        href="#projects"
                        class="btn btn-primary"
                    >
                        View Projects
                    </a>


                    <a
                        href="/api/status"
                        class="btn btn-secondary"
                    >
                        Check API
                    </a>

                </div>

            </div>


            <div class="terminal">

                <div class="terminal-header">

                    <span class="terminal-dot"></span>
                    <span class="terminal-dot"></span>
                    <span class="terminal-dot"></span>

                </div>


                <div class="terminal-body">

                    <div class="terminal-line">

                        <span class="terminal-green">
                            $
                        </span>

                        python app.py

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-gray">
                            Starting application...
                        </span>

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-blue">
                            Docker
                        </span>

                        container started

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-purple">
                            GitHub Actions
                        </span>

                        CI/CD ready

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-blue">
                            Render
                        </span>

                        deployment active

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-green">
                            ✓ SERVER ONLINE
                        </span>

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-green">
                            ✓ HEALTH CHECK OK
                        </span>

                    </div>


                    <div class="terminal-line">

                        <span class="terminal-green">
                            ✓ APPLICATION READY
                        </span>

                    </div>

                </div>

            </div>

        </div>


        <div class="stats">

            <div class="stat-card">

                <div class="stat-number">
                    24/7
                </div>

                <div class="stat-text">
                    Cloud availability
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-number">
                    CI/CD
                </div>

                <div class="stat-text">
                    Automated workflow
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-number">
                    Docker
                </div>

                <div class="stat-text">
                    Containerized app
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-number">
                    API
                </div>

                <div class="stat-text">
                    REST endpoints
                </div>

            </div>

        </div>

    </div>

</section>


<!-- =========================================================
     ABOUT
     ========================================================= -->

<section id="about">

    <div class="container">

        <div class="section-label">
            About
        </div>

        <h2 class="section-title">
            Engineering with automation.
        </h2>

        <p class="section-description">

            This platform demonstrates a complete
            development and deployment workflow from
            source code to production.

        </p>


        <div class="about-grid">

            <div class="about-text">

                <p>
                    The application is written in Python and
                    runs as a lightweight HTTP service.
                </p>

                <p>
                    Docker provides a reproducible runtime
                    environment while GitHub Actions handles
                    automated testing and container builds.
                </p>

                <p>
                    The application is deployed to the cloud
                    and exposed through a public production URL.
                </p>

            </div>


            <div class="skills">

                <div class="skill">
                    <strong>Python</strong>
                    <span>Backend development</span>
                </div>


                <div class="skill">
                    <strong>Docker</strong>
                    <span>Containerization</span>
                </div>


                <div class="skill">
                    <strong>GitHub Actions</strong>
                    <span>CI/CD automation</span>
                </div>


                <div class="skill">
                    <strong>Cloud Deployment</strong>
                    <span>Production hosting</span>
                </div>


                <div class="skill">
                    <strong>REST API</strong>
                    <span>Service endpoints</span>
                </div>


                <div class="skill">
                    <strong>Linux / DevOps</strong>
                    <span>Infrastructure concepts</span>
                </div>

            </div>

        </div>

    </div>

</section>


<!-- =========================================================
     SERVICES
     ========================================================= -->

<section id="services">

    <div class="container">

        <div class="section-label">
            Services
        </div>

        <h2 class="section-title">
            What can be delivered?
        </h2>

        <p class="section-description">

            The same technologies used in this demo can be
            applied to real applications and small businesses.

        </p>


        <div class="cards">

            <div class="card">

                <div class="card-icon">
                    🐍
                </div>

                <h3>
                    Python Development
                </h3>

                <p>
                    Lightweight APIs, backend services,
                    automation scripts and web applications.
                </p>

            </div>


            <div class="card">

                <div class="card-icon">
                    🐳
                </div>

                <h3>
                    Docker Deployment
                </h3>

                <p>
                    Package applications into reproducible
                    containers for reliable deployment.
                </p>

            </div>


            <div class="card">

                <div class="card-icon">
                    ⚙️
                </div>

                <h3>
                    CI/CD Automation
                </h3>

                <p>
                    Automate testing, builds and deployment
                    with GitHub Actions workflows.
                </p>

            </div>


            <div class="card">

                <div class="card-icon">
                    ☁️
                </div>

                <h3>
                    Cloud Deployment
                </h3>

                <p>
                    Deploy applications to modern cloud
                    platforms and configure production services.
                </p>

            </div>


            <div class="card">

                <div class="card-icon">
                    📊
                </div>

                <h3>
                    Monitoring
                </h3>

                <p>
                    Health checks, status endpoints and
                    application logging.
                </p>

            </div>


            <div class="card">

                <div class="card-icon">
                    🔐
                </div>

                <h3>
                    Production Basics
                </h3>

                <p>
                    Environment variables, secure configuration,
                    error handling and deployment practices.
                </p>

            </div>

        </div>

    </div>

</section>


<!-- =========================================================
     PROJECTS
     ========================================================= -->

<section id="projects">

    <div class="container">

        <div class="section-label">
            Projects
        </div>

        <h2 class="section-title">
            Built and deployed.
        </h2>

        <p class="section-description">

            A growing collection of practical software and
            infrastructure projects.

        </p>


        <div class="projects">

            <div class="project">

                <div class="project-top">

                    <h3>
                        Python DevOps Demo
                    </h3>

                    <span class="project-status">
                        LIVE
                    </span>

                </div>


                <p>
                    Production-style Python HTTP application
                    containerized with Docker and deployed
                    through a CI/CD workflow.
                </p>


                <div class="tags">

                    <span class="tag">
                        Python
                    </span>

                    <span class="tag">
                        Docker
                    </span>

                    <span class="tag">
                        GitHub Actions
                    </span>

                    <span class="tag">
                        Render
                    </span>

                </div>

            </div>


            <div class="project">

                <div class="project-top">

                    <h3>
                        API Monitoring
                    </h3>

                    <span class="project-status">
                        ACTIVE
                    </span>

                </div>


                <p>
                    Health and status endpoints designed
                    for automated service monitoring.
                </p>


                <div class="tags">

                    <span class="tag">
                        REST API
                    </span>

                    <span class="tag">
                        Health Check
                    </span>

                    <span class="tag">
                        Monitoring
                    </span>

                </div>

            </div>

        </div>

    </div>

</section>


<!-- =========================================================
     STATUS
     ========================================================= -->

<section id="status">

    <div class="container">

        <div class="section-label">
            System
        </div>

        <h2 class="section-title">
            Live system status.
        </h2>

        <p class="section-description">

            Production endpoints are available for
            health checks and service monitoring.

        </p>


        <div class="status-panel">

            <div class="status-row">

                <span class="status-name">
                    Application
                </span>

                <span class="status-value">
                    ● ONLINE
                </span>

            </div>


            <div class="status-row">

                <span class="status-name">
                    Python Service
                </span>

                <span class="status-value">
                    ● RUNNING
                </span>

            </div>


            <div class="status-row">

                <span class="status-name">
                    Docker
                </span>

                <span class="status-value">
                    ● ACTIVE
                </span>

            </div>


            <div class="status-row">

                <span class="status-name">
                    API
                </span>

                <span class="status-value">
                    ● AVAILABLE
                </span>

            </div>


            <div class="status-row">

                <span class="status-name">
                    Deployment
                </span>

                <span class="status-value">
                    ● LIVE
                </span>

            </div>

        </div>


        <div
            class="hero-buttons"
            style="margin-top: 25px;"
        >

            <a
                href="/health"
                class="btn btn-secondary"
            >
                Health Check
            </a>


            <a
                href="/api/status"
                class="btn btn-secondary"
            >
                API Status
            </a>


            <a
                href="/api/info"
                class="btn btn-secondary"
            >
                API Info
            </a>

        </div>

    </div>

</section>


<!-- =========================================================
     CONTACT
     ========================================================= -->

<section id="contact">

    <div class="container">

        <div class="contact-box">

            <div class="section-label">
                Contact
            </div>

            <h2>
                Build something useful.
            </h2>

            <p>
                This platform can be expanded into real
                business applications, APIs and automated
                cloud deployments.
            </p>


            <a
                href="mailto:contact@example.com"
                class="btn btn-primary"
            >
                Contact
            </a>

        </div>

    </div>

</section>

</main>


<!-- =========================================================
     FOOTER
     ========================================================= -->

<footer>

    <div class="container">

        <div class="footer-content">

            <div>
                Python DevOps Platform
            </div>

            <div>
                Python • Docker • GitHub Actions • Cloud
            </div>

        </div>

    </div>

</footer>


</body>

</html>
"""


# ============================================================
# 404 PAGE
# ============================================================

NOT_FOUND_HTML = """
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>404 - Not Found</title>

    <style>

        body {
            margin: 0;
            min-height: 100vh;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #070b16;
            color: white;

            font-family: Arial, sans-serif;

            text-align: center;
        }

        .box {
            padding: 40px;
        }

        h1 {
            font-size: 80px;
            margin: 0 0 10px;
        }

        p {
            color: #94a3b8;
            margin-bottom: 25px;
        }

        a {
            display: inline-block;

            padding: 12px 20px;

            border-radius: 10px;

            background: #2563eb;

            color: white;

            text-decoration: none;
        }

    </style>

</head>

<body>

    <div class="box">

        <h1>404</h1>

        <p>
            The requested page was not found.
        </p>

        <a href="/">
            Return Home
        </a>

    </div>

</body>

</html>
"""


# ============================================================
# JSON HELPERS
# ============================================================

def json_response(handler, data, status_code=200):
    """
    Send a JSON response.
    """

    body = json.dumps(
        data,
        indent=2
    ).encode("utf-8")


    handler.send_response(status_code)

    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8"
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

    return body


def html_response(handler, html, status_code=200):
    """
    Send an HTML response.
    """

    body = html.encode("utf-8")


    handler.send_response(status_code)

    handler.send_header(
        "Content-Type",
        "text/html; charset=utf-8"
    )

    handler.send_header(
        "Content-Length",
        str(len(body))
    )

    handler.send_header(
        "Cache-Control",
        "no-cache"
    )

    handler.end_headers()

    return body


# ============================================================
# REQUEST HANDLER
# ============================================================

class Handler(BaseHTTPRequestHandler):

    server_version = "PythonDevOps/2.0"


    def log_message(self, format_string, *args):
        """
        Use Python logging instead of the default output.
        """

        logger.info(
            "%s - %s",
            self.address_string(),
            format_string % args
        )


    def get_path(self):
        """
        Remove query parameters from the URL.
        """

        return self.path.split("?", 1)[0]


    def do_HEAD(self):
        """
        Support HEAD requests.
        """

        path = self.get_path()


        if path == "/":

            body = HTML.encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(body))
            )

            self.end_headers()

            return


        if path == "/health":

            body = b"ok"

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/plain; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(body))
            )

            self.end_headers()

            return


        if path in (
            "/api/status",
            "/api/info"
        ):

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )

            self.end_headers()

            return


        self.send_response(404)
        self.end_headers()


    def do_GET(self):

        path = self.get_path()


        logger.info(
            "GET request: %s",
            path
        )


        # ----------------------------------------------------
        # HOME
        # ----------------------------------------------------

        if path == "/":

            body = html_response(
                self,
                HTML,
                200
            )

            self.wfile.write(body)

            return


        # ----------------------------------------------------
        # HEALTH
        # ----------------------------------------------------

        if path == "/health":

            body = b"ok"

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/plain; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(body))
            )

            self.send_header(
                "Cache-Control",
                "no-store"
            )

            self.end_headers()

            self.wfile.write(body)

            return


        # ----------------------------------------------------
        # API STATUS
        # ----------------------------------------------------

        if path == "/api/status":

            response = {
                "status": "ok",
                "service": SERVICE_NAME,
                "version": APP_VERSION,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat()
            }


            body = json_response(
                self,
                response,
                200
            )

            self.wfile.write(body)

            return


        # ----------------------------------------------------
        # API INFO
        # ----------------------------------------------------

        if path == "/api/info":

            response = {
                "application": APP_NAME,
                "service": SERVICE_NAME,
                "version": APP_VERSION,
                "python": platform.python_version(),
                "platform": platform.system(),
                "architecture": platform.machine(),
                "environment": "production"
            }


            body = json_response(
                self,
                response,
                200
            )

            self.wfile.write(body)

            return


        # ----------------------------------------------------
        # 404
        # ----------------------------------------------------

        body = html_response(
            self,
            NOT_FOUND_HTML,
            404
        )

        self.wfile.write(body)


# ============================================================
# SERVER START
# ============================================================

def main():

    server = HTTPServer(
        ("0.0.0.0", PORT),
        Handler
    )


    logger.info(
        "Starting %s",
        APP_NAME
    )

    logger.info(
        "Version: %s",
        APP_VERSION
    )

    logger.info(
        "Port: %s",
        PORT
    )

    logger.info(
        "Server is ready"
    )


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        logger.info(
            "Server stopped by user"
        )

    finally:

        server.server_close()

        logger.info(
            "Server shutdown complete"
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
