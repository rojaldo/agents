"""
Tools for CrewAI agents
Provides data processing, analysis, and API functionality
"""

import os
import sys
from crewai.tools import tool

# Add parent directory to path to import tools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import DataDownloader, DataProcessor, DataAnalyzer, APIClient


# ========================
# DATA DOWNLOADER TOOLS
# ========================

@tool
def download_csv_file(url: str, filepath: str) -> str:
    """Download a CSV file from a URL and save it locally"""
    return DataDownloader.download_csv(url, filepath)


@tool
def download_json_file(url: str, filepath: str) -> str:
    """Download a JSON file from a URL and save it locally"""
    return DataDownloader.download_json(url, filepath)


# ========================
# DATA PROCESSOR TOOLS
# ========================

@tool
def load_csv_file(filepath: str) -> str:
    """Load a CSV file and display its structure and information"""
    return DataProcessor.load_csv(filepath)


@tool
def clean_data_file(filepath: str, output_filepath: str) -> str:
    """Clean data by removing duplicates and handling missing values"""
    return DataProcessor.clean_data(filepath, output_filepath)


@tool
def filter_data_file(filepath: str, column: str, value: str, output_filepath: str) -> str:
    """Filter data by a specific column value"""
    return DataProcessor.filter_data(filepath, column, value, output_filepath)


# ========================
# DATA ANALYZER TOOLS
# ========================

@tool
def calculate_statistics_file(filepath: str) -> str:
    """Calculate descriptive statistics for all numeric columns"""
    return DataAnalyzer.calculate_statistics(filepath)


@tool
def analyze_column_file(filepath: str, column: str) -> str:
    """Analyze a specific column in detail"""
    return DataAnalyzer.analyze_column(filepath, column)


@tool
def correlation_analysis_file(filepath: str) -> str:
    """Calculate correlation matrix for numeric columns"""
    return DataAnalyzer.correlation_analysis(filepath)


# ========================
# API CLIENT TOOLS
# ========================

@tool
def make_api_request(url: str, params: dict = None) -> str:
    """Make a GET request to an API and return the JSON response"""
    return APIClient.get_request(url, params)


@tool
def fetch_and_save_api(url: str, filepath: str, params: dict = None) -> str:
    """Fetch data from an API and save the response to a file"""
    return APIClient.save_api_response(url, filepath, params)
