// Peter: connect page forms to the browser helpers.
import { loadInventory, saveChange } from "./api.js";
import { renderInventory, showMessage } from "./view.js";

let inventory = { products: [], movements: [] };
let orders = [];
const $ = id => document.getElementById(id);

async function refresh() {
  const latest = await loadInventory();
  inventory = latest.inventory;
  orders = latest.orders;
  renderInventory(inventory, orders);
}

async function save(url, values, form, success) {
  try {
    await saveChange(url, values);
    await refresh();
    showMessage(success);
    form.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
}

function connectForm(id, url, fields, success) {
  $(id).addEventListener("submit", event => {
    event.preventDefault();
    const form = event.currentTarget;
    const values = Object.fromEntries(new FormData(form));
    fields.forEach(field => {
      values[field] = Number(values[field] || (field === "threshold" ? 5 : 0));
    });
    save(url, values, form, success);
  });
}

connectForm("add-product", "/api/products", ["price", "stock", "threshold"], "Product saved.");
connectForm("add-movement", "/api/movements", ["product_id", "qty"], "Stock movement saved.");

refresh()
  .then(() => showMessage("Inventory loaded."))
  .catch(error => showMessage(error.message + " Start with python3 run.py.", true));
