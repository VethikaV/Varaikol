import { useState, useEffect, useRef } from "react";
import "../pages/style.css";

export default function ImageUpload({
  onFileSelect,
  label = "Upload Image"
}) {
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);

  const inputRef = useRef(null);

  const validateFile = (file) => {
    if (!file.type.startsWith("image/")) {
      setError("Only image files are allowed.");
      return false;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("File must be under 5MB.");
      return false;
    }

    setError(null);
    return true;
  };

  const handleFile = (file) => {
    if (!file) return;
    if (!validateFile(file)) return;

    onFileSelect(file);

    const url = URL.createObjectURL(file);
    setPreview(url);
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    handleFile(file);

    e.target.value = "";
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  return (
    <div className="upload-wrapper">
      <div
        className={`upload-card ${dragActive ? "drag-active" : ""}`}
        onDrop={handleDrop}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
      >
        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="preview" className="upload-preview" />

            <button
              type="button"
              className="remove-btn"
              onClick={() => {
                setPreview(null);
                onFileSelect(null);
              }}
            >
              ✕ Remove
            </button>
          </div>
        ) : (
          <div className="dropzone">
            <div className="upload-icon">📤</div>
            <h3>{label}</h3>
            <p>Drag & drop your file here</p>
            <span className="hint">PNG, JPG, JPEG (max 5MB)</span>

            {/* IMPORTANT FIX */}
            <button
              type="button"
              className="upload-btn"
              onClick={() => inputRef.current.click()}
            >
              Choose File
            </button>

            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              onChange={handleChange}
              hidden
            />
          </div>
        )}
      </div>

      {error && <p className="upload-error">{error}</p>}
    </div>
  );
}