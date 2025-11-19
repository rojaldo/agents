from fastapi import APIRouter, HTTPException
from ..models import AgentRequest
from ..services.crewai_service import CrewAIService
from ..services.autogen_service import AutoGenService

router = APIRouter()
crewai_service = CrewAIService()
autogen_service = AutoGenService()

@router.post("/crewai/agent")
async def run_crewai_agent(request: AgentRequest):
    try:
        response = crewai_service.run_agent(request)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CrewAI Error: {str(e)}")

@router.post("/autogen/agent")
async def run_autogen_agent(request: AgentRequest):
    try:
        response = autogen_service.run_agent(request)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AutoGen Error: {str(e)}")
