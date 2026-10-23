# Inventory & Reorder System

An inventory project built with HTML, CSS, JavaScript, and Python. It tracks products, stock movements, and low-stock reorder suggestions. Browser changes are saved to a shared JSON file.

## Run the project

From this folder, start the server:

```bash
python3 run.py
```

Open [http://localhost:8000](http://localhost:8000) for the inventory page. Keep the server terminal open while using the app; press **Ctrl+C** to stop it.

## File assignments

| Member | Assigned file | Responsibility |
|---|---|---|
| Mr. Peter | `members/peter/app.js` | Inventory loading and page entry point |
| Mr. Sam | `members/sam/index.html` | Main page structure and forms |
| Promise | `members/promise/forms.js` | Product and stock form submissions |
| Mr. Daniel | `members/daniel/storage.py`, `style.css` | Inventory storage and shared page styling |
| David | `members/david/inventory.py` | Product and stock movement updates |
| Thomas | `members/thomas/order.py` | Reorder calculations |
| Cynthia | `members/cynthia/data.json` | Product and movement records |

`run.py` connects the page to the member-owned Python modules.

## Keep the shared wiring working

The main page must keep the IDs `add-product`, `product-rows`, `alert-list`, `add-movement`, `movement-product`, `movement-rows`. The data file uses these shapes:

- Product: `{id, name, sku, price, stock, threshold, supplier}`
- Movement: `{id, product_id, qty, reason, by, date}`

A positive movement quantity adds stock; a negative quantity removes stock. A product is low when its stock is at or below its threshold. Validate JSON edits with:

```bash
python3 -c "import json; json.load(open('members/cynthia/data.json'))"
```
