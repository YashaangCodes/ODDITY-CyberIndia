# ODDITY Cyber India

### Find what doesn't fit.

**A rule-based digital threat investigation platform built to identify suspicious messages, URLs, and phone numbers using indicators inspired by Indian scam patterns.**

[Live Demo](YOUR_LIVE_DEMO_URL) · [Report a Bug](YOUR_GITHUB_ISSUES_URL) · [Explore the Source Code](YOUR_GITHUB_REPOSITORY_URL)

---

## About the Project

ODDITY Cyber India is a digital threat investigation and scam-awareness platform designed to help users examine suspicious digital content before interacting with it.

In an environment where phishing messages, fraudulent links, impersonation attempts, and phone-based scams are increasingly common, identifying warning signs can make a significant difference.

ODDITY provides three independent analysis tools that examine submitted content against predefined detection rules, identify suspicious indicators, calculate risk scores, and present understandable explanations.

Rather than simply labelling something as safe or dangerous, ODDITY aims to help users understand **what doesn't fit and why.**

## Features

### 1. Message Analyzer
Examines suspicious messages and identifies indicators commonly associated with fraudulent communication.

- Detects suspicious credential and OTP requests.
- Identifies urgency and pressure-based language.
- Recognizes reward, prize, and lottery lures.
- Examines combinations of suspicious indicators.
- Generates a risk assessment with supporting evidence.

### 2. URL Analyzer
Examines URLs for structural irregularities and suspicious characteristics.

- URL validation and normalization.
- HTTPS and domain-structure checks.
- IP-address-based URL detection.
- Brand impersonation detection.
- Typosquatting detection.
- Suspicious brand references in URL paths.
- Encoded brand-path detection.
- Redirect and URL user-information checks.
- Risk assessment with explanatory indicators.

### 3. Phone Analyzer
Evaluates phone numbers using validation, normalization, and available reputation indicators.

- Phone number validation.
- Number normalization.
- Country and number-type identification.
- Reputation-based assessment.
- Risk scoring and supporting explanations.

## How It Works

ODDITY follows a frontend-backend architecture.

1. The user selects an analyzer and submits suspicious content.
2. The React frontend sends the input to the corresponding FastAPI endpoint.
3. The backend processes the input using its dedicated analysis engine.
4. Detection rules and available reputation indicators are evaluated.
5. The backend returns a structured analysis response.
6. The frontend presents the risk assessment and supporting evidence.

The analysis logic resides in the backend. The frontend is responsible for collecting input and presenting results.

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS |
| Build Tool | Vite |
| Backend | Python, FastAPI |
| API Validation | Pydantic |
| Phone Analysis | phonenumbers |
| API Communication | REST, JSON |
| UI Icons | Lucide React |

## Project Architecture

```text
ODDITY-CyberIndia/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── message_routes.py
│   │   │   ├── url_routes.py
│   │   │   └── phone_routes.py
│   │   │
│   │   ├── data/
│   │   │   ├── brands.py
│   │   │   └── phone_reputation.py
│   │   │
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── mappers/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   └── package.json
│
├── .gitignore
└── README.md
```

## Running Locally

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ODDITY-CyberIndia
```

### 2. Start the Backend

```bash
cd backend

python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend: `http://127.0.0.1:8000`

API documentation: `http://127.0.0.1:8000/docs`

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend

npm install
```

Create a `.env` file inside the frontend directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

```bash
npm run dev
```

Frontend: `http://localhost:5173`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend status |
| GET | `/health` | Health check |
| POST | `/api/v1/analyze/message` | Message analysis |
| POST | `/api/v1/analyze/url` | URL analysis |
| POST | `/api/v1/analyze/phone` | Phone analysis |

Interactive API documentation is available through FastAPI's Swagger UI at `/docs`.

## Project Scope and Limitations

ODDITY Cyber India is an educational investigation and scam-awareness project.

- Detection is based on predefined rules and available reputation data.
- It does not guarantee detection of every scam or malicious link.
- A low-risk result does not guarantee that submitted content is safe.
- Reputation data may be limited and may include demonstration or synthetic entries.
- The platform does not replace professional cybersecurity tools or independent verification.

**Always exercise caution before sharing personal information, OTPs, passwords, or financial details.**

## Project Status

Developed as a college project to explore practical applications of cybersecurity concepts, rule-based detection, API development, and frontend-backend integration.

The project is preserved as a completed academic implementation and demonstration.

## Acknowledgements

Built with curiosity, experimentation, and the goal of making digital threat awareness more accessible.

---

**ODDITY Cyber India — Find what doesn't fit.**