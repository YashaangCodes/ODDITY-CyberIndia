// Architecture B: the Python backend is the only analysis engine. This
// module does exactly three things per call — build a request, POST it to
// the real FastAPI endpoint, and return the parsed JSON response (or throw
// a readable error). No scoring, no regex, no phone/brand logic lives here
// or anywhere else in the frontend.
//
// Override the backend location with a .env file if it's not on localhost:
//   VITE_API_BASE_URL=http://127.0.0.1:8000

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function postJson(path, body) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch (networkError) {
    throw new Error(
      `Could not reach the ODDITY backend at ${API_BASE_URL}. Is it running? (${networkError.message})`,
      { cause: networkError }
    );
  }

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    // Some error responses may have no body at all — fall through to the
    // status-based message below instead of throwing here.
  }

  if (!response.ok) {
    const detail = Array.isArray(payload?.detail)
      ? payload.detail.map((item) => item.msg || JSON.stringify(item)).join("; ")
      : payload?.detail || `Request failed with status ${response.status}.`;
    throw new Error(detail);
  }

  if (payload === null) {
    throw new Error("The backend returned an empty or non-JSON response.");
  }

  return payload;
}

export function analyzeMessage(text) {
  return postJson("/api/v1/analyze/message", { text });
}

export function analyzeUrl(url) {
  return postJson("/api/v1/analyze/url", { url });
}

export function analyzePhoneNumber(phoneNumber) {
  return postJson("/api/v1/analyze/phone", { phone_number: phoneNumber });
}