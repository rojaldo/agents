"""
Generic tools for CrewAI exercises
Reusable tools for data downloading, processing, and analysis
"""

import os
import requests
import pandas as pd
import json
from typing import Any, Dict, List
from pathlib import Path


class DataDownloader:
    """Tool for downloading data from URLs"""

    @staticmethod
    def download_csv(url: str, filepath: str) -> str:
        """Download CSV file from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(response.text)
            return f"Successfully downloaded CSV to {filepath}"
        except Exception as e:
            return f"Error downloading file: {str(e)}"

    @staticmethod
    def download_json(url: str, filepath: str) -> str:
        """Download JSON from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(response.json(), f, indent=2)
            return f"Successfully downloaded JSON to {filepath}"
        except Exception as e:
            return f"Error downloading JSON: {str(e)}"


class DataProcessor:
    """Tool for processing and cleaning data"""

    @staticmethod
    def load_csv(filepath: str) -> str:
        """Load and display info about CSV file"""
        try:
            df = pd.read_csv(filepath)
            info = f"CSV loaded successfully\n"
            info += f"Shape: {df.shape}\n"
            info += f"Columns: {list(df.columns)}\n"
            info += f"Data types:\n{df.dtypes}\n"
            info += f"Missing values:\n{df.isnull().sum()}"
            return info
        except Exception as e:
            return f"Error loading CSV: {str(e)}"

    @staticmethod
    def clean_data(filepath: str, output_filepath: str) -> str:
        """Clean data: remove duplicates and handle missing values"""
        try:
            df = pd.read_csv(filepath)
            initial_rows = len(df)

            # Remove duplicates
            df = df.drop_duplicates()

            # Fill missing values with appropriate defaults
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    df[col].fillna('Unknown', inplace=True)

            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            df.to_csv(output_filepath, index=False)

            removed_rows = initial_rows - len(df)
            return f"Data cleaned successfully\nRows removed: {removed_rows}\nCleaned data saved to {output_filepath}"
        except Exception as e:
            return f"Error cleaning data: {str(e)}"

    @staticmethod
    def filter_data(filepath: str, column: str, value: Any, output_filepath: str) -> str:
        """Filter data by column value"""
        try:
            df = pd.read_csv(filepath)
            filtered_df = df[df[column] == value]

            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            filtered_df.to_csv(output_filepath, index=False)

            return f"Filtered {len(filtered_df)} rows where {column} == {value}\nFiltered data saved to {output_filepath}"
        except Exception as e:
            return f"Error filtering data: {str(e)}"


class DataAnalyzer:
    """Tool for analyzing data with pandas"""

    @staticmethod
    def calculate_statistics(filepath: str) -> str:
        """Calculate descriptive statistics"""
        try:
            df = pd.read_csv(filepath)

            analysis = "Descriptive Statistics:\n"
            analysis += str(df.describe())

            return analysis
        except Exception as e:
            return f"Error calculating statistics: {str(e)}"

    @staticmethod
    def analyze_column(filepath: str, column: str) -> str:
        """Analyze a specific column"""
        try:
            df = pd.read_csv(filepath)

            if column not in df.columns:
                return f"Column '{column}' not found"

            analysis = f"Analysis of column '{column}':\n"
            analysis += f"Data type: {df[column].dtype}\n"
            analysis += f"Non-null count: {df[column].notna().sum()}\n"
            analysis += f"Null count: {df[column].isna().sum()}\n"

            if df[column].dtype in ['float64', 'int64']:
                analysis += f"Mean: {df[column].mean():.2f}\n"
                analysis += f"Std: {df[column].std():.2f}\n"
                analysis += f"Min: {df[column].min()}\n"
                analysis += f"Max: {df[column].max()}\n"

            analysis += f"Unique values: {df[column].nunique()}"

            return analysis
        except Exception as e:
            return f"Error analyzing column: {str(e)}"

    @staticmethod
    def correlation_analysis(filepath: str) -> str:
        """Calculate correlation between numeric columns"""
        try:
            df = pd.read_csv(filepath)
            numeric_df = df.select_dtypes(include=['float64', 'int64'])

            if numeric_df.empty:
                return "No numeric columns found"

            corr = numeric_df.corr()
            return f"Correlation Matrix:\n{corr}"
        except Exception as e:
            return f"Error calculating correlation: {str(e)}"


class APIClient:
    """Tool for making API requests"""

    @staticmethod
    def get_request(url: str, params: Dict = None) -> str:
        """Make GET request to API"""
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except Exception as e:
            return f"Error making API request: {str(e)}"

    @staticmethod
    def save_api_response(url: str, filepath: str, params: Dict = None) -> str:
        """Make API request and save response"""
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(response.json(), f, indent=2)

            return f"API response saved to {filepath}"
        except Exception as e:
            return f"Error saving API response: {str(e)}"
