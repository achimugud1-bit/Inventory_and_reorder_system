// Peter: safely draw inventory tables and page messages.
const $ = id => document.getElementById(id);

function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, char =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", """: "&quot;", "'": "&#39;" })[char]);
}

export function showMessage(text, failed = false) {
  $("app-message").textContent = text;
  $("app-message").className = `app-status ${failed ? "alert" : "notice"}`;
}

export function renderInventory(data, orders) {
  $("product-rows").innerHTML = data.products.map(product => `<tr>
    <td>${product.id}</td><td><b>${safe(product.name)}</b><br><small>${safe(product.sku)}</small></td>
    <td>${product.stock} <span class="tag ${product.stock <= product.threshold ? "low" : "ok"}">${product.stock <= product.threshold ? "LOW" : "ok"}</span></td>
    <td>≤ ${product.threshold}</td><td>${Number(product.price).toLocaleString()}</td>
    <td>${safe(product.supplier || "—")}</td></tr>`).join("")
    || '<tr><td colspan="6">No products yet.</td></tr>';

  $("alert-list").innerHTML = orders.map(item => `<li>⚠️ <b>${safe(item.name)}</b> — ${item.stock} left
    (threshold ${item.threshold}); order ${item.order_quantity} · supplier: ${safe(item.supplier || "?")}</li>`).join("")
    || '<li>✅ Nothing is low on stock right now.</li>';

  $("movement-rows").innerHTML = data.movements.slice().reverse().map(move => `<tr>
    <td>${safe(move.date)}</td><td>${safe(data.products.find(p => p.id === move.product_id)?.name || "#" + move.product_id)}</td>
    <td>${move.qty > 0 ? "+" : ""}${move.qty}</td><td>${safe(move.reason)}</td><td>${safe(move.by)}</td></tr>`).join("")
    || '<tr><td colspan="5">No movements recorded yet.</td></tr>';

  $("movement-product").innerHTML = data.products.map(product =>
    `<option value="${product.id}">${safe(product.name)}</option>`).join("");
}
