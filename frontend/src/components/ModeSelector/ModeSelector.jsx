import "./ModeSelector.css";

function ModeSelector({ mode, onChange, fullWidth }) {
  return (
    <div
      className={`mode-selector${fullWidth ? " mode-selector-full" : ""}`}
      role="tablist"
      aria-label="Analyzer tier"
    >
      <button
        type="button"
        role="tab"
        aria-selected={mode === "basic"}
        className={`mode-pill${mode === "basic" ? " is-active" : ""}`}
        onClick={() => onChange("basic")}
      >
        Basic
      </button>
      <button
        type="button"
        role="tab"
        aria-selected={mode === "advanced"}
        className="mode-pill mode-pill-disabled"
        disabled
        aria-disabled="true"
        title="Advanced tools are not yet available"
      >
        Advanced
      </button>
    </div>
  );
}

export default ModeSelector;