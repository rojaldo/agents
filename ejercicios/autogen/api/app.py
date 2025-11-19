from fastapi import FastAPI
from .controllers.agent_controller import router as agent_router

app = FastAPI(title="Agent API", description="API for CrewAI and AutoGen agents")

app.include_router(agent_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
