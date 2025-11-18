"""
APOD (Astronomy Picture of the Day) Analysis using CrewAI
A multi-agent system for fetching and analyzing NASA APOD data
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
    make_api_request,
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
DATA_DIR = os.path.join(os.path.dirname(__file__), os.getenv("APOD_DATA_DIR", "data"))

# NASA APOD API endpoint
APOD_API_KEY = os.getenv("APOD_API_KEY", "DEMO_KEY")
APOD_BASE_URL = os.getenv("APOD_BASE_URL", "https://api.nasa.gov/planetary/apod")

APOD_DATA = os.path.join(DATA_DIR, 'apod_data.json')
APOD_METADATA = os.path.join(DATA_DIR, 'apod_metadata.csv')

# Create data directory
os.makedirs(DATA_DIR, exist_ok=True)

# Define Agents with Ollama Mistral
api_developer = Agent(
    role="API Developer",
    goal="Fetch APOD data from NASA API and ensure data quality",
    backstory="""You are an experienced developer specializing in NASA APIs and astronomical data.
    Your expertise ensures we retrieve accurate and complete data from the APOD API.""",
    tools=[make_api_request, fetch_and_save_api],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

image_processor = Agent(
    role="Image Processor",
    goal="Process and extract metadata from APOD images",
    backstory="""You are a specialist in image metadata processing and content analysis.
    You understand how to extract meaningful information from image API responses.""",
    tools=[load_csv_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

image_analyst = Agent(
    role="Image Analyst",
    goal="Perform comprehensive analysis on APOD data and generate insights",
    backstory="""You are a data scientist specializing in astronomical data and visual content analysis.
    You provide deep insights through statistical analysis of image collections.""",
    tools=[analyze_column_file, calculate_statistics_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Tasks
task_fetch = Task(
    description=f"""Fetch Astronomy Picture of the Day (APOD) data from NASA API:
    - Use the base URL: {APOD_BASE_URL}
    - Use API key: {APOD_API_KEY}
    - Fetch the last 10 days of APOD data
    - Save all responses to: {APOD_DATA}
    - Verify successful data retrieval""",
    expected_output="Confirmation of successful API fetches with list of dates retrieved",
    agent=api_developer
)

task_process = Task(
    description=f"""Process the APOD data from {APOD_DATA}:
    1. Extract metadata: date, title, media_type, explanation length, copyright
    2. Create a structured metadata file
    3. Save processed metadata to: {APOD_METADATA}
    4. Report on number of records processed and fields extracted""",
    expected_output="Processed APOD metadata in CSV format with data quality report",
    agent=image_processor,
    depends_on=[task_fetch]
)

task_media_analysis = Task(
    description=f"""Analyze the media types in APOD data from {APOD_METADATA}:
    - Identify unique media types (image, video, etc.)
    - Calculate percentage distribution of each type
    - Provide insights about the content composition
    - Report on media type diversity""",
    expected_output="Media type distribution analysis with percentages and insights",
    agent=image_processor,
    depends_on=[task_process]
)

task_content_analysis = Task(
    description=f"""Analyze content characteristics from {APOD_METADATA}:
    - Calculate statistics on explanation text length
    - Analyze copyright information distribution
    - Identify patterns in description length
    - Provide insights about content richness""",
    expected_output="Content characteristics analysis with statistics on explanations and copyright",
    agent=image_analyst,
    depends_on=[task_process]
)

task_temporal_analysis = Task(
    description=f"""Analyze temporal patterns from {APOD_METADATA}:
    - Examine the date range of fetched images
    - Analyze the consistency of daily releases
    - Provide insights about APOD publication patterns
    - Calculate statistics about content timing""",
    expected_output="Temporal analysis showing date patterns and publication consistency",
    agent=image_analyst,
    depends_on=[task_process]
)

task_comprehensive_report = Task(
    description=f"""Generate a comprehensive report analyzing all APOD data from {APOD_METADATA}:
    1. Summarize key statistics (total images, date range, content types)
    2. Highlight media type composition
    3. Discuss explanation text characteristics
    4. Analyze copyright patterns
    5. Provide overall insights about the APOD collection
    6. Make recommendations based on findings""",
    expected_output="Comprehensive APOD analysis report with findings and recommendations",
    agent=image_analyst,
    depends_on=[task_media_analysis, task_content_analysis, task_temporal_analysis]
)

# Create and run the Crew
crew = Crew(
    agents=[api_developer, image_processor, image_analyst],
    tasks=[
        task_fetch,
        task_process,
        task_media_analysis,
        task_content_analysis,
        task_temporal_analysis,
        task_comprehensive_report
    ],
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("APOD (ASTRONOMY PICTURE OF THE DAY) ANALYSIS - CREWAI MULTI-AGENT SYSTEM WITH MISTRAL")
    print("=" * 80 + "\n")

    result = crew.kickoff()

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nFinal Report:")
    print(result)
