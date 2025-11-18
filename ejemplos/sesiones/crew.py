from crewai import Agent, Task, Crew

dev_agent = Agent(
    role="Experto en Python",
    goal="Ayudar con programación Python",
    backstory="Desarrollador con 10 años de experiencia",
    llm="ollama/llama3.2:3b",  # Modelo local con Ollama,
    base_url="http://localhost:11434",
)

task = Task(
    description="¿Cómo creo una función en Python?",
    expected_output="Una explicación clara de cómo crear funciones en Python",
    agent=dev_agent
)

crew = Crew(
    agents=[dev_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)