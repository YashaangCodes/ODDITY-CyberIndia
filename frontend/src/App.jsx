import { useState } from "react";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("Not checked");
  const [isLoading, setIsLoading] = useState(false);

  async function checkBackend() {
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/health");

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      setBackendStatus(data.status);
    } catch (error) {
      setBackendStatus(`Connection failed: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <h1>ODDITY Cyber India</h1>
      <p>Find what doesn't fit.</p>

      <button onClick={checkBackend} disabled={isLoading}>
        {isLoading ? "Checking..." : "Check Backend"}
      </button>

      <p>
        Backend status: <strong>{backendStatus}</strong>
      </p>
    </main>
  );
}

export default App;