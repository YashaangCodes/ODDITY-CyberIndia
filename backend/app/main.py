from app.api.message_routes import router as message_router
from app.api.url_routes import router as url_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ScamShield India API",
    description="Backend API for digital threat risk assessment",
    version="0.1.0",
)

# Allow the React frontend to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router)
app.include_router(url_router)

@app.get("/")
def home() -> dict[str, str]:
    return {
        "project": "ScamShield India",
        "message": "Backend API is running successfully",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
    }