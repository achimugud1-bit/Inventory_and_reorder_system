"""Validate and apply product and stock-movement changes."""

from datetime import date


class InventoryError(Exception):
    """An inventory update error with the HTTP status to return."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def add_product(data, form):
    """Validate a product form and append the new product."""
    products = data["products"]
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
        raise InventoryError(
            "Enter a name and non-negative price, stock, and threshold."
        )
    if sku and any(item.get("sku", "").casefold() == sku.casefold() for item in products):
        raise InventoryError("That SKU is already in use.", 409)

    products.append(product)


def add_movement(data, form):
    """Validate a stock movement, then update stock and movement history."""
    products = data["products"]
    movements = data["movements"]
    product_id = int(form.get("product_id", 0))
    quantity = int(form.get("qty", 0))
    product = next((item for item in products if item["id"] == product_id), None)

    if not product or not quantity or product["stock"] + quantity < 0:
        raise InventoryError("Choose a product and enter a valid quantity.")

    product["stock"] += quantity
    movements.append({
        "id": max((item["id"] for item in movements), default=0) + 1,
        "product_id": product_id,
        "qty": quantity,
        "reason": form.get("reason", ""),
        "by": form.get("by", ""),
        "date": date.today().isoformat(),
    })


def update_inventory(data, endpoint, form):
    """Choose the correct inventory update for an API endpoint."""
    if endpoint == "/api/products":
        add_product(data, form)
    elif endpoint == "/api/movements":
        add_movement(data, form)
    else:
        raise InventoryError("Unknown API endpoint.", 404)
