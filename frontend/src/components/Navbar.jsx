import "../pages/style.css";

export default function Navbar({ active, setActive, tabs }) {
  return (
    <nav className="navbar">
      {tabs.map((t, i) => {
        const Icon = t.icon;
        const isActive = active === i;

        return (
          <button
            key={t.label}
            className={`navbar-item ${isActive ? "navbar-item-active" : ""}`}
            onClick={() => setActive(i)}
          >
            <Icon size={18} className="navbar-icon" />
            <span>{t.label}</span>
          </button>
        );
      })}
    </nav>
  );
}