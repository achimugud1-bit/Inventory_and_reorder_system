"""Build supplier reorder suggestions from current product records."""


def build_order_draft(products):
    """Return products at or below threshold with a suggested quantity."""
    # Start with an empty draft list that will collect reorder candidates.
    draft = []

    for product in products:
        # Normalize inventory values to integers so comparisons and math are consistent.
        stock = int(product.get("stock", 0))
        threshold = int(product.get("threshold", 0))

        # Only restock items that have reached or fallen below the reorder point.
        if stock <= threshold:
            # Order enough to cover a full two-threshold buffer, without going negative.
            quantity = max(0, threshold * 2 - stock)
            item = dict(product)
            item["order_quantity"] = quantity
            draft.append(item)

    return draft
