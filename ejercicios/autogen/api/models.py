from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    message: str
    humor_setting: int = Field(..., ge=0, le=10, description="Humor level from 0 (serious) to 10 (funny)")
