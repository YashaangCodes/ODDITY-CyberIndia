import ThemeToggle from "../ThemeToggle/ThemeToggle.jsx";
import "./Navbar.css";

const SECTION_LINKS = [
  { id: "home", label: "Home" },
  { id: "tools", label: "Tools" },
  { id: "learn", label: "Learn About Scams" },
  { id: "more", label: "More About Us" },
];

function Navbar({ activeSection, onNavigate }) {
  function handleNavClick(event, sectionId) {
    event.preventDefault();
    onNavigate(sectionId);
    document.getElementById(sectionId)?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <header className="navbar">
      <nav className="navbar-links" aria-label="Page sections">
        {SECTION_LINKS.map(({ id, label }) => (
          <a key={id} href={`#${id}`} className={activeSection === id ? "is-active" : undefined}
             aria-current={activeSection === id ? "true" : undefined}
             onClick={(event) => handleNavClick(event, id)}>
            {label}
          </a>
        ))}
      </nav>
      <ThemeToggle />
    </header>
  );
}

export default Navbar;