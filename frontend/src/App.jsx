import { useState } from "react";
import Logo from "./components/Logo/Logo.jsx";
import Sidebar from "./components/Sidebar/Sidebar.jsx";
import Navbar from "./components/Navbar/Navbar.jsx";
import HomeHero from "./components/Home/HomeHero.jsx";
import AnalyzerPanel from "./components/AnalyzerPanel/AnalyzerPanel.jsx";
import { ShieldAlert, Users } from "lucide-react";
import "./App.css";

function App() {
  const [mode, setMode] = useState("basic");
  const [activeAnalyzer, setActiveAnalyzer] = useState("message");
  const [activeSection, setActiveSection] = useState("home");

  function goToSection(sectionId) {
    setActiveSection(sectionId);
    document.getElementById(sectionId)?.scrollIntoView({ behavior: "smooth" });
  }

  function selectAnalyzerAndGo(id) {
    setActiveAnalyzer(id);
    goToSection("tools");
  }

  return (
    <>
      <div className="app-left-rail">
        <Logo />
        <Sidebar
          mode={mode}
          onModeChange={setMode}
          activeAnalyzer={activeAnalyzer}
          onSelectAnalyzer={selectAnalyzerAndGo}
        />
      </div>

      <div className="app-panel">
        <div className="app-body">
          <div className="app-content-column">
          <div className="navbar-row">
            <Navbar activeSection={activeSection} onNavigate={setActiveSection} />
          </div>

          <section id="home" className="section-panel home-section">
            <HomeHero onSelectAnalyzer={selectAnalyzerAndGo} />
          </section>

          <section id="tools" className="section-panel tools-section">
            <AnalyzerPanel analyzerType={activeAnalyzer} />
          </section>

          <section id="learn" className="section-panel section-panel-full">
            <div className="section-panel-heading">
              <ShieldAlert size={20} strokeWidth={2} aria-hidden="true" />
              <h2>Learn About Scams</h2>
            </div>
            <p className="section-panel-lead">
              Scammers rely on urgency, impersonation, and unfamiliar formats to catch
              people off guard. Understanding common patterns — fake KYC requests, prize
              and lottery lures, unofficial job offers, and OTP-sharing tricks — is often
              the fastest way to spot trouble before it costs you anything.
            </p>
          </section>

          <section id="more" className="section-panel section-panel-full">
            <div className="section-panel-heading">
              <Users size={20} strokeWidth={2} aria-hidden="true" />
              <h2>More About Us</h2>
            </div>
            <p className="section-panel-lead">
              ODDITY Cyber India is a scam-awareness project built to give people a fast,
              free way to check suspicious messages, links, and phone numbers against
              known patterns — no account, no data collection beyond what's needed to run
              the analysis.
            </p>
          </section>
        </div>
        </div>
      </div>
    </>
  );
}

export default App;