import { Link } from "react-router-dom";

export default function Navigation({ hideLinks = false }) {
  return (
    <nav className="marketing-navbar">
      <Link to="/" className="workspace-navbar__brand">
        GrammarDSL
      </Link>

      {!hideLinks && (
        <div className="marketing-navbar__actions">
          <div className="marketing-navbar__links">
            <a href="#services" className="workspace-navbar__link">
              Services
            </a>
            <Link to="/grammar" className="workspace-navbar__link">
              Grammar Workspace
            </Link>
          </div>

          <div className="marketing-navbar__buttons">
            <Link to="/login" className="marketing-navbar__button marketing-navbar__button--ghost">
              Login
            </Link>
            <Link to="/register" className="marketing-navbar__button">
              Sign up
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
