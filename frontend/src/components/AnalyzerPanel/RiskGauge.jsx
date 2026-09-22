import "./RiskGauge.css";

const SEGMENT_COUNT = 26;
const START_ANGLE = -130; // degrees from 12 o'clock, clockwise
const SWEEP = 260;
const CENTER = 100;
const TICK_RADIUS = 74;
const TICK_LENGTH = 20;
const TICK_WIDTH = 7;

// Fixed colour ramp, independent of theme — a gauge's green/yellow/orange/red
// language is a security convention, not a theme choice. Stops are placed so
// the *last* stop (pure red) only lands on the very final segment; nothing
// before position 1.0 reaches it, which is what keeps a score like 75 from
// reading as "fully red."
const COLOR_STOPS = [
  { at: 0, color: [34, 197, 94] },    // risk-low
  { at: 0.45, color: [234, 179, 8] }, // risk-medium
  { at: 0.75, color: [249, 115, 22] },// risk-high
  { at: 1, color: [239, 68, 68] },    // risk-critical
];

function colorAtPosition(fraction) {
  for (let i = 0; i < COLOR_STOPS.length - 1; i++) {
    const a = COLOR_STOPS[i];
    const b = COLOR_STOPS[i + 1];
    if (fraction >= a.at && fraction <= b.at) {
      const t = (fraction - a.at) / (b.at - a.at || 1);
      const r = Math.round(a.color[0] + (b.color[0] - a.color[0]) * t);
      const g = Math.round(a.color[1] + (b.color[1] - a.color[1]) * t);
      const bl = Math.round(a.color[2] + (b.color[2] - a.color[2]) * t);
      return `rgb(${r}, ${g}, ${bl})`;
    }
  }
  const last = COLOR_STOPS[COLOR_STOPS.length - 1].color;
  return `rgb(${last[0]}, ${last[1]}, ${last[2]})`;
}

function RiskGauge({ riskScore, riskLevelLabel, riskColor, status }) {
  const hasScore = typeof riskScore === "number";
  const clamped = hasScore ? Math.max(0, Math.min(riskScore, 100)) : 0;
  const litCount = hasScore ? Math.round((clamped / 100) * SEGMENT_COUNT) : 0;

  const segments = Array.from({ length: SEGMENT_COUNT }, (_, i) => {
    const fraction = SEGMENT_COUNT === 1 ? 0 : i / (SEGMENT_COUNT - 1);
    const angle = START_ANGLE + SWEEP * fraction;
    const isLit = i < litCount;
    return { angle, isLit, color: colorAtPosition(fraction) };
  });

  return (
    <div className={`risk-gauge${status === "loading" ? " is-loading" : ""}`}>
      <svg
        viewBox="0 0 200 200"
        className="risk-gauge-svg"
        role="img"
        aria-label={hasScore ? `Risk score ${clamped} out of 100` : "Risk score not yet available"}
      >
        <circle className="risk-gauge-well" cx={CENTER} cy={CENTER} r={TICK_RADIUS + 2} />
        {segments.map(({ angle, isLit, color }, i) => (
          <rect
            key={i}
            className={`risk-gauge-segment${isLit ? " is-lit" : ""}`}
            x={CENTER - TICK_WIDTH / 2}
            y={CENTER - TICK_RADIUS - TICK_LENGTH / 2}
            width={TICK_WIDTH}
            height={TICK_LENGTH}
            rx={2}
            transform={`rotate(${angle} ${CENTER} ${CENTER})`}
            style={isLit ? { fill: color, "--tick-glow": color } : undefined}
          />
        ))}
      </svg>

      <div className="risk-gauge-center">
        <span className="risk-gauge-value">{hasScore ? clamped : "—"}</span>
        <span className="risk-gauge-max">/ 100</span>
        {riskLevelLabel && (
          <span className="risk-gauge-level" style={{ "--score-color": riskColor }}>
            {riskLevelLabel}
          </span>
        )}
      </div>
    </div>
  );
}

export default RiskGauge;