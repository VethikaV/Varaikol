import { useState, useEffect } from "react";
import { analyzeDrawing } from "../api/client";
import ImageUpload from "../components/ImageUpload";
import ResultCard from "../components/ResultCard";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./style.css";

export default function AnalyzePage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Generate preview when file changes
  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    return () => URL.revokeObjectURL(url);
  }, [file]);

  const handleFileSelect = (f) => {
    setFile(f);
    setResult(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please upload a valid image file.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("File size should be less than 5MB.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeDrawing(file);
      setResult(data);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="page-tag">Improve</span>
        <h2 className="page-title">Analyze My Drawing</h2>
        <p className="page-sub">
          Upload your artwork and receive AI feedback on medium, style, and tips to improve.
        </p>
      </div>

      <div className="page-body">
        <ImageUpload onFileSelect={handleFileSelect} label="Upload your drawing" />

        <button
          className="action-btn"
          onClick={handleAnalyze}
          disabled={loading || !file}
        >
          {loading ? (
            <span className="btn-loading"><span className="spinner" /> Analyzing...</span>
          ) : (
            "Analyze Drawing →"
          )}
        </button>

        {error && <p className="error-msg">{error}</p>}

        {/* RESULT SECTION */}

        {result && (
  <div className="analyze-result">
    <ResultCard title="Analysis Result" className="analyze-result-card">
      <div className="analyze-layout">
        {/* ... rest unchanged ... */} {/* LEFT: IMAGE */}
                <div className="analyze-image-box">
                  {previewUrl && (
                    <img
                      src={previewUrl}
                      alt="uploaded artwork"
                      className="analyze-image"
                    />
                  )}
                </div>

                {/* RIGHT: CONTENT */}
                <div className="analyze-content">
                  {/* MEDIUM */}
                 <div className="info-block">
  <span className="label">Detected Medium</span>
  <div className="value highlight">
    {result?.medium || "Unknown"}
  </div>
                 </div>
 
                   {/* COLORS */}
                 {result?.colors?.length > 0 && (
                 <div className="info-block">
                  <span className="label">Colors Used</span>
                   <div className="colors-list">
                   {result.colors.map((color, index) => (
                   <span key={index} className="color-chip">
                   {color}
                  </span>
                     ))}
                   </div>
                   </div>
                  )} 

                  {/* FEEDBACK */}
                 <div className="info-block">
               <span className="label">Feedback</span>
             <div className="feedback-text markdown-body">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {result?.feedback || "No feedback available"}
             </ReactMarkdown>
            </div>
           </div>

                  {/* TIPS */}
                  {result?.tips?.length > 0 && (
                    <div className="info-block">
                      <span className="label">Improvement Tips</span>
                      <ul className="tips-list">
                        {result.tips.map((tip, i) => (
                          <li key={i}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              
      </div>
    </ResultCard>
  </div>
)}
       
      </div>
    </div>
  );
}