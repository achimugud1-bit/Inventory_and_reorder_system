// Shared browser entry point: load inventory and connect the page parts.
import { connectForms, readJson } from "../promise/forms.js";

// Escape text from the inventory before putting it into HTML.
function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, char =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

function message(text, failed = false) {
  const status = document.getElementById("app-message");
  status.textContent = text;
  status.className = `app-status ${failed ? "alert" : "notice"}`;
}

function render(data) {
  document.getElementById("product-rows").innerHTML = data.products.map(product => `<tr>
    <td>${product.id}</td><td><b>${safe(product.name)}</b><br><small>${safe(product.sku)}</small></td>
    <td>${product.stock} <span class="tag ${product.stock <= product.threshold ? "low" : "ok"}">${product.stock <= product.threshold ? "LOW" : "ok"}</span></td>
    <td>≤ ${product.threshold}</td><td>${Number(product.price).toLocaleString()}</td>
    <td>${safe(product.supplier || "—")}</td></tr>`).join("")
    || '<tr><td colspan="6">No products yet.</td></tr>';

  document.getElementById("alert-list").innerHTML = data.orders.map(item => `<li>⚠️ <b>${safe(item.name)}</b> — ${item.stock} left
    (threshold ${item.threshold}); order ${item.order_quantity} · supplier: ${safe(item.supplier || "?")}</li>`).join("")
    || '<li>✅ Nothing is low on stock right now.</li>';

  document.getElementById("movement-rows").innerHTML = data.movements.slice().reverse().map(move => `<tr>
    <td>${safe(move.date)}</td><td>${safe(data.products.find(p => p.id === move.product_id)?.name || `#${move.product_id}`)}</td>
    <td>${move.qty > 0 ? "+" : ""}${move.qty}</td><td>${safe(move.reason)}</td><td>${safe(move.by)}</td></tr>`).join("")
    || '<tr><td colspan="5">No movements recorded yet.</td></tr>';

  document.getElementById("movement-product").innerHTML = data.products.map(product =>
    `<option value="${product.id}">${safe(product.name)}</option>`).join("");
}

// Load current stock and reorder suggestions from the Python server.
async function refresh() {
  const [stockResponse, orderResponse] = await Promise.all([
    fetch("/members/cynthia/data.json", { cache: "no-store" }),
    fetch("/api/orders", { cache: "no-store" }),
  ]);
  if (!stockResponse.ok || !orderResponse.ok) throw Error("Could not load inventory.");

  const inventory = await readJson(stockResponse);
  const { orders } = await readJson(orderResponse);
  render({ ...inventory, orders });
  message("Inventory loaded.");
}

connectForms(refresh, message);
refresh().catch(error => message(`${error.message} Start with python3 run.py.`, true));
