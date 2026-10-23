#!/usr/bin/env python3
'Start the inventory server and connect its supporting modules.'

import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from members.david.storage import load_inventory, save_inventory
from members.thomas.records import add_product, apply_movement
from order import build_order_draft

ROOT = Path(__file__).resolve().parent
MEMBERS = ROOT / "members"
PORT = 8000
DATA_LOCK = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    'Serve the page and route inventory requests to the project modules.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path == "/api/orders":
            with DATA_LOCK:
                data = load_inventory()
            return self.send_json(200, {"orders": build_order_draft(data["products"])})

        if self.path == "/":
            page = next(MEMBERS.glob("*/index.html"), None)
            if page:
                self.path = "/" + page.relative_to(ROOT).as_posix()
        super().do_GET()

    def send_json(self, status, result):
        body = json.dumps(result).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", 0))
            if not 0 < size <= 100_000:
                return self.send_json(400, {"error": "Request is empty or too large."})
            form = json.loads(self.rfile.read(size))

            with DATA_LOCK:
                data = load_inventory()
                if self.path == "/api/products":
                    data["products"].append(add_product(form, data["products"]))
                elif self.path == "/api/movements":
                    apply_movement(form, data["products"], data["movements"])
                else:
                    return self.send_json(404, {"error": "Unknown API endpoint."})
                save_inventory(data)

            return self.send_json(201, {"data": data})
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            return self.send_json(400, {"error": f"Invalid request: {error}"})
        except OSError as error:
            return self.send_json(500, {"error": f"Could not save inventory data: {error}"})

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    print(f"Inventory & Reorder System: http://localhost:{PORT}")
    print("Stop with Ctrl+C")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
