import { MessageSquare, Link2, Phone } from "lucide-react";
import ModeSelector from "../ModeSelector/ModeSelector.jsx";
import "./Sidebar.css";

const BASIC_TOOLS = [
  { id: "message", label: "Message Analyzer", icon: MessageSquare },
  { id: "url", label: "URL Analyzer", icon: Link2 },
  { id: "phone", label: "Phone Analyzer", icon: Phone },
];

function Sidebar({ mode, onModeChange, activeAnalyzer, onSelectAnalyzer }) {
  return (
    <aside className="sidebar">
      <ModeSelector mode={mode} onChange={onModeChange} fullWidth />

      <nav className="sidebar-nav" aria-label="Basic analysis tools">
        <p className="sidebar-nav-label">Basic Tools</p>
        <ul>
          {BASIC_TOOLS.map(({ id, label, icon: Icon }) => {
            const isActive = activeAnalyzer === id;
            return (
              <li key={id}>
                <button
                  type="button"
                  className={`sidebar-nav-item${isActive ? " is-active" : ""}`}
                  onClick={() => onSelectAnalyzer(id)}
                  aria-current={isActive ? "true" : undefined}
                >
                  <Icon size={18} strokeWidth={2} aria-hidden="true" />
                  <span>{label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="sidebar-promo">
        <p className="sidebar-promo-title">
          ODD —<br />
          Outlier Detection &amp; Diagnostics
        </p>
        <p className="sidebar-promo-tagline">Spot what's out of place.</p>
        <p className="sidebar-promo-sub">
          Every scam leaves something out of place. A strange request. A misleading link. An
          unfamiliar number. ODDITY helps you find it.
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;