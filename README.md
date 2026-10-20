# 📦 Inventory & Reorder System
**Learn2Earn group project · 7 people · 7 files · 1 run file · HTML + Python only · zero installs**

Manage products, stock movements and low-stock notifications.
Each person owns **exactly one file**. All seven files are **already linked** to `run.py` — nobody touches anyone else's wiring.

## ▶ Run it
```bash
python3 run.py
# open http://localhost:8000        (main page)
# open http://localhost:8000/reports (reports page)
# second terminal, optional:
#   python3 members/member5/report.py    → stock report in terminal
#   python3 members/member6/notify.py    → low-stock notifications in terminal
```
No pip. No database. No backend logic. Data lives in one JSON file.

## 👥 Who owns what
| File | Type | Owner | Their job (write ONLY inside their file) |
|---|---|---|---|
| `members/member1/app.js` | JS | member1 | ✅ finished example — wires forms & tables; others copy its spirit, not its code |
| `members/member2/index.html` | HTML | member2 | the main page: sections, layout, headings (keep the ids + link/script tags) |
| `members/member3/style.css` | CSS | member3 | all looks: colors, spacing, table style, tags |
| `members/member4/data.json` | data | member4 | the inventory book: add/edit product & movement rows |
| `members/member5/report.py` | Python | member5 | terminal stock report (WRITE HERE marks inside) |
| `members/member6/notify.py` | Python | member6 | terminal low-stock notifications (WRITE HERE marks inside) |
| `members/member7/reports.html` | HTML | member7 | printable reports page (one WRITE HERE render block) |
| `run.py` | Python | **leader only** | the server. nobody else opens it |

*Put real names on folders with:* `./rename.sh name2 name3 name4 name5 name6 name7`

## 🔗 The wiring (already done — read once, forget forever)
- `index.html` already contains: `<link … member3/style.css>` and `<script … member1/app.js>`
- `app.js` already fetches `member4/data.json`
- `reports.html` already links member3's CSS and fetches member4's data
- `run.py` already serves every folder and redirects `/` → index, `/reports` → reports
- `report.py` / `notify.py` already find data.json by themselves

**So each person opens ONE file and writes between the `═══ WRITE HERE ═══` marks. That's the entire collaboration model.**

## 📋 The only contract (the agreements between files)
`index.html` must keep these ids (app.js looks for them):
`add-product` (form, inputs named name/sku/price/stock/threshold/supplier) · `product-rows` (tbody) · `alert-list` (ul) · `add-movement` (form) · `movement-product` (select) · `movement-rows` (tbody) · `export-data` (button)

`data.json` rows must keep this exact shape (copy an existing row):
product = `{id, name, sku, price, stock, threshold, supplier}` · movement = `{id, product_id, qty, reason, by, date}`
(`qty` positive = stock-in, negative = stock-out. Low stock = `stock <= threshold`.)

## 🔒 House rules (write these in the group chat too)
1. **One file per person.** Not run.py, not someone else's file, not "just a quick fix".
2. **No installs.** Python standard library + plain HTML/CSS/JS only.
3. **Test before you share:** `python3 run.py` → look at your part. Python folks: run your file directly.
4. **data.json edits get validated** (one wrong comma breaks the page):
   `python3 -c "import json;json.load(open('members/member4/data.json'))"`
5. Browser adds are **demo memory** — permanent changes go through member4 (or the Export button).

## 🆘 If something breaks
| Symptom | Fix |
|---|---|
| Page shows "Could not load data.json" | server not running → `python3 run.py` |
| Page shows nothing in tables | data.json has a JSON error → run the validate command above |
| Port 8000 busy | leader changes `PORT` at top of run.py |
| A section disappeared | someone removed an id from index.html → restore from git |
