'Promise: calculate reorder suggestions from product stock levels.'


def build_order_draft(products):
    'Return products at or below threshold with a suggested quantity.'
    draft = []
    for product in products:
        stock = int(product.get("stock", 0))
        threshold = int(product.get("threshold", 0))
        if stock <= threshold:
            item = dict(product)
            item["order_quantity"] = max(0, threshold * 2 - stock)
            draft.append(item)
    return draft
