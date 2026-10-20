# members/member6/notify.py — OWNER: member6 · low-stock notifier (Python file)
# Run (no server needed):   python3 members/member6/notify.py
# ── WIRING BELOW — DO NOT DELETE: finds data.json + selects low products for you ──
import json, pathlib
DATA = pathlib.Path(__file__).resolve().parents[2] / "members" / "member4" / "data.json"
db = json.loads(DATA.read_text())
lows = [p for p in db["products"] if p["stock"] <= p["threshold"]]

print("🔔 LOW-STOCK NOTIFICATIONS — written by member6")
print("-" * 46)

# ═══════════ WRITE YOUR PYTHON HERE ═══════════
# Loop over `lows`. For each p print one notification line containing:
#   product name · stock left · supplier · suggested reorder qty
# Suggested qty formula:  p["threshold"] * 2 - p["stock"]
# If `lows` is empty, print "nothing to reorder today".

print("-" * 46)
print(f"{len(lows)} notification(s)")
