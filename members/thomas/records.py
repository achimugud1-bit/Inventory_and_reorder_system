'Mr. Thomas: validate and apply product and stock form changes.'

from datetime import date


def add_product(form, products):
    'Validate a product form and return the next product record.'
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
    if not name or min(product["price"], product["stock"], product["threshold"]) < 0:
        raise ValueError("Enter a name and non-negative price, stock, and threshold.")
    if sku and any(item.get("sku", "").casefold() == sku.casefold() for item in products):
        raise ValueError("That SKU is already in use.")
    return product


def apply_movement(form, products, movements):
    'Validate a stock movement, update its product, and record the change.'
    product_id = int(form.get("product_id", 0))
    quantity = int(form.get("qty", 0))
    product = next((item for item in products if item["id"] == product_id), None)
    if not product or not quantity or product["stock"] + quantity < 0:
        raise ValueError("Choose a product and enter a valid quantity.")
    product["stock"] += quantity
    movements.append({
        "id": max((item["id"] for item in movements), default=0) + 1,
        "product_id": product_id,
        "qty": quantity,
        "reason": form.get("reason", ""),
        "by": form.get("by", ""),
        "date": date.today().isoformat(),
    })
