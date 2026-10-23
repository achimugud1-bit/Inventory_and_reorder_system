"""Build supplier reorder suggestions from current product records."""


def build_order_draft(products):
    """Return products at or below threshold with a suggested quantity."""
    draft = []

    for product in products:
        stock = int(product.get("stock", 0))
        threshold = int(product.get("threshold", 0))
        if stock <= threshold:
            quantity = max(0, threshold * 2 - stock)
            item = dict(product)
            item["order_quantity"] = quantity
            draft.append(item)

    return draft
