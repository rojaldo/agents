"""
RestCountries API Analysis Exercise
Crew that queries the RestCountries API and analyzes country data
"""

import asyncio
import os
import json
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.task import Task
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Load environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

# Configuration
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

API_BASE_URL = os.getenv("RESTCOUNTRIES_API_BASE", "https://restcountries.com/v3.1")

# LLM Configuration
LLM_CONFIG = {
    "model": os.getenv("LLM_MODEL", "mistral"),
    "base_url": os.getenv("LLM_BASE_URL", "http://localhost:8000/v1"),
    "api_key": os.getenv("LLM_API_KEY", "ollama"),
}


# Tools for API consumption and data processing
def query_countries_api(endpoint: str = "all", output_file: str = None) -> dict:
    """Query the RestCountries API."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)

        if isinstance(data, list):
            return {
                "status": "success",
                "message": f"Retrieved data from API endpoint: {endpoint}",
                "record_count": len(data),
                "sample": data[0] if data else None,
                "saved_to": output_file
            }
        else:
            return {
                "status": "success",
                "message": f"Retrieved data from API endpoint: {endpoint}",
                "data": data,
                "saved_to": output_file
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to query API: {str(e)}"
        }


def process_json_data(input_file: str, output_file: str) -> dict:
    """Process and clean JSON data from API responses."""
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Convert to DataFrame for better processing
        if isinstance(data, list):
            records = []
            for country in data:
                record = {
                    "name": country.get("name", {}).get("common", ""),
                    "official_name": country.get("name", {}).get("official", ""),
                    "region": country.get("region", ""),
                    "subregion": country.get("subregion", ""),
                    "population": country.get("population", 0),
                    "area": country.get("area", 0),
                    "capital": country.get("capital", [""])[0] if country.get("capital") else "",
                    "languages": list(country.get("languages", {}).values()) if country.get("languages") else [],
                    "currencies": list(country.get("currencies", {}).keys()) if country.get("currencies") else [],
                    "timezones_count": len(country.get("timezones", [])),
                }
                records.append(record)

            df = pd.DataFrame(records)
            df.to_csv(output_file, index=False)

            return {
                "status": "success",
                "message": f"Processed {len(records)} countries",
                "output_file": output_file,
                "columns": list(df.columns),
                "shape": {"rows": len(df), "columns": df.shape[1]}
            }
        else:
            return {
                "status": "error",
                "message": "Expected list of countries in JSON data"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process JSON data: {str(e)}"
        }


def analyze_countries_data(file_path: str) -> dict:
    """Perform statistical analysis on country data."""
    try:
        df = pd.read_csv(file_path)

        # Basic statistics
        analysis = {
            "status": "success",
            "total_countries": len(df),
            "regions": df['region'].value_counts().to_dict(),
            "population_stats": {
                "total": int(df['population'].sum()),
                "average": float(df['population'].mean()),
                "min": int(df['population'].min()),
                "max": int(df['population'].max()),
                "median": float(df['population'].median()),
            },
            "area_stats": {
                "total": float(df['area'].sum()),
                "average": float(df['area'].mean()),
                "min": float(df['area'].min()),
                "max": float(df['area'].max()),
                "median": float(df['area'].median()),
            },
            "largest_countries_by_population": df.nlargest(5, 'population')[['name', 'population']].to_dict('records'),
            "smallest_countries_by_population": df.nsmallest(5, 'population')[['name', 'population']].to_dict('records'),
            "most_common_languages": df['languages'].explode().value_counts().head(10).to_dict(),
            "countries_by_region": {}
        }

        # Detailed analysis by region
        for region in df['region'].unique():
            region_data = df[df['region'] == region]
            analysis["countries_by_region"][region] = {
                "count": len(region_data),
                "population": int(region_data['population'].sum()),
                "avg_population": float(region_data['population'].mean()),
            }

        return analysis

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to analyze data: {str(e)}"
        }


async def main():
    """Main function to run the RestCountries analysis crew."""

    # Initialize the LLM client
    client = OpenAIChatCompletionClient(
        model=LLM_CONFIG["model"],
        base_url=LLM_CONFIG["base_url"],
        api_key=LLM_CONFIG["api_key"],
    )

    # Create agents
    api_developer = AssistantAgent(
        name="APIDeveloper",
        description="Queries APIs and retrieves data",
        model_client=client,
        tools=[query_countries_api],
    )

    data_processor = AssistantAgent(
        name="DataProcessor",
        description="Processes and cleans JSON data",
        model_client=client,
        tools=[process_json_data],
    )

    data_analyst = AssistantAgent(
        name="DataAnalyst",
        description="Performs statistical analysis on datasets",
        model_client=client,
        tools=[analyze_countries_data],
    )

    # Create the crew task
    task = Task(
        description=f"""
        Analyze country data from the RestCountries API:
        1. Query the RestCountries API to get all countries data
        2. Process and clean the JSON data
        3. Perform statistical analysis on the countries

        Save processed data in {DATA_DIR}
        """,
        agents=[api_developer, data_processor, data_analyst],
    )

    # Create the team and run
    team = RoundRobinGroupChat([api_developer, data_processor, data_analyst])

    print("Starting RestCountries API Analysis...")
    print("-" * 50)

    result = await team.run(
        task=task,
        max_turns=10,
    )

    print("-" * 50)
    print("Analysis Complete!")
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
