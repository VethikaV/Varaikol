import { useState } from "react";
import { convertSketch } from "../api/client";
import ImageUpload from "../components/ImageUpload";
import ResultCard from "../components/ResultCard";
import "./style.css";

export default function SketchPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [sketch, setSketch] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleFileSelect = (f) => {
  console.log("Received:", f);
  console.log("Is File?", f instanceof File);

  setFile(f);

  if (f instanceof File) {
    setPreview(URL.createObjectURL(f));
  } else {
    console.error("Not a File object:", f);
  }

  setSketch(null);
};

  const handleConvert = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const data = await convertSketch(file);
      setSketch(data.sketch);
    } catch (err) {
      setError("Conversion failed. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="page-tag">Transform</span>
        <h2 className="page-title">Photo to Sketch</h2>
        <p className="page-sub">Upload any photo and get a clean pencil outline instantly.</p>
      </div>

      <div className="page-body">
        <ImageUpload onFileSelect={handleFileSelect} label="Upload a photo" />

        <button
          className="action-btn"
          onClick={handleConvert}
          disabled={loading || !file}
        >
          {loading ? (
            <span className="btn-loading"><span className="spinner" /> Converting...</span>
          ) : (
            "Convert to Sketch →"
          )}
        </button>

        {error && <p className="error-msg">{error}</p>}

        {(preview || sketch) && (
          <div className="sketch-compare">
            {preview && (
              <ResultCard title="Original Photo">
                <img src={preview} alt="original" className="sketch-img" />
              </ResultCard>
            )}
            {sketch && (
              <ResultCard title="Pencil Outline">
                <img
                  src={`data:image/png;base64,${sketch}`}
                  alt="sketch"
                  className="sketch-img"
                />
              </ResultCard>
            )}
          </div>
        )}
      </div>
    </div>
  );
}