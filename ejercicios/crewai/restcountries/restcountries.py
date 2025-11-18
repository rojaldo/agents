"""
RestCountries API Analysis using CrewAI
A multi-agent system for querying and analyzing country data from the RestCountries API
Uses Mistral LLM via Ollama
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import CrewAI tools
from crew_tools import (
    fetch_and_save_api,
    load_csv_file,
    analyze_column_file,
    calculate_statistics_file
)

# Initialize Ollama LLM with configuration from .env
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

# Define the data directory and URLs from .env
DATA_DIR = os.path.join(os.path.dirname(__file__), os.getenv("RESTCOUNTRIES_DATA_DIR", "data"))
RESTCOUNTRIES_URL = os.getenv("RESTCOUNTRIES_URL", "https://restcountries.com/v2/all")
RAW_DATA = os.path.join(DATA_DIR, 'countries_raw.json')
CSV_DATA = os.path.join(DATA_DIR, 'countries.csv')

# Create data directory
os.makedirs(DATA_DIR, exist_ok=True)

# Define Agents with Ollama Mistral
api_developer = Agent(
    role="API Developer",
    goal="Fetch and validate data from the RestCountries API",
    backstory="""You are an experienced API developer with expertise in RESTful APIs and JSON data.
    Your role is to fetch country data and ensure the data integrity from the API response.""",
    tools=[fetch_and_save_api],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

data_processor = Agent(
    role="Data Processor",
    goal="Process and clean the countries JSON data for analysis",
    backstory="""You are a skilled data processor specialized in transforming API responses into
    analyzable formats. You understand JSON structures and can extract relevant information.""",
    tools=[load_csv_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

data_analyst = Agent(
    role="Data Analyst",
    goal="Perform statistical analysis on countries data",
    backstory="""You are an experienced data analyst specializing in demographic and geographic data.
    You provide insights through statistical analysis and identify patterns in country data.""",
    tools=[analyze_column_file, calculate_statistics_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Tasks
task_fetch = Task(
    description=f"""Fetch all countries data from the RestCountries API v2:
    - Use the URL: {RESTCOUNTRIES_URL}
    - Save the complete JSON response to: {RAW_DATA}
    - Verify that the API call was successful and data was saved""",
    expected_output="Confirmation of successful API fetch with number of countries retrieved",
    agent=api_developer
)

task_process = Task(
    description=f"""Process the countries JSON data from {RAW_DATA}:
    1. Extract key fields: name, population, area, region, subregion, capital
    2. Convert the JSON data to CSV format
    3. Save the processed data to: {CSV_DATA}
    4. Report on the number of countries processed and fields extracted""",
    expected_output="Processed countries data in CSV format with details about extracted fields",
    agent=data_processor,
    depends_on=[task_fetch]
)

task_regional_analysis = Task(
    description=f"""Analyze the regional distribution of countries from {CSV_DATA}:
    - Identify unique regions
    - Count countries per region
    - Report the distribution

    Provide insights about regional diversity in the dataset.""",
    expected_output="Summary of countries by region with distribution analysis",
    agent=data_processor,
    depends_on=[task_process]
)

task_population = Task(
    description=f"""Analyze population statistics from {CSV_DATA}:
    - Calculate mean, median, min, and max population by region
    - Identify regions with largest and smallest populations
    - Provide statistical insights about global population distribution""",
    expected_output="Population statistics grouped by region with analysis",
    agent=data_analyst,
    depends_on=[task_process]
)

task_area = Task(
    description=f"""Analyze area statistics from {CSV_DATA}:
    - Calculate mean, median, min, and max area by region
    - Identify largest and smallest countries by area
    - Provide insights about geographic distribution""",
    expected_output="Area statistics grouped by region with geographic insights",
    agent=data_analyst,
    depends_on=[task_process]
)

task_density = Task(
    description=f"""Calculate and analyze population density from {CSV_DATA}:
    - Compute population density for each country (population/area)
    - Identify the most and least densely populated countries
    - Provide analysis of population concentration patterns
    - Report top 10 most densely populated countries""",
    expected_output="Population density analysis with ranking of countries",
    agent=data_analyst,
    depends_on=[task_process]
)

# Create and run the Crew
crew = Crew(
    agents=[api_developer, data_processor, data_analyst],
    tasks=[
        task_fetch,
        task_process,
        task_regional_analysis,
        task_population,
        task_area,
        task_density
    ],
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("RESTCOUNTRIES API ANALYSIS - CREWAI MULTI-AGENT SYSTEM WITH MISTRAL")
    print("=" * 80 + "\n")

    result = crew.kickoff()

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nFinal Report:")
    print(result)
