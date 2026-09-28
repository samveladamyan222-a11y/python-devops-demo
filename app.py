from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python DevOps Demo</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px;
        }

        .container {
            width: 100%;
            max-width: 900px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 24px;
            padding: 45px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        }

        .status {
            display: inline-block;
            background: #16a34a;
            padding: 10px 18px;
            border-radius: 50px;
            font-weight: bold;
            margin-bottom: 25px;
        }

        h1 {
            font-size: 48px;
            margin-bottom: 15px;
        }

        .subtitle {
            font-size: 20px;
            color: #cbd5e1;
            margin-bottom: 35px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
        }

        .card {
            background: rgba(255,255,255,0.08);
            padding: 25px;
            border-radius: 18px;
        }

        .card h3 {
            margin-bottom: 10px;
        }

        .card p {
            color: #cbd5e1;
        }

        .api {
            margin-top: 30px;
            display: inline-block;
            padding: 14px 24px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
        }

        footer {
            margin-top: 35px;
            color: #94a3b8;
        }

        @media (max-width: 700px) {
            h1 {
                font-size: 36px;
            }

            .cards {
                grid-template-columns: 1fr;
            }

            .container {
                padding: 30px 20px;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="status">● SERVER ONLINE</div>

    <h1>Python DevOps Demo</h1>

    <p class="subtitle">
        Dockerized Python Application running on Render
    </p>

    <div class="cards">

        <div class="card">
            <h3>🐍 Python</h3>
            <p>Python HTTP Server</p>
        </div>

        <div class="card">
            <h3>🐳 Docker</h3>
            <p>Containerized Application</p>
        </div>

        <div class="card">
            <h3>🚀 DevOps</h3>
            <p>GitHub → Docker → Render</p>
        </div>

    </div>

    <a class="api" href="/api/status">
        Check API Status
    </a>

    <footer>
        Python • Docker • GitHub Actions • Render
    </footer>

</div>

</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        if self.path.split("?")[0] == "/":
            body = HTML.encode()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):

        path = self.path.split("?")[0]

        if path == "/":

            body = HTML.encode()

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        elif path == "/api/status":

            response = {
                "status": "ok",
                "service": "python-devops-demo"
            }

            body = json.dumps(response).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()

            self.wfile.write(body)

        else:

            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))

    server = HTTPServer(("0.0.0.0", port), Handler)

    print(f"Server running on port {port}")

    try:
        server.serve_forever()

    except KeyboardInterrupt:

        print("\nServer stopped")
        server.server_close()
