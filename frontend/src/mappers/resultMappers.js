// raw analyzer response -> UI-friendly display model, one mapper per
// analyzer since the three backend schemas are genuinely different (see
// the audit notes delivered alongside this code). Each mapper:
//   - keeps every meaningful field from the raw response
//   - sets a UI field to `null` when the backend didn't return it, so
//     components can omit that row entirely instead of showing "Unknown"
//   - never invents a value the response doesn't contain
//
// analyzedAt is a client-side timestamp of when the result was received —
// it is UI metadata about the request/response cycle, not an analysis
// finding, and neither backend nor engine returns one.

import {
  formatCategory,
  formatCountry,
  formatNumberType,
  formatRiskLevel,
  formatConfidence,
  formatTimestamp,
  riskLevelToColorVar,
} from "../utils/formatters.js";

function baseFields(raw, analyzedAt) {
  return {
    riskScore: raw.risk_score, // number | null
    safetyScore: raw.safety_score, // number | null
    riskLevel: raw.risk_level,
    riskLevelLabel: formatRiskLevel(raw.risk_level),
    riskColor: riskLevelToColorVar(raw.risk_level),
    category: raw.threat_category || null,
    categoryLabel: formatCategory(raw.threat_category),
    indicators: raw.reasons || [],
    recommendation: raw.recommendation || null,
    analyzedAtLabel: formatTimestamp(analyzedAt),
  };
}

export function mapMessageAnalysisResponse(raw, analyzedAt) {
  return {
    kind: "message",
    ...baseFields(raw, analyzedAt),
  };
}

export function mapUrlAnalysisResponse(raw, analyzedAt) {
  return {
    kind: "url",
    ...baseFields(raw, analyzedAt),
    // analyzed_url is an echo of the (normalized) input, added by the
    // engine for display context — it is not part of the backend's
    // URLResponse schema.
    analyzedUrl: raw.analyzed_url || null,
  };
}

export function mapPhoneAnalysisResponse(raw, analyzedAt) {
  const reputation = raw.reputation_evidence
    ? {
        classification: raw.reputation_evidence.classification,
        classificationLabel: formatCategory(raw.reputation_evidence.classification),
        categoryLabel: formatCategory(raw.reputation_evidence.category),
        reportCount: raw.reputation_evidence.report_count,
        sourceCount: raw.reputation_evidence.source_count,
        confidenceLabel: formatConfidence(raw.reputation_evidence.confidence),
        conflictingEvidence: raw.reputation_evidence.conflicting_evidence,
      }
    : null;

  return {
    kind: "phone",
    ...baseFields(raw, analyzedAt),
    country: raw.country || null,
    countryLabel: formatCountry(raw.country),
    numberType: raw.number_type || null,
    numberTypeLabel: formatNumberType(raw.number_type),
    reputation,
  };
}