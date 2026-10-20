# members/member5/report.py — OWNER: member5 · terminal stock report (Python file)
# Run (no server needed):   python3 members/member5/report.py
# ── WIRING BELOW — DO NOT DELETE: finds and loads data.json for you ──
import json, pathlib
DATA = pathlib.Path(__file__).resolve().parents[2] / "members" / "member4" / "data.json"
db = json.loads(DATA.read_text())
products, movements = db["products"], db["movements"]

print("=" * 46)
print("  STOCK REPORT — written by member5")
print("=" * 46)

# ═══════════ WRITE YOUR PYTHON HERE ═══════════
# 1) print one line per product: name, stock, threshold
#    (loop over `products`; each p is a dict: p["name"], p["stock"], p["threshold"])
# 2) print a LOW STOCK section: only products where p["stock"] <= p["threshold"]
# 3) bonus: print total stock value = sum of stock * price

print("-" * 46)
print("report done ✔")
