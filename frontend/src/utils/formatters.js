// Small formatting helpers shared by the analyzer result mappers. These only
// reformat values that already exist in a response — they never invent data.

const CATEGORY_LABELS = {
  banking_or_kyc_scam: "Banking / KYC Scam",
  credential_theft: "Credential Theft",
  lottery_or_reward_scam: "Lottery / Reward Scam",
  fake_job_scam: "Fake Job Offer",
  shopping_or_delivery_scam: "Shopping / Delivery Scam",
  malicious_download: "Malicious Download",
  social_engineering: "Social Engineering",
  general_suspicious_message: "General Suspicious Message",
  general_suspicious_url: "General Suspicious URL",
  phishing_or_impersonation: "Phishing / Impersonation",
  suspicious_ip_url: "Suspicious IP Address",
  suspicious_redirect: "Suspicious Redirect",
  no_clear_threat_detected: "No Clear Threat Detected",
  invalid_url: "Invalid URL",
  invalid_phone_number: "Invalid Phone Number",
  service_number: "Emergency / Service Number",
  spam_phone_number: "Spam Number",
  suspicious_phone_number: "Suspicious Number",
  suspicious_activity: "Suspicious Activity",
  telemarketing_spam: "Telemarketing Spam",
  investment_scam: "Investment Scam",
  general_scam_phone: "Scam Number",
};

export function formatCategory(rawCategory) {
  if (!rawCategory) return null;
  if (CATEGORY_LABELS[rawCategory]) return CATEGORY_LABELS[rawCategory];
  return rawCategory
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

const NUMBER_TYPE_LABELS = {
  mobile: "Mobile",
  landline: "Landline",
  mobile_or_landline: "Mobile or Landline",
  toll_free: "Toll-Free",
  premium_rate: "Premium Rate",
  shared_cost: "Shared Cost",
  voip: "VoIP",
  personal: "Personal Number",
  pager: "Pager",
  indian_service_number: "Indian Service Number",
  unknown: "Unknown",
};

export function formatNumberType(rawType) {
  if (!rawType) return null;
  return NUMBER_TYPE_LABELS[rawType] || formatCategory(rawType);
}

// Small friendly-name map for common regions; falls back to the raw ISO
// code the backend/engine returns rather than guessing at unlisted ones.
// Note: the backend's own get_phone_country() can legitimately return the
// literal string "Unknown" when phonenumbers can't determine a region for
// an otherwise-valid number — that is a real returned value, not a missing
// field, so it is formatted and shown as-is rather than treated as absent.
const COUNTRY_NAMES = {
  IN: "India",
  US: "United States",
  GB: "United Kingdom",
  CA: "Canada",
  AU: "Australia",
  AE: "United Arab Emirates",
  SG: "Singapore",
};

export function formatCountry(rawCountry) {
  if (!rawCountry) return null;
  return COUNTRY_NAMES[rawCountry] ? `${COUNTRY_NAMES[rawCountry]} (${rawCountry})` : rawCountry;
}

export function formatRiskLevel(riskLevel) {
  if (riskLevel === "not_applicable") return "Not Applicable";
  if (!riskLevel) return null;
  return riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1);
}

// CSS variable name (defined in index.css) to color-code by risk level.
export function riskLevelToColorVar(riskLevel) {
  switch (riskLevel) {
    case "high":
      return "var(--risk-high)";
    case "medium":
      return "var(--risk-medium)";
    case "low":
      return "var(--risk-low)";
    default:
      return "var(--text-tertiary)";
  }
}

export function formatConfidence(confidence) {
  if (!confidence) return null;
  return confidence.charAt(0).toUpperCase() + confidence.slice(1);
}

export function formatTimestamp(date) {
  return date.toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}