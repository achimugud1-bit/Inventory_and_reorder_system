# Owner: Miss Thomas · run with: python3 members/thomas/notify.py
# This prints reorder suggestions; it does not send email or messages.
import json
from pathlib import Path

# Read products from the group's shared inventory file.
data_file = Path(__file__).resolve().parents[2] / "members/cynthia/data.json"
products = json.loads(data_file.read_text(encoding="utf-8"))["products"]
low_stock = [
    product for product in products
    if product["stock"] <= product["threshold"]
]

print("LOW-STOCK REORDER SUGGESTIONS")
for product in low_stock:
    # Suggest enough units to raise stock to twice the reorder threshold.
    quantity = max(0, product["threshold"] * 2 - product["stock"])
    print(
        f"{product['supplier']}: order {quantity} x {product['name']} "
        f"({product['stock']} left)"
    )

if not low_stock:
    print("Nothing to reorder today.")
