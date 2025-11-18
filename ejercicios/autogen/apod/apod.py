"""
APOD (Astronomy Picture of the Day) API Analysis Exercise
Crew that queries NASA's APOD API and analyzes images
"""

import asyncio
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np
from PIL import Image
from io import BytesIO
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

API_BASE_URL = "https://api.nasa.gov/planetary/apod"
NASA_API_KEY = os.getenv("NASA_API_KEY", "demo")

# LLM Configuration
LLM_CONFIG = {
    "model": os.getenv("LLM_MODEL", "mistral"),
    "base_url": os.getenv("LLM_BASE_URL", "http://localhost:8000/v1"),
    "api_key": os.getenv("LLM_API_KEY", "ollama"),
}


# Tools for API consumption and image processing
def query_apod_api(days: int = 5, output_file: str = None) -> dict:
    """Query NASA's APOD API for recent pictures of the day."""
    try:
        apod_data = []

        # Get last N days of APOD data
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            params = {
                "api_key": NASA_API_KEY,
                "date": date,
                "hd": "False"  # Use standard quality to avoid timeout
            }

            response = requests.get(API_BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if "error" not in data:
                apod_data.append(data)

        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(apod_data, f, indent=2)

        return {
            "status": "success",
            "message": f"Retrieved {len(apod_data)} APOD entries",
            "entries": len(apod_data),
            "saved_to": output_file,
            "sample": apod_data[0] if apod_data else None
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to query APOD API: {str(e)}"
        }


def download_images(input_file: str, output_dir: str, max_images: int = 5) -> dict:
    """Download and process APOD images."""
    try:
        with open(input_file, 'r') as f:
            apod_data = json.load(f)

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        downloaded_images = []
        failed_downloads = []

        for idx, entry in enumerate(apod_data[:max_images]):
            if "url" not in entry or entry.get("media_type") != "image":
                continue

            try:
                url = entry["url"]
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # Save image
                filename = f"apod_{entry['date']}.jpg"
                filepath = Path(output_dir) / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)

                image = Image.open(BytesIO(response.content))
                downloaded_images.append({
                    "date": entry["date"],
                    "title": entry.get("title", ""),
                    "filename": filename,
                    "size": len(response.content),
                    "image_dimensions": image.size
                })

            except Exception as e:
                failed_downloads.append({
                    "date": entry.get("date"),
                    "error": str(e)
                })

        return {
            "status": "success",
            "message": f"Downloaded {len(downloaded_images)} images",
            "downloaded": len(downloaded_images),
            "failed": len(failed_downloads),
            "output_dir": output_dir,
            "images": downloaded_images
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to download images: {str(e)}"
        }


def process_apod_metadata(input_file: str, output_file: str) -> dict:
    """Process and clean APOD metadata from API responses."""
    try:
        with open(input_file, 'r') as f:
            apod_data = json.load(f)

        # Extract and process metadata
        records = []
        for entry in apod_data:
            record = {
                "date": entry.get("date", ""),
                "title": entry.get("title", ""),
                "explanation_length": len(entry.get("explanation", "")),
                "media_type": entry.get("media_type", ""),
                "has_image": entry.get("media_type") == "image",
                "has_video": entry.get("media_type") == "video",
                "url": entry.get("url", ""),
                "copyright": entry.get("copyright", "Unknown"),
            }
            records.append(record)

        df = pd.DataFrame(records)
        df.to_csv(output_file, index=False)

        return {
            "status": "success",
            "message": f"Processed {len(records)} APOD entries",
            "output_file": output_file,
            "shape": {"rows": len(df), "columns": df.shape[1]},
            "media_breakdown": {
                "images": int(df['has_image'].sum()),
                "videos": int(df['has_video'].sum())
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process metadata: {str(e)}"
        }


def analyze_images(image_dir: str, metadata_file: str) -> dict:
    """Analyze images and their properties."""
    try:
        image_files = list(Path(image_dir).glob("*.jpg"))

        analysis = {
            "status": "success",
            "total_images": len(image_files),
            "images_analysis": []
        }

        for img_file in image_files:
            try:
                image = Image.open(img_file)
                arr = np.array(image.convert('RGB'))

                img_analysis = {
                    "filename": img_file.name,
                    "size_bytes": img_file.stat().st_size,
                    "dimensions": {"width": image.width, "height": image.height},
                    "pixel_count": image.width * image.height,
                    "format": image.format,
                    "mode": image.mode,
                    "average_brightness": float(arr.mean()),
                    "color_variance": {
                        "red": float(arr[:,:,0].var()),
                        "green": float(arr[:,:,1].var()),
                        "blue": float(arr[:,:,2].var()),
                    }
                }
                analysis["images_analysis"].append(img_analysis)

            except Exception as e:
                analysis["images_analysis"].append({
                    "filename": img_file.name,
                    "error": str(e)
                })

        # Summary statistics
        if analysis["images_analysis"]:
            valid_images = [i for i in analysis["images_analysis"] if "error" not in i]
            if valid_images:
                analysis["summary"] = {
                    "avg_file_size": float(np.mean([i["size_bytes"] for i in valid_images])),
                    "total_pixels": sum(i["pixel_count"] for i in valid_images),
                    "avg_dimensions": {
                        "width": float(np.mean([i["dimensions"]["width"] for i in valid_images])),
                        "height": float(np.mean([i["dimensions"]["height"] for i in valid_images]))
                    }
                }

        return analysis

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to analyze images: {str(e)}"
        }


async def main():
    """Main function to run the APOD analysis crew."""

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
        tools=[query_apod_api],
    )

    image_processor = AssistantAgent(
        name="ImageProcessor",
        description="Downloads and processes images",
        model_client=client,
        tools=[download_images, process_apod_metadata],
    )

    image_analyst = AssistantAgent(
        name="ImageAnalyst",
        description="Analyzes image properties and metadata",
        model_client=client,
        tools=[analyze_images],
    )

    # Create the crew task
    task = Task(
        description=f"""
        Analyze NASA's Astronomy Picture of the Day (APOD):
        1. Query the APOD API to get recent pictures
        2. Download and process the images
        3. Analyze image properties and metadata

        Save data and images in {DATA_DIR}
        Note: Using 'demo' API key for basic access
        """,
        agents=[api_developer, image_processor, image_analyst],
    )

    # Create the team and run
    team = RoundRobinGroupChat([api_developer, image_processor, image_analyst])

    print("Starting APOD Analysis...")
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
