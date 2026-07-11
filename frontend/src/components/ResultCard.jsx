import { useState } from "react";
import "../pages/style.css";

export default function ResultCard({
  title,
  children,
  loading = false,
  icon = null,
  emptyText = null,
  className = "",
  actions = null,
}) {

  const [preview, setPreview] = useState(null);

  const handleClick = (e) => {
    if (e.target.tagName === "IMG") {
      setPreview(e.target.src);
    }
  };

  return (
    <>
      <div
        className={`result-card ${className}`}
        onClick={handleClick}
      >
        {(title || icon) && (
          <div className="result-header">
            {icon && <span className="result-icon">{icon}</span>}
            {title && <h3 className="result-title">{title}</h3>}
          </div>
        )}

        <div className="result-body">
          {loading ? (
            <div className="result-loading">
              <div className="spinner" />
              <p>Analyzing...</p>
            </div>
          ) : children ? (
            children
          ) : (
            emptyText && <p className="result-empty">{emptyText}</p>
          )}
        </div>

        {actions && <div className="result-actions">{actions}</div>}
      </div>

      {preview && (
  <div className="image-modal" onClick={() => setPreview(null)}>
    <div
      className="image-modal-content"
      onClick={(e) => e.stopPropagation()}
    >
      <div className="image-toolbar">
        <a href={preview} download="sketch.png" className="toolbar-btn">
          <i className="fa-solid fa-download"></i>
        </a>

        <button
          className="toolbar-btn"
          onClick={() => setPreview(null)}
        >
          <i className="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div className="image-scroll">
        <img src={preview} alt="Preview" className="modal-image" />
      </div>
    </div>
  </div>
)}
    </>
  );
}