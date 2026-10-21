# Inventory & Reorder System

A seven-person inventory project built with HTML, CSS, JavaScript, and Python. It tracks products, stock movements, and low-stock alerts. Browser changes are saved to a shared JSON file.

## Run the project

From this folder, start the server:

```bash
python3 run.py
```

Open [http://localhost:8000](http://localhost:8000) for the inventory page or [http://localhost:8000/reports](http://localhost:8000/reports) for the stock report. Keep the server terminal open while using the app; press **Ctrl+C** to stop it.

Optional terminal reports:

```bash
python3 members/david/report.py
python3 members/sam/notify.py
```

The notification script prints reorder suggestions; it does not send email.

## File assignments

| Member | Assigned file | Responsibility |
|---|---|---|
| Mr. Peter | `members/peter/app.js` | Browser behavior, saving changes, and live stock alerts |
| Miss Thomas | `members/thomas/index.html` | Main page structure and forms |
| Mr. Daniel | `members/daniel/style.css` | Shared page styling |
| Cynthia | `members/cynthia/data.json` | Product and movement records |
| David | `members/david/report.py` | Terminal stock report |
| Mr. Sam | `members/sam/notify.py` | Terminal reorder suggestions |
| Promise | `members/promise/reports.html` | Browser stock report |

`run.py` is maintained by the group leader. The links between pages, styles, scripts, and data are already set up.

## Keep the shared wiring working

The main page must keep the IDs `add-product`, `product-rows`, `alert-list`, `add-movement`, `movement-product`, `movement-rows`, and `export-data`. The data file uses these shapes:

- Product: `{id, name, sku, price, stock, threshold, supplier}`
- Movement: `{id, product_id, qty, reason, by, date}`

A positive movement quantity adds stock; a negative quantity removes stock. A product is low when its stock is at or below its threshold. Validate JSON edits with:

```bash
python3 -c "import json; json.load(open('members/cynthia/data.json'))"
```
