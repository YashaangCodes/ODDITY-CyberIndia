import logoDark from "../../assets/logo-dark.png";
import logoLight from "../../assets/logo-light.png";
import { useTheme } from "../../hooks/useTheme.js";
import "./Logo.css";

function Logo() {
  const { theme } = useTheme();
  const logoSrc = theme === "dark" ? logoDark : logoLight;

  return (
    <div className="app-logo">
      <img src={logoSrc} alt="ODDITY Cyber India" className="app-logo-img" />
    </div>
  );
}

export default Logo;