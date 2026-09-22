import {
  ShieldCheck,
  Loader2,
  AlertTriangle,
  Globe,
  Smartphone,
  Flag,
  Clock,
  ListChecks,
} from "lucide-react";

function ResultSummary({ result }) {
  return (
    <div className="result-summary-row">
      <span className="result-risk-chip" style={{ "--score-color": result.riskColor }}>
        {result.riskLevelLabel}
      </span>
      {result.categoryLabel && (
        <span className="result-category">{result.categoryLabel}</span>
      )}
    </div>
  );
}

function InfoChip({ icon: Icon, label, value }) {
  if (!value) return null;
  return (
    <div className="analyzer-meta-chip">
      <Icon size={16} strokeWidth={2} aria-hidden="true" />
      <div>
        <p className="analyzer-meta-label">{label}</p>
        <p className="analyzer-meta-value">{value}</p>
      </div>
    </div>
  );
}

function ReputationBlock({ reputation }) {
  if (!reputation) return null;

  return (
    <div className="reputation-block">
      <div className="glass-card-heading">
        <Flag size={16} strokeWidth={2} aria-hidden="true" />
        <span>REPUTATION DATA</span>
      </div>
      <div className="reputation-grid">
        <InfoChip icon={ShieldCheck} label="Classification" value={reputation.classificationLabel} />
        <InfoChip icon={ListChecks} label="Reported Category" value={reputation.categoryLabel} />
        <InfoChip icon={Flag} label="Report Count" value={String(reputation.reportCount)} />
        <InfoChip icon={Globe} label="Source Count" value={String(reputation.sourceCount)} />
        <InfoChip icon={ShieldCheck} label="Confidence" value={reputation.confidenceLabel} />
      </div>
      {reputation.conflictingEvidence && (
        <p className="reputation-conflict-note">
          <AlertTriangle size={14} strokeWidth={2} aria-hidden="true" />
          The sample dataset contains conflicting classifications for this number.
        </p>
      )}
    </div>
  );
}

function AnalyzerResult({ status, errorMessage, result }) {
  if (status === "loading") {
    return (
      <div className="analyzer-result-empty">
        <Loader2 size={32} strokeWidth={1.5} className="spin" aria-hidden="true" />
        <p className="analyzer-result-title">Analyzing…</p>
        <p className="analyzer-result-sub">This usually takes a moment.</p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="analyzer-result-empty analyzer-result-error" role="alert">
        <AlertTriangle size={32} strokeWidth={1.5} aria-hidden="true" />
        <p className="analyzer-result-title">Something went wrong</p>
        <p className="analyzer-result-sub">
          {errorMessage || "The analyzer could not complete. Please try again."}
        </p>
      </div>
    );
  }

  if (status !== "success" || !result) {
    return (
      <div className="analyzer-result-empty">
        <ShieldCheck size={32} strokeWidth={1.5} aria-hidden="true" />
        <p className="analyzer-result-title">No analysis yet</p>
        <p className="analyzer-result-sub">
          Enter details above and click Analyze to see the results
        </p>
      </div>
    );
  }

  return (
    <div className="analyzer-result-success" aria-live="polite">
      <ResultSummary result={result} />

      {result.kind === "url" && result.analyzedUrl && (
        <p className="result-analyzed-url">{result.analyzedUrl}</p>
      )}

      {result.kind === "phone" && (
        <div className="analyzer-meta-row analyzer-meta-row-compact">
          <InfoChip icon={Globe} label="Country" value={result.countryLabel} />
          <InfoChip icon={Smartphone} label="Number Type" value={result.numberTypeLabel} />
        </div>
      )}

      {result.kind === "phone" && <ReputationBlock reputation={result.reputation} />}

      {result.indicators.length > 0 && (
        <div className="result-indicators">
          <div className="glass-card-heading">
            <ListChecks size={16} strokeWidth={2} aria-hidden="true" />
            <span>DETECTED INDICATORS</span>
          </div>
          <ul>
            {result.indicators.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </div>
      )}

      {result.recommendation && (
        <div className="result-recommendation">
          <p>{result.recommendation}</p>
        </div>
      )}

      <p className="result-analyzed-at">
        <Clock size={13} strokeWidth={2} aria-hidden="true" />
        Analyzed at {result.analyzedAtLabel}
      </p>
    </div>
  );
}

export default AnalyzerResult;