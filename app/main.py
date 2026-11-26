from fastapi import FastAPI

app = FastAPI(
    title="Brand Context Analyzer",
    description="Detect brand mentions, extract context and analyze sentiment in AI-generated answers.",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Brand Context Analyzer API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}