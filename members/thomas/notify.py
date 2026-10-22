# Owner: Miss Thomas · run with: python3 members/thomas/notify.py
# This prints reorder suggestions; it does not send email or messages.
import json
from pathlib import Path

# Finds the shared inventory data file.
data_file = Path(__file__).resolve().parents[2] / "members/cynthia/data.json"

# Read the products from the JSON file
products = json.loads(data_file.read_text(encoding="utf-8"))["products"]

# Finds products whose stock is at or below the reorder threshold.
low_stock = [
    product for product in products
    if product["stock"] <= product["threshold"]
]

print("LOW-STOCK REORDER SUGGESTIONS")
for product in low_stock:
    # Calculate how many units are needed to reach twice the threshold.
    quantity = max(0, product["threshold"] * 2 - product["stock"])

# Display the supplier, quantity to order, product name and stock left.
    print(
        f"{product['supplier']}: order {quantity} x {product['name']} "
        f"({product['stock']} left)"
    )

# Show this message if no products need reordering
if not low_stock:
    print("Nothing to reorder today.")
