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
  return (
    <div className={`result-card ${className}`}>

      {/* HEADER */}
      {(title || icon) && (
        <div className="result-header">
          {icon && <span className="result-icon">{icon}</span>}
          {title && <h3 className="result-title">{title}</h3>}
        </div>
      )}

      {/* BODY */}
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

      {/* ACTIONS (NEW) */}
      {actions && <div className="result-actions">{actions}</div>}
    </div>
  );
}