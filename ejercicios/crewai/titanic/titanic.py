"""
Titanic Dataset Analysis using CrewAI
A multi-agent system for downloading, cleaning, and analyzing the Titanic dataset
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
    download_csv_file,
    load_csv_file,
    clean_data_file,
    analyze_column_file,
    calculate_statistics_file,
    correlation_analysis_file
)

# Initialize Ollama LLM with configuration from .env
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

# Define the data directory and URLs from .env
DATA_DIR = os.path.join(os.path.dirname(__file__), os.getenv("TITANIC_DATA_DIR", "data"))
TITANIC_URL = os.getenv("TITANIC_URL", "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
RAW_DATA = os.path.join(DATA_DIR, 'titanic_raw.csv')
CLEANED_DATA = os.path.join(DATA_DIR, 'titanic_cleaned.csv')

# Create data directory
os.makedirs(DATA_DIR, exist_ok=True)

# Define Agents with Ollama Mistral
data_engineer = Agent(
    role="Data Engineer",
    goal="Download and validate the Titanic dataset to ensure data quality",
    backstory="""You are an expert data engineer with 10 years of experience in data acquisition
    and validation. Your job is to ensure that data is properly downloaded and its structure is verified.""",
    tools=[download_csv_file, load_csv_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

data_analyst = Agent(
    role="Data Analyst",
    goal="Clean and analyze the Titanic dataset to prepare it for statistical analysis",
    backstory="""You are a skilled data analyst specialized in data cleaning and preparation.
    You understand the importance of handling missing values and duplicates properly.""",
    tools=[clean_data_file, analyze_column_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

statistician = Agent(
    role="Statistician",
    goal="Perform comprehensive statistical analysis on the Titanic dataset",
    backstory="""You are a PhD statistician with expertise in descriptive and exploratory data analysis.
    You provide deep insights through statistical methods and correlation analysis.""",
    tools=[calculate_statistics_file, correlation_analysis_file],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define Tasks
task_download = Task(
    description=f"""Download the Titanic dataset from the URL: {TITANIC_URL}
    Save it to: {RAW_DATA}
    Then validate that the file was downloaded successfully.""",
    expected_output="Confirmation that the Titanic dataset was successfully downloaded and basic file info",
    agent=data_engineer
)

task_validate = Task(
    description=f"""Load the Titanic dataset from {RAW_DATA} and provide detailed information about:
    - Number of rows and columns
    - Column names and data types
    - Missing values count
    - Basic dataset structure""",
    expected_output="Detailed structure and information about the Titanic dataset",
    agent=data_engineer,
    depends_on=[task_download]
)

task_clean = Task(
    description=f"""Clean the Titanic dataset by:
    1. Removing duplicate rows
    2. Handling missing values (fill numeric columns with mean, categorical with 'Unknown')
    3. Save the cleaned data to: {CLEANED_DATA}

    Report on the cleaning operations performed.""",
    expected_output="Summary of cleaning operations and confirmation that cleaned data was saved",
    agent=data_analyst,
    depends_on=[task_validate]
)

task_survival_analysis = Task(
    description=f"""Analyze the 'Survived' column from {CLEANED_DATA} to understand:
    - Distribution of survival (0 = died, 1 = survived)
    - Survival rate percentage
    - Statistical properties""",
    expected_output="Detailed analysis of passenger survival rates",
    agent=data_analyst,
    depends_on=[task_clean]
)

task_age_analysis = Task(
    description=f"""Analyze the 'Age' column from {CLEANED_DATA} to understand:
    - Age distribution of passengers
    - Mean, median, standard deviation
    - Min and max ages
    - Number of unique ages""",
    expected_output="Comprehensive analysis of passenger age distribution",
    agent=data_analyst,
    depends_on=[task_clean]
)

task_statistics = Task(
    description=f"""Calculate descriptive statistics for {CLEANED_DATA}:
    - Mean, median, std deviation for all numeric columns
    - Min and max values
    - Quartiles (25%, 50%, 75%)

    Provide a comprehensive statistical summary.""",
    expected_output="Complete descriptive statistics table for all numeric columns",
    agent=statistician,
    depends_on=[task_clean]
)

task_correlation = Task(
    description=f"""Analyze correlations in {CLEANED_DATA}:
    - Calculate correlation matrix for numeric columns
    - Identify strongest positive and negative correlations
    - Discuss relationships between variables

    Focus on correlations with survival outcome.""",
    expected_output="Correlation matrix and analysis of key relationships in the data",
    agent=statistician,
    depends_on=[task_clean]
)

# Create and run the Crew
crew = Crew(
    agents=[data_engineer, data_analyst, statistician],
    tasks=[
        task_download,
        task_validate,
        task_clean,
        task_survival_analysis,
        task_age_analysis,
        task_statistics,
        task_correlation
    ],
    verbose=True
)

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TITANIC DATASET ANALYSIS - CREWAI MULTI-AGENT SYSTEM WITH MISTRAL")
    print("=" * 80 + "\n")

    result = crew.kickoff()

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nFinal Report:")
    print(result)
