// members/member1/app.js — OWNER: member1 · THE JavaScript file (finished example)
// ═══════════════════════════════════════════════════════════════
// Already linked from index.html. It fetches data.json and wires the forms.
// Teammates: you never need to open this file. Just keep the ids in index.html.
// ═══════════════════════════════════════════════════════════════
const DATA_URL = "/members/member4/data.json";   // leader updates on rename
let DB = { products: [], movements: [] };

const $ = (id) => document.getElementById(id);
const lowList = () => DB.products.filter(p => p.stock <= p.threshold);
const productName = (id) => { const p = DB.products.find(x => x.id === id); return p ? p.name : "#" + id; };

function renderProducts(){
  const el = $("product-rows"); if (!el) return;
  el.innerHTML = DB.products.map(p => `
    <tr><td>${p.id}</td><td><b>${p.name}</b><br><small>${p.sku || ""}</small></td>
    <td>${p.stock} ${p.stock <= p.threshold ? '<span class="tag low">LOW</span>' : '<span class="tag ok">ok</span>'}</td>
    <td>≤ ${p.threshold}</td><td>${Number(p.price || 0).toLocaleString()}</td>
    <td>${p.supplier || "—"}</td></tr>`).join("")
    || '<tr><td colspan="6">No products in data.json yet.</td></tr>';
}
function renderAlerts(){
  const el = $("alert-list"); if (!el) return;
  const lows = lowList();
  el.innerHTML = lows.length
    ? lows.map(p => `<li>⚠️ <b>${p.name}</b> — ${p.stock} left (threshold ${p.threshold}) · supplier: ${p.supplier || "?"}</li>`).join("")
    : '<li>✅ Nothing is low on stock right now.</li>';
}
function renderMovements(){
  const el = $("movement-rows"); if (!el) return;
  el.innerHTML = DB.movements.slice().reverse().map(m => `
    <tr><td>${m.date || ""}</td><td>${productName(m.product_id)}</td>
    <td>${m.qty > 0 ? "+" : ""}${m.qty}</td><td>${m.reason || ""}</td><td>${m.by || ""}</td></tr>`).join("")
    || '<tr><td colspan="5">No movements recorded yet.</td></tr>';
}
function fillMovementSelect(){
  const sel = $("movement-product"); if (!sel) return;
  sel.innerHTML = DB.products.map(p => `<option value="${p.id}">${p.name}</option>`).join("");
}
function renderAll(){ renderProducts(); renderAlerts(); renderMovements(); fillMovementSelect(); }

async function load(){
  try {
    DB = await (await fetch(DATA_URL)).json();
    delete DB._readme;
    renderAll();
  } catch (e) {
    document.body.insertAdjacentHTML("afterbegin",
      '<p class="alert">⚠️ Could not load data.json — start the server with: python3 run.py</p>');
  }
}

// Changes live in browser memory (demo-simple). Permanent = Export → hand file to data owner.
function wireForms(){
  const add = $("add-product");
  if (add) add.addEventListener("submit", e => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(add));
    DB.products.push({ id: Math.max(0, ...DB.products.map(p => p.id)) + 1,
      name: f.name || "Unnamed", sku: f.sku || "", price: Number(f.price) || 0,
      stock: Number(f.stock) || 0, threshold: Number(f.threshold) || 5, supplier: f.supplier || "" });
    add.reset(); renderAll();
  });
  const mv = $("add-movement");
  if (mv) mv.addEventListener("submit", e => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(mv));
    const qty = Number(f.qty) || 0;
    const p = DB.products.find(x => x.id === Number(f.product_id));
    if (p) p.stock = Math.max(0, p.stock + qty);
    DB.movements.push({ id: Math.max(0, ...DB.movements.map(m => m.id)) + 1,
      product_id: Number(f.product_id), qty, reason: f.reason || "", by: f.by || "",
      date: new Date().toISOString().slice(0, 10) });
    mv.reset(); renderAll();
  });
  const ex = $("export-data");
  if (ex) ex.addEventListener("click", () => {
    const blob = new Blob([JSON.stringify({ products: DB.products, movements: DB.movements }, null, 2)],
      { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = "data.json"; a.click();
  });
}

load(); wireForms();
