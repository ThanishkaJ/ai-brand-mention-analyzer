
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.analysis import router as analysis_router


app = FastAPI(
    title="Brand Context Analyzer",
    description=(
        "Detect brand mentions, extract context and analyze "
        "sentiment in AI-generated answers."
    ),
    version="1.0.0"
)


# Register API routers
app.include_router(analysis_router)


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# Serve the frontend
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)
