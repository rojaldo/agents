"""
Titanic Dataset Analysis Exercise
Crew that downloads, cleans and analyzes the Titanic dataset
"""

import os
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

# Configuration
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TITANIC_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"

# LLM Configuration
LLM_CONFIG = {
    "config_list": [
        {
            "model": "mistral",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ],
    "cache_seed": None,
}


# Tools for data engineering
def download_dataset(url: str, output_path: str) -> str:
    """Download dataset from URL and save to file."""
    try:
        print(f"[DOWNLOAD] Fetching from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(response.text)

        size_kb = len(response.content) / 1024
        result = f"✓ Downloaded {size_kb:.1f} KB to {output_path}"
        print(f"[DOWNLOAD] {result}")
        return result
    except Exception as e:
        error = f"✗ Error: {str(e)}"
        print(f"[DOWNLOAD] {error}")
        return error


def validate_data(file_path: str) -> str:
    """Load and validate the dataset."""
    try:
        print(f"[VALIDATE] Checking {file_path}...")
        df = pd.read_csv(file_path)
        missing = df.isnull().sum()

        report = f"""✓ Validation Report:
  Rows: {len(df)}, Columns: {df.shape[1]}
  Missing values: {missing.sum()} total"""

        print(f"[VALIDATE] {report}")
        return report
    except Exception as e:
        error = f"✗ Error: {str(e)}"
        print(f"[VALIDATE] {error}")
        return error


def clean_data(file_path: str, output_path: str) -> str:
    """Clean the dataset by handling missing values."""
    try:
        print(f"[CLEAN] Processing {file_path}...")
        df = pd.read_csv(file_path)
        initial_rows = len(df)

        # Data cleaning
        if 'Age' in df.columns:
            df['Age'].fillna(df['Age'].median(), inplace=True)
        if 'Embarked' in df.columns:
            df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

        df.to_csv(output_path, index=False)

        result = f"✓ Cleaned {initial_rows} rows → {len(df)} rows saved to {output_path}"
        print(f"[CLEAN] {result}")
        return result
    except Exception as e:
        error = f"✗ Error: {str(e)}"
        print(f"[CLEAN] {error}")
        return error


def analyze_dataset(file_path: str) -> str:
    """Analyze the dataset with descriptive statistics."""
    try:
        print(f"[ANALYZE] Analyzing {file_path}...")
        df = pd.read_csv(file_path)

        analysis = f"""✓ TITANIC ANALYSIS:
  Shape: {len(df)} rows × {df.shape[1]} cols"""

        if 'Survived' in df.columns:
            survival = df['Survived'].mean()
            analysis += f"\n  Survival rate: {survival*100:.1f}%"

        if 'Sex' in df.columns:
            analysis += f"\n  Genders: {df['Sex'].nunique()}"

        if 'Age' in df.columns:
            analysis += f"\n  Age range: {df['Age'].min():.0f}-{df['Age'].max():.0f} years"

        print(f"[ANALYZE] {analysis}")
        return analysis
    except Exception as e:
        error = f"✗ Error: {str(e)}"
        print(f"[ANALYZE] {error}")
        return error


def main():
    """Main function to run the Titanic analysis."""

    print("\n" + "=" * 60)
    print("TITANIC DATASET ANALYSIS WITH AUTOGEN")
    print("=" * 60 + "\n")

    # Create agents with proper configuration
    data_engineer = AssistantAgent(
        name="DataEngineer",
        system_message="""You are a Data Engineer. Download and validate datasets.
        When asked, use download_dataset() and validate_data() functions.
        Report results concisely.""",
        llm_config=LLM_CONFIG,
    )

    data_cleaner = AssistantAgent(
        name="DataCleaner",
        system_message="""You are a Data Cleaner. Clean datasets and handle missing values.
        When asked, use clean_data() function.
        Report results concisely.""",
        llm_config=LLM_CONFIG,
    )

    analyst = AssistantAgent(
        name="DataAnalyst",
        system_message="""You are a Data Analyst. Analyze datasets and provide statistics.
        When asked, use analyze_dataset() function.
        Provide detailed insights.""",
        llm_config=LLM_CONFIG,
    )

    # Create user proxy
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=15,
        code_execution_config={"use_docker": False},
    )

    # Register functions for all agents
    for agent in [data_engineer, data_cleaner, analyst]:
        agent.register_for_llm(
            description="Download a dataset from a URL",
        )(download_dataset)
        agent.register_for_llm(
            description="Validate a CSV dataset",
        )(validate_data)
        agent.register_for_llm(
            description="Clean a CSV dataset",
        )(clean_data)
        agent.register_for_llm(
            description="Analyze a CSV dataset",
        )(analyze_dataset)

    # Task message
    task_msg = f"""Complete the Titanic dataset analysis:

1. Download from: {TITANIC_URL}
   Save to: {DATA_DIR}/titanic.csv

2. Validate the data

3. Clean it and save to: {DATA_DIR}/titanic_cleaned.csv

4. Analyze and report findings

Each agent should use their specialized functions."""

    print("Starting workflow...\n")

    # Run the conversation
    try:
        user_proxy.initiate_chat(
            data_engineer,
            message=task_msg,
            max_turns=25,
        )
    except Exception as e:
        print(f"Error during execution: {e}")

    print("\n" + "=" * 60)
    print("ANALYSIS WORKFLOW COMPLETE")
    print("=" * 60)

    # Show generated files
    print("\nGenerated Files:")
    for f in sorted(DATA_DIR.glob("*.csv")):
        size = f.stat().st_size / 1024
        print(f"  ✓ {f.name} ({size:.1f} KB)")


if __name__ == "__main__":
    main()
