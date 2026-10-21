#!/usr/bin/env python3
"""Serve the inventory pages and save changes to the shared JSON file."""

import json
import threading
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MEMBERS = ROOT / "members"
DATA_FILE = next(MEMBERS.glob("*/data.json"))
PORT = 8000
DATA_LOCK = threading.Lock()  # Prevent two requests writing the file at once.


def save_data(data):
    """Write the inventory safely, then replace the old file in one step."""
    temp_file = DATA_FILE.with_suffix(".json.tmp")
    temp_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temp_file.replace(DATA_FILE)


class Handler(SimpleHTTPRequestHandler):
    """Serve project files and handle product and stock-movement saves."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Always serve the newest HTML, CSS, JavaScript, and inventory data.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        # Give the two main pages short, easy-to-remember URLs.
        pages = {"/": "index.html", "/reports": "reports.html"}
        if self.path in pages:
            page = next(MEMBERS.glob(f"*/{pages[self.path]}"), None)
            if page:
                self.path = "/" + page.relative_to(ROOT).as_posix()
        super().do_GET()

    def send_json(self, status, result):
        """Return API results in JSON so the browser can display them."""
        body = json.dumps(result).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        """Save a new product or record a stock movement."""
        try:
            size = int(self.headers.get("Content-Length", 0))
            if not 0 < size <= 100_000:
                return self.send_json(400, {"error": "Request is empty or too large."})

            form = json.loads(self.rfile.read(size))

            # Read, update, and save as one locked operation to avoid lost changes.
            with DATA_LOCK:
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                products = data["products"]
                movements = data["movements"]

                if self.path == "/api/products":
                    name = str(form.get("name", "")).strip()
                    sku = str(form.get("sku", "")).strip()
                    product = {
                        "id": max((item["id"] for item in products), default=0) + 1,
                        "name": name,
                        "sku": sku,
                        "price": float(form.get("price", 0)),
                        "stock": int(form.get("stock", 0)),
                        "threshold": int(form.get("threshold", 5)),
                        "supplier": str(form.get("supplier", "")).strip(),
                    }

                    if not name or min(
                        product["price"], product["stock"], product["threshold"]
                    ) < 0:
                        return self.send_json(
                            400,
                            {"error": "Enter a name and non-negative price, stock, and threshold."},
                        )
                    if sku and any(
                        item.get("sku", "").casefold() == sku.casefold()
                        for item in products
                    ):
                        return self.send_json(409, {"error": "That SKU is already in use."})

                    products.append(product)

                elif self.path == "/api/movements":
                    product_id = int(form.get("product_id", 0))
                    quantity = int(form.get("qty", 0))
                    product = next(
                        (item for item in products if item["id"] == product_id),
                        None,
                    )

                    if not product or not quantity or product["stock"] + quantity < 0:
                        return self.send_json(
                            400,
                            {"error": "Choose a product and enter a valid quantity."},
                        )

                    product["stock"] += quantity
                    movements.append(
                        {
                            "id": max((item["id"] for item in movements), default=0) + 1,
                            "product_id": product_id,
                            "qty": quantity,
                            "reason": form.get("reason", ""),
                            "by": form.get("by", ""),
                            "date": date.today().isoformat(),
                        }
                    )

                else:
                    return self.send_json(404, {"error": "Unknown API endpoint."})

                save_data(data)

            return self.send_json(201, {"data": data})

        except (ValueError, TypeError, json.JSONDecodeError) as error:
            return self.send_json(400, {"error": f"Invalid request: {error}"})
        except OSError as error:
            return self.send_json(500, {"error": f"Could not save inventory data: {error}"})

    def log_message(self, *_):
        # Keep routine browser requests from cluttering the terminal.
        pass


if __name__ == "__main__":
    print(f"Inventory & Reorder System: http://localhost:{PORT}")
    print(f"Reports: http://localhost:{PORT}/reports")
    print("Stop with Ctrl+C")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
