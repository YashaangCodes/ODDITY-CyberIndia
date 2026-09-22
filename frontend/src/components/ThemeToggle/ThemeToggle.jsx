import { Moon, Sun } from "lucide-react";
import { useTheme } from "../../hooks/useTheme.js";
import "./ThemeToggle.css";

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={toggleTheme}
      aria-pressed={isDark}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
    >
      {isDark ? (
        <Moon size={16} strokeWidth={2} />
      ) : (
        <Sun size={16} strokeWidth={2} />
      )}
      <span>{isDark ? "Dark Mode" : "Light Mode"}</span>
      <span className="theme-toggle-track" aria-hidden="true">
        <span className="theme-toggle-thumb" />
      </span>
    </button>
  );
}

export default ThemeToggle;