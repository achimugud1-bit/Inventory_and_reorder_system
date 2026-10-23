# Inventory & Reorder System

An inventory project built with HTML, CSS, JavaScript, and Python. It tracks products, stock movements, and low-stock reorder suggestions. Browser changes are saved to a shared JSON file.

## Run the project

From this folder, start the server:

    python3 run.py

Open http://localhost:8000. Keep the server terminal open while using the app; press Ctrl+C to stop it.

## Seven member assignments

| Member | File to work on | What it handles |
|---|---|---|
| Mr. Peter | members/peter/app.js, api.js, view.js | Browser logic, data requests, and display |
| Mr. Sam | members/sam/index.html | Main page and forms |
| Mr. Daniel | members/daniel/style.css and CSS helper files | Page appearance |
| Cynthia | members/cynthia/data.json | Product and movement data |
| David | members/david/storage.py | Loading and safely saving inventory |
| Mr. Thomas | members/thomas/records.py | Product and movement validation |
| Promise | order.py | Low-stock reorder suggestions |

run.py connects the server to these modules. The short parent files remain in place as entry points.

## Shared data shapes

- Product: {id, name, sku, price, stock, threshold, supplier}
- Movement: {id, product_id, qty, reason, by, date}

A positive movement adds stock; a negative movement removes stock. Stock is low when it is at or below its threshold.
