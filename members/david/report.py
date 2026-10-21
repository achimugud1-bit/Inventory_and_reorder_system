# Owner: David · run with: python3 members/david/report.py
import json
from pathlib import Path

# Read the shared inventory file from the project folder.
data_file = Path(__file__).resolve().parents[2] / "members/cynthia/data.json"
inventory = json.loads(data_file.read_text(encoding="utf-8"))
products = inventory["products"]

# Print each product and mark items that need reordering.
print("STOCK REPORT\n" + "-" * 40)
for product in products:
    status = "LOW" if product["stock"] <= product["threshold"] else "OK"
    print(
        f"{status:>3} {product['name']}: {product['stock']} in stock "
        f"(threshold {product['threshold']})"
    )

# List low-stock products and calculate the total value of all stock.
low_stock = [
    product for product in products
    if product["stock"] <= product["threshold"]
]
print("\nLOW STOCK:")
if low_stock:
    for product in low_stock:
        print(f"- {product['name']}: reorder from {product['supplier']}")
else:
    print("- Nothing to reorder")

total_value = sum(product["stock"] * product["price"] for product in products)
print(f"\nTotal stock value: {total_value:,.2f}")
