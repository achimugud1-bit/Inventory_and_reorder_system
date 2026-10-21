// Owner: Mr. Peter · browser interface for the inventory server in run.py.

// Keep the current inventory in memory while the page is open.
let DB = { products: [], movements: [] };
let ready = false;
let connected = false;
let alertTimer;

const $ = id => document.getElementById(id);
const lows = () => DB.products.filter(product => product.stock <= product.threshold);
const productName = id => DB.products.find(product => product.id === id)?.name || `#${id}`;

// Escape text before placing it inside an HTML template.
function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

// Draw the product table, alerts, movement history, and product selector.
function render() {
  $("product-rows").innerHTML = DB.products.map(product => `
    <tr>
      <td>${product.id}</td>
      <td><b>${safe(product.name)}</b><br><small>${safe(product.sku)}</small></td>
      <td>${product.stock} ${product.stock <= product.threshold
        ? '<span class="tag low">LOW</span>'
        : '<span class="tag ok">ok</span>'}</td>
      <td>≤ ${product.threshold}</td>
      <td>${Number(product.price).toLocaleString()}</td>
      <td>${safe(product.supplier || "—")}</td>
    </tr>`).join("")
    || '<tr><td colspan="6">No products yet.</td></tr>';

  $("alert-list").innerHTML = lows().map(product => `
    <li>⚠️ <b>${safe(product.name)}</b> — ${product.stock} left
      (threshold ${product.threshold}) · supplier: ${safe(product.supplier || "?")}</li>`).join("")
    || '<li>✅ Nothing is low on stock right now.</li>';

  $("movement-rows").innerHTML = DB.movements.slice().reverse().map(movement => `
    <tr>
      <td>${safe(movement.date)}</td>
      <td>${safe(productName(movement.product_id))}</td>
      <td>${movement.qty > 0 ? "+" : ""}${movement.qty}</td>
      <td>${safe(movement.reason)}</td>
      <td>${safe(movement.by)}</td>
    </tr>`).join("")
    || '<tr><td colspan="5">No movements recorded yet.</td></tr>';

  $("movement-product").innerHTML = DB.products.map(product =>
    `<option value="${product.id}">${safe(product.name)}</option>`).join("");
}

function showMessage(message, failed = false) {
  const box = $("app-message");
  box.textContent = message;
  box.className = `app-status ${failed ? "alert" : "notice"}`;
}

// Give a useful message if the server returns an error page instead of JSON.
async function readJson(response) {
  const type = response.headers.get("content-type") || "";
  if (!type.includes("application/json")) {
    throw new Error("Server returned a web page instead of JSON. Restart with python3 run.py, then refresh.");
  }
  return response.json();
}

// Update the page and announce products that have newly reached low stock.
function update(data) {
  const oldLowIds = new Set(lows().map(product => product.id));
  DB = data;
  delete DB._readme;
  render();

  if (ready) {
    const newlyLow = lows().filter(product => !oldLowIds.has(product.id));
    if (newlyLow.length) {
      const alert = $("live-alert");
      alert.textContent = `New low-stock alert: ${newlyLow.map(product =>
        `${product.name} (${product.stock} left)`).join(", ")}`;
      alert.hidden = false;
      clearTimeout(alertTimer);
      alertTimer = setTimeout(() => { alert.hidden = true; }, 8000);
    }
  }
  ready = true;
}

// Reload saved inventory. The timer below calls this every five seconds.
async function refresh(showStatus = false) {
  const response = await fetch("/members/cynthia/data.json", { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load inventory data.");

  const wasConnected = connected;
  update(await readJson(response));
  connected = true;
  if (showStatus || !wasConnected) showMessage("Live updates · every 5 sec");
}

// Send a change to Python, then show the latest saved inventory.
async function save(endpoint, values, successMessage) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    const result = await readJson(response);
    if (!response.ok) throw new Error(result.error || "The change could not be saved.");

    update(result.data);
    showMessage(successMessage);
    return true;
  } catch (error) {
    showMessage(error.message, true);
    return false;
  }
}

// Add a product using the values from the main-page form.
$("add-product").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  values.price = Number(values.price || 0);
  values.stock = Number(values.stock || 0);
  values.threshold = Number(values.threshold || 5);

  if (await save("/api/products", values, "Product saved to inventory.")) {
    form.reset();
  }
});

// Record a restock or stock-out movement.
$("add-movement").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const values = Object.fromEntries(new FormData(form));
  values.product_id = Number(values.product_id);
  values.qty = Number(values.qty);

  if (await save("/api/movements", values, "Stock movement saved.")) {
    form.reset();
  }
});

// Download the current inventory as a backup JSON file.
$("export-data").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(DB, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "data.json";
  link.click();
  URL.revokeObjectURL(link.href);
});

refresh(true).catch(error => showMessage(
  `${error.message} Start the app with python3 run.py.`, true,
));

setInterval(() => refresh().catch(() => {
  connected = false;
  showMessage("Live updates paused. Check the server.", true);
}), 5000);
