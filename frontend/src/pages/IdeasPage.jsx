import { useState } from "react";
import { getIdeas } from "../api/client";
import ResultCard from "../components/ResultCard";
import "./style.css";

const DIFFICULTY_COLOR = {
  Easy: "#22c55e",
  Medium: "#f59e0b",
  Hard: "#ef4444",
};

export default function IdeasPage() {
  const [prompt, setPrompt] = useState("");
  const [ideas, setIdeas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
  if (!prompt.trim()) return;

  setLoading(true);
  setError(null);
  setIdeas([]);

  try {
    const res = await getIdeas(prompt);

    const text = res.data; // IMPORTANT

    const easy = text.match(/EASY:\s*(.*?)(?=\nMEDIUM:|$)/s)?.[1]?.trim();
    const medium = text.match(/MEDIUM:\s*(.*?)(?=\nHARD:|$)/s)?.[1]?.trim();
    const hard = text.match(/HARD:\s*(.*)/s)?.[1]?.trim();

    setIdeas([
      { difficulty: "Easy", prompt: easy, image_url: generateImage(easy) },
      { difficulty: "Medium", prompt: medium, image_url: generateImage(medium) },
      { difficulty: "Hard", prompt: hard, image_url: generateImage(hard) },
    ]);

  } catch (err) {
    setError("Could not fetch ideas. Please try again.");
  }

  setLoading(false);
};

  const generateImage = (prompt) => {
  if (!prompt) return null;
  return `https://source.unsplash.com/600x400/?${encodeURIComponent(prompt)}`;
};

  return (
    <div className="page">
      <div className="page-header">
        <span className="page-tag">Inspire</span>
        <h2 className="page-title">What Can I Draw?</h2>
        <p className="page-sub">Describe anything and get three drawing ideas with reference images.</p>
      </div>

      <div className="page-body">
        <div className="input-row">
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. a butterfly, rainy street, fantasy castle..."
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />
          <button
            className="action-btn"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? (
              <span className="btn-loading"><span className="spinner" /> Generating...</span>
            ) : (
              "Get Ideas →"
            )}
          </button>
        </div>

        {error && <p className="error-msg">{error}</p>}

        <div className="ideas-grid">
          {ideas.map((idea, i) => (
            <ResultCard key={i}>
              <div className="idea-image-wrap">
                {idea.image_url ? (
                  <img
                    src={idea.image_url}
                    alt={idea.difficulty}
                    className="idea-image"
                  />
                ) : (
                  <div className="idea-image-placeholder">Generating...</div>
                )}
                <span
                  className="difficulty-badge"
                  style={{ background: DIFFICULTY_COLOR[idea.difficulty] }}
                >
                  {idea.difficulty}
                </span>
              </div>
              <p className="idea-prompt">{idea.prompt}</p>
            </ResultCard>
          ))}
        </div>
      </div>
    </div>
  );
}