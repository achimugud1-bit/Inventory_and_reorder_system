// Peter: browser requests for inventory data and server updates.
async function readJson(response) {
  if (!(response.headers.get("content-type") || "").includes("application/json")) {
    throw Error("The server did not return JSON. Restart it with python3 run.py.");
  }
  return response.json();
}

export async function loadInventory() {
  const [inventoryResponse, ordersResponse] = await Promise.all([
    fetch("/members/cynthia/data.json", { cache: "no-store" }),
    fetch("/api/orders", { cache: "no-store" }),
  ]);
  if (!inventoryResponse.ok || !ordersResponse.ok) throw Error("Could not load inventory.");
  return {
    inventory: await readJson(inventoryResponse),
    orders: (await readJson(ordersResponse)).orders,
  };
}

export async function saveChange(url, values) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values),
  });
  const result = await readJson(response);
  if (!response.ok) throw Error(result.error || "Could not save the change.");
  return result.data;
}
