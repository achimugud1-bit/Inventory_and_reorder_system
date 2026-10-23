#!/usr/bin/env python3
"""Serve the inventory page and connect browser requests to project modules."""

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from inventory import InventoryError, update_inventory
from order import build_order_draft
from storage import DATA_LOCK, MEMBERS, ROOT, load_data, save_data

PORT = 8000


class Handler(SimpleHTTPRequestHandler):
    """Serve project files and handle inventory API requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path == "/api/orders":
            with DATA_LOCK:
                data = load_data()
            return self.send_json(200, {"orders": build_order_draft(data["products"])})

        pages = {"/": "index.html"}
        if self.path in pages:
            page = next(MEMBERS.glob(f"*/{pages[self.path]}"), None)
            if page:
                self.path = "/" + page.relative_to(ROOT).as_posix()
        super().do_GET()

    def send_json(self, status, result):
        """Send an API response as JSON."""
        body = json.dumps(result).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        """Read a browser request and save the requested inventory change."""
        try:
            size = int(self.headers.get("Content-Length", 0))
            if not 0 < size <= 100_000:
                return self.send_json(400, {"error": "Request is empty or too large."})

            form = json.loads(self.rfile.read(size))
            with DATA_LOCK:
                data = load_data()
                update_inventory(data, self.path, form)
                save_data(data)

            return self.send_json(201, {"data": data})
        except InventoryError as error:
            return self.send_json(error.status, {"error": str(error)})
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
