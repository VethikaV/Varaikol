const BASE = "http://localhost:5000";

export async function getIdeas(prompt) {
  const res = await fetch(`${BASE}/api/ideas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  return res.json();
}

export async function convertSketch(file) {
  const form = new FormData();
  form.append("image", file);
  const res = await fetch(`${BASE}/api/sketch`, { method: "POST", body: form });
  return res.json();
}

export async function analyzeDrawing(file) {
  const form = new FormData();
  form.append("image", file);
  const res = await fetch(`${BASE}/api/analyze`, { method: "POST", body: form });
  return res.json();
}