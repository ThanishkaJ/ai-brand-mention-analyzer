
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.analysis import router as analysis_router



app = FastAPI(
    title="Brand Context Analyzer",
    description=(
        "Detect brand mentions, extract context and analyze "
        "sentiment in AI-generated answers."
    ),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(analysis_router)


@app.get("/")
async def root():
    return {
        "message": "Brand Context Analyzer API is running!"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }
