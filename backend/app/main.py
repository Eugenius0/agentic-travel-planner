from fastapi import FastAPI

app = FastAPI(
    title="Agentic Travel Planner API",
    description="AI-powered travel planning using LangGraph and MCP",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
