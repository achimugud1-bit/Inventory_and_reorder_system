// Peter's browser code: display inventory and send form changes to Python.
let DB = { products: [], movements: [], orders: [] };
const $ = id => document.getElementById(id);

// Escape inventory text before inserting it into the page.
function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, char =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

function message(text, failed = false) {
  $("app-message").textContent = text;
  $("app-message").className = `app-status ${failed ? "alert" : "notice"}`;
}

async function readJson(response) {
  if (!(response.headers.get("content-type") || "").includes("application/json")) {
    throw Error("The server did not return JSON. Restart it with python3 run.py.");
  }
  return response.json();
}

// Draw products, server-calculated reorder alerts, and movement history.
function render() {
  $("product-rows").innerHTML = DB.products.map(product => `<tr>
    <td>${product.id}</td><td><b>${safe(product.name)}</b><br><small>${safe(product.sku)}</small></td>
    <td>${product.stock} <span class="tag ${product.stock <= product.threshold ? "low" : "ok"}">${product.stock <= product.threshold ? "LOW" : "ok"}</span></td>
    <td>≤ ${product.threshold}</td><td>${Number(product.price).toLocaleString()}</td>
    <td>${safe(product.supplier || "—")}</td></tr>`).join("")
    || '<tr><td colspan="6">No products yet.</td></tr>';

  $("alert-list").innerHTML = DB.orders.map(item => `<li>⚠️ <b>${safe(item.name)}</b> — ${item.stock} left
    (threshold ${item.threshold}); order ${item.order_quantity} · supplier: ${safe(item.supplier || "?")}</li>`).join("")
    || '<li>✅ Nothing is low on stock right now.</li>';

  $("movement-rows").innerHTML = DB.movements.slice().reverse().map(move => `<tr>
    <td>${safe(move.date)}</td><td>${safe(DB.products.find(p => p.id === move.product_id)?.name || `#${move.product_id}`)}</td>
    <td>${move.qty > 0 ? "+" : ""}${move.qty}</td><td>${safe(move.reason)}</td><td>${safe(move.by)}</td></tr>`).join("")
    || '<tr><td colspan="5">No movements recorded yet.</td></tr>';

  $("movement-product").innerHTML = DB.products.map(product =>
    `<option value="${product.id}">${safe(product.name)}</option>`).join("");
}

function update(data, orders) {
  DB = { ...data, orders };
  delete DB._readme;
  render();
}

// Get inventory data and reorder suggestions from the Python server.
async function refresh() {
  const [inventoryResponse, ordersResponse] = await Promise.all([
    fetch("/members/cynthia/data.json", { cache: "no-store" }),
    fetch("/api/orders", { cache: "no-store" }),
  ]);
  if (!inventoryResponse.ok || !ordersResponse.ok) throw Error("Could not load inventory.");
  const inventory = await readJson(inventoryResponse);
  const { orders } = await readJson(ordersResponse);
  update(inventory, orders);
  message("Inventory loaded.");
}

async function save(url, values, form, success) {
  try {
    const response = await fetch(url, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(values),
    });
    const result = await readJson(response);
    if (!response.ok) throw Error(result.error || "Could not save the change.");
    await refresh();
    message(success);
    form.reset();
  } catch (error) {
    message(error.message, true);
  }
}

function connectForm(id, url, fields, success) {
  $(id).addEventListener("submit", event => {
    event.preventDefault();
    const form = event.currentTarget;
    const values = Object.fromEntries(new FormData(form));
    fields.forEach(field => values[field] = Number(values[field] || (field === "threshold" ? 5 : 0)));
    save(url, values, form, success);
  });
}

connectForm("add-product", "/api/products", ["price", "stock", "threshold"], "Product saved.");
connectForm("add-movement", "/api/movements", ["product_id", "qty"], "Stock movement saved.");

refresh().catch(error => message(`${error.message} Start with python3 run.py.`, true));
