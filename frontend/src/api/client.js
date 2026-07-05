const BASE = "http://localhost:5000";


export const getIdeas = async (prompt) => {
  const res = await axios.post("http://127.0.0.1:5000/api/ideas", {
    prompt,
  });

  return res.data; 
};

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