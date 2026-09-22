import { useState } from "react";
import {
  MessageSquare,
  Link2,
  Phone,
  PenLine,
  TrendingUp,
  Search,
  Gauge,
} from "lucide-react";
import {
  analyzeMessage,
  analyzeUrl,
  analyzePhoneNumber,
} from "../../services/analyzerService.js";
import {
  mapMessageAnalysisResponse,
  mapUrlAnalysisResponse,
  mapPhoneAnalysisResponse,
} from "../../mappers/resultMappers.js";
import AnalyzerResult from "./AnalyzerResult.jsx";
import RiskGauge from "./RiskGauge.jsx";
import "./AnalyzerPanel.css";

const ANALYZER_CONFIG = {
  message: {
    icon: MessageSquare,
    titlePlain: "MESSAGE",
    titleAccent: "ANALYZER",
    description:
      "Analyze suspicious messages, SMS, WhatsApp texts, and emails to detect potential scams and fraud attempts.",
    inputLabel: "ENTER MESSAGE",
    inputSub: "Paste the suspicious message below",
    placeholder: "Type or paste the message here...",
    maxLength: 5000,
    minLength: 3,
    multiline: true,
    buttonLabel: "Analyze Message",
    run: analyzeMessage,
    map: mapMessageAnalysisResponse,
  },
  url: {
    icon: Link2,
    titlePlain: "URL",
    titleAccent: "ANALYZER",
    description:
      "Check a suspicious link before you open it — spot phishing pages, redirects, and lookalike domains.",
    inputLabel: "ENTER URL",
    inputSub: "Paste the suspicious link below",
    placeholder: "https://example.com",
    maxLength: 2048,
    minLength: 1,
    multiline: false,
    buttonLabel: "Analyze URL",
    run: analyzeUrl,
    map: mapUrlAnalysisResponse,
  },
  phone: {
    icon: Phone,
    titlePlain: "PHONE",
    titleAccent: "ANALYZER",
    description:
      "Check an unknown number against known scam and spam patterns before you call back.",
    inputLabel: "ENTER PHONE NUMBER",
    inputSub: "Include the country code if you have it",
    placeholder: "+91 XXXXX XXXXX",
    maxLength: 25,
    minLength: 3,
    multiline: false,
    buttonLabel: "Analyze Phone Number",
    run: analyzePhoneNumber,
    map: mapPhoneAnalysisResponse,
  },
};

const ANALYZER_TYPES = Object.keys(ANALYZER_CONFIG);

function initialPerAnalyzerState(defaultValue) {
  return ANALYZER_TYPES.reduce((acc, type) => {
    acc[type] = defaultValue;
    return acc;
  }, {});
}

function AnalyzerPanel({ analyzerType }) {
  // Separate state per analyzer so switching tools never leaks another
  // analyzer's input, result, or error onto the current one.
  const [inputs, setInputs] = useState(() => initialPerAnalyzerState(""));
  const [statuses, setStatuses] = useState(() => initialPerAnalyzerState("idle"));
  const [results, setResults] = useState(() => initialPerAnalyzerState(null));
  const [errors, setErrors] = useState(() => initialPerAnalyzerState(null));

  const config = ANALYZER_CONFIG[analyzerType] ?? ANALYZER_CONFIG.message;
  const Icon = config.icon;
  const InputTag = config.multiline ? "textarea" : "input";

  const value = inputs[analyzerType];
  const status = statuses[analyzerType];
  const result = results[analyzerType];
  const errorMessage = errors[analyzerType];

  const trimmedLength = value.trim().length;
  const canSubmit = trimmedLength >= config.minLength && status !== "loading";

  function handleInputChange(event) {
    const nextValue = event.target.value;
    setInputs((current) => ({ ...current, [analyzerType]: nextValue }));
  }

  async function handleAnalyze() {
    if (!canSubmit) return;

    const type = analyzerType;
    setStatuses((current) => ({ ...current, [type]: "loading" }));
    setErrors((current) => ({ ...current, [type]: null }));

    try {
      const raw = await config.run(value.trim());
      const mapped = config.map(raw, new Date());
      setResults((current) => ({ ...current, [type]: mapped }));
      setStatuses((current) => ({ ...current, [type]: "success" }));
    } catch (err) {
      // Surface a useful, debuggable error rather than hiding the failure.
      console.error(`[AnalyzerPanel] ${type} analysis failed:`, err);
      setErrors((current) => ({
        ...current,
        [type]: "The analyzer could not process this input. Please try again.",
      }));
      setStatuses((current) => ({ ...current, [type]: "error" }));
    }
  }

  function handleKeyDown(event) {
    if (!config.multiline && event.key === "Enter") {
      event.preventDefault();
      handleAnalyze();
    }
  }

  return (
    <section className="analyzer-panel">
      <header className="analyzer-header">
        <div>
          <h1 className="analyzer-title">
            {config.titlePlain} <span>{config.titleAccent}</span>
          </h1>
          <p className="analyzer-description">{config.description}</p>
        </div>

        <div className="analyzer-badge" aria-hidden="true">
          <Icon size={28} strokeWidth={1.75} />
        </div>
      </header>

      <div className="analyzer-grid">
        <div className="analyzer-left-column">
          <div className="glass-card">
            <div className="glass-card-heading">
              <PenLine size={16} strokeWidth={2} aria-hidden="true" />
              <span>{config.inputLabel}</span>
            </div>
            <p className="glass-card-sub">{config.inputSub}</p>

            <label className="sr-only" htmlFor={`analyzer-input-${analyzerType}`}>
              {config.inputLabel}
            </label>
            <InputTag
              id={`analyzer-input-${analyzerType}`}
              className="analyzer-input"
              placeholder={config.placeholder}
              maxLength={config.maxLength}
              value={value}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              rows={config.multiline ? 8 : undefined}
              disabled={status === "loading"}
            />

            {config.multiline && (
              <div className="analyzer-counter">
                {value.length} / {config.maxLength} characters
              </div>
            )}

            <button
              type="button"
              className="analyzer-button"
              disabled={!canSubmit}
              onClick={handleAnalyze}
            >
              <Search size={16} strokeWidth={2} aria-hidden="true" />
              {status === "loading" ? "Analyzing…" : config.buttonLabel}
            </button>
          </div>

          <div className="glass-card gauge-card">
            <div className="glass-card-heading">
              <Gauge size={16} strokeWidth={2} aria-hidden="true" />
              <span>RISK LEVEL</span>
            </div>
            <RiskGauge
              riskScore={status === "success" ? result?.riskScore ?? null : null}
              riskLevelLabel={status === "success" ? result?.riskLevelLabel : null}
              riskColor={status === "success" ? result?.riskColor : null}
              status={status}
            />
            {status !== "success" && (
              <p className="gauge-card-empty-note">
                {status === "loading"
                  ? "Waiting on the backend…"
                  : status === "error"
                  ? "Unavailable — last request failed."
                  : "Run an analysis to see your risk score."}
              </p>
            )}
          </div>
        </div>

        <div className="glass-card">
          <div className="glass-card-heading">
            <TrendingUp size={16} strokeWidth={2} aria-hidden="true" />
            <span>ANALYSIS RESULT</span>
          </div>
          <p className="glass-card-sub">
            Our analyzer will process your input and show results here
          </p>

          <AnalyzerResult status={status} errorMessage={errorMessage} result={result} />
        </div>
      </div>
    </section>
  );
}

export default AnalyzerPanel;