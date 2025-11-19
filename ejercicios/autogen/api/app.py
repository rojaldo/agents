from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
from typing import Optional, List, Dict, Any

# Imports for CrewAI
from crewai import Agent, Task, Crew, Process, LLM

# Imports for AutoGen
import autogen

app = FastAPI(title="Agent API", description="API for CrewAI and AutoGen agents")

class AgentRequest(BaseModel):
    message: str
    humor_setting: int = Field(..., ge=0, le=10, description="Humor level from 0 (serious) to 10 (funny)")

def get_humor_instruction(level: int) -> str:
    """
    Generates a system instruction based on the humor level.
    """
    if level <= 2:
        return "You are extremely serious, formal, and professional. Do not use any humor. Be concise and factual."
    elif level <= 5:
        return "You are professional but approachable. You can be slightly casual but keep it business-like."
    elif level <= 8:
        return "You are friendly and witty. Feel free to use light humor and be conversational."
    else:
        return "You are a hilarious comedian. Be extremely funny, informal, and crack jokes in your response. Use emojis."

@app.post("/crewai/agent")
async def run_crewai_agent(request: AgentRequest):
    """
    Endpoint to run a CrewAI agent.
    """
    try:
        humor_instruction = get_humor_instruction(request.humor_setting)
        
        # Configure LLM for Ollama
        # Using the LLM class to specify the local Ollama instance
        my_llm = LLM(
            model="ollama/llama3.2:3b",
            base_url="http://localhost:11434"
        )
        
        # Define the agent
        agent = Agent(
            role='Assistant',
            goal='Respond to the user message appropriately based on the humor setting.',
            backstory=f"You are an AI assistant. {humor_instruction}",
            verbose=True,
            allow_delegation=False,
            llm=my_llm
        )

        task = Task(
            description=request.message,
            agent=agent,
            expected_output="A text response to the user's message."
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        return {"response": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CrewAI Error: {str(e)}")

@app.post("/autogen/agent")
async def run_autogen_agent(request: AgentRequest):
    """
    Endpoint to run an AutoGen agent.
    """
    try:
        humor_instruction = get_humor_instruction(request.humor_setting)
        
        # Configure AutoGen to use local Ollama
        config_list = [
            {
                "model": "llama3.2:3b",
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
            }
        ]
        
        llm_config = {
            "config_list": config_list,
            "temperature": 0.7,
        }

        assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config=llm_config,
            system_message=f"You are a helpful AI assistant. {humor_instruction}"
        )

        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0, # Stop after the assistant replies once
            code_execution_config=False,
        )

        # Initiate chat
        chat_res = user_proxy.initiate_chat(
            assistant,
            message=request.message,
            summary_method="last_msg"
        )
        
        # Retrieve the summary (last message)
        response_text = "No response"
        if hasattr(chat_res, 'summary'):
            response_text = chat_res.summary
        elif hasattr(chat_res, 'chat_history'):
             # Fallback for older versions or if summary is missing
             if chat_res.chat_history:
                 response_text = chat_res.chat_history[-1]['content']

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AutoGen Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
