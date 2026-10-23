"""Build supplier reorder suggestions from current product records."""


def build_order_draft(products):
    """Return products at or below threshold with suggested quantity and cost."""
    draft = []

    for product in products:
        stock = int(product.get("stock", 0))
        threshold = int(product.get("threshold", 0))
        if stock <= threshold:
            quantity = max(0, threshold * 2 - stock)
            item = dict(product)
            item["order_quantity"] = quantity
            item["estimated_cost"] = quantity * float(product.get("price", 0))
            draft.append(item)

    return draft
