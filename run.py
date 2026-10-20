#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
 INVENTORY & REORDER SYSTEM — THE RUN FILE (leader-only)
 ▶ Run:   python3 run.py      →  open http://localhost:8000
 It is a plain file server. No backend logic lives here on purpose.
═══════════════════════════════════════════════════════════════
"""
import glob, os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8000   # leader: change here if 8000 is busy

def find(filename):
    hits = glob.glob(os.path.join(ROOT, "members", "*", filename))
    return os.path.relpath(hits[0], ROOT).replace(os.sep, "/") if hits else None

INDEX   = find("index.html")
REPORTS = find("reports.html")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)
    def do_GET(self):
        if self.path in ("/", ""):
            self.path = "/" + (INDEX or "index.html")
        elif self.path == "/reports":
            self.path = "/" + (REPORTS or INDEX or "index.html")
        return super().do_GET()
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    print("▶ Inventory & Reorder System  →  http://localhost:%d" % PORT)
    print("  reports page               →  http://localhost:%d/reports" % PORT)
    print("  terminal tools (second terminal window):")
    for tool in ("report.py", "notify.py"):
        for p in glob.glob(os.path.join(ROOT, "members", "*", tool)):
            print("    python3", os.path.relpath(p, ROOT))
    print("  stop with Ctrl+C")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
