import { MessageSquare, Link2, Phone, ArrowRight } from "lucide-react";
import "./HomeHero.css";

const HOME_ANALYZERS = [
  {
    id: "message",
    icon: MessageSquare,
    title: "Message Analyzer",
    tagline: "Find what's odd in the conversation.",
    description:
      "Analyze SMS, WhatsApp messages, and emails for unusual patterns and scam indicators.",
  },
  {
    id: "url",
    icon: Link2,
    title: "URL Analyzer",
    tagline: "Look beyond the link.",
    description: "Check URLs for unusual patterns and phishing indicators before you open them.",
  },
  {
    id: "phone",
    icon: Phone,
    title: "Phone Analyzer",
    tagline: "Know who's really calling.",
    description: "Check phone numbers for signals commonly associated with scams.",
  },
];

function HomeHero({ onSelectAnalyzer }) {
  return (
    <div className="home-hero">
      <div className="home-hero-content">
        <p className="home-hero-eyebrow">ODDITY Cyber India</p>

        <h1 className="home-hero-title">
          Something feels off?
          <span>Spot what's out of place.</span>
        </h1>

        <p className="home-hero-lead">
          Not every scam looks suspicious at first glance. ODDITY analyzes messages, URLs, and
          phone numbers to detect unusual patterns, inconsistencies, and red flags — helping you
          understand what's wrong before you interact.
        </p>

        <div className="home-hero-analyzers">
          {HOME_ANALYZERS.map(({ id, icon: Icon, title, tagline, description }) => (
            <button
              key={id}
              type="button"
              className="home-hero-analyzer"
              onClick={() => onSelectAnalyzer(id)}
            >
              <span className="home-hero-analyzer-icon">
                <Icon size={20} strokeWidth={2} aria-hidden="true" />
              </span>
              <span className="home-hero-analyzer-text">
                <span className="home-hero-analyzer-title">{title}</span>
                <span className="home-hero-analyzer-tagline">{tagline}</span>
                <span className="home-hero-analyzer-desc">{description}</span>
              </span>
            </button>
          ))}
        </div>

        <button
          type="button"
          className="home-hero-cta"
          onClick={() => onSelectAnalyzer("message")}
        >
          Find Out Why
          <ArrowRight size={16} strokeWidth={2} aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}

export default HomeHero;