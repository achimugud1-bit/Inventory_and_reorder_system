// Promise: send product and stock-movement forms to the server.

export async function readJson(response) {
  if (!(response.headers.get("content-type") || "").includes("application/json")) {
    throw Error("The server did not return JSON. Restart it with python3 run.py.");
  }
  return response.json();
}

async function save(url, values, form, success, refresh, message) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
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

function connectForm(id, url, fields, success, refresh, message) {
  document.getElementById(id).addEventListener("submit", event => {
    event.preventDefault();
    const form = event.currentTarget;
    const values = Object.fromEntries(new FormData(form));
    fields.forEach(field => {
      values[field] = Number(values[field] || (field === "threshold" ? 5 : 0));
    });
    save(url, values, form, success, refresh, message);
  });
}

export function connectForms(refresh, message) {
  connectForm("add-product", "/api/products", ["price", "stock", "threshold"], "Product saved.", refresh, message);
  connectForm("add-movement", "/api/movements", ["product_id", "qty"], "Stock movement saved.", refresh, message);
}
