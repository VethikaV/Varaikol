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
      const data = await getIdeas(prompt);
      setIdeas([
        { difficulty: "Easy",   prompt: data.easy?.prompt,   image_url: data.easy?.image },
        { difficulty: "Medium", prompt: data.medium?.prompt, image_url: data.medium?.image },
        { difficulty: "Hard",   prompt: data.hard?.prompt,   image_url: data.hard?.image },
      ]);
    } catch (err) {
      setError("Could not fetch ideas. Please try again.");
    }
    setLoading(false);
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