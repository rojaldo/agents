from crewai import Agent, Task, Crew, Process, LLM
from ..models import AgentRequest
from .common import get_humor_instruction

class CrewAIService:
    def run_agent(self, request: AgentRequest) -> str:
        humor_instruction = get_humor_instruction(request.humor_setting)
        
        # Configure LLM for Ollama
        my_llm = LLM(
            model="ollama/llama3.2:3b",
            base_url="http://localhost:11434"
        )
        
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
        return str(result)
