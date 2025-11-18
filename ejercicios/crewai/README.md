# CrewAI Exercises

A collection of CrewAI exercises demonstrating multi-agent systems for data analysis tasks. Each exercise showcases how multiple AI agents can collaborate to complete complex workflows.

## Project Structure

```
crewai/
├── tools.py              # Generic, reusable tools across all exercises
├── titanic/              # Titanic dataset analysis exercise
│   ├── titanic.py       # Main script
│   └── data/            # Data directory
├── restcountries/        # REST Countries API analysis exercise
│   ├── restcountries.py # Main script
│   └── data/            # Data directory
├── apod/                 # NASA APOD API analysis exercise
│   ├── apod.py          # Main script
│   └── data/            # Data directory
└── README.md            # This file
```

## Requirements

```
crewai
pandas
requests
```

Install dependencies:
```bash
pip install crewai pandas requests
```

## Exercises

### 1. Titanic Dataset Analysis

**Objective:** Download, clean, and analyze the famous Titanic passenger dataset.

**Agents:**
- **Data Engineer**: Downloads and validates the dataset
- **Data Analyst**: Cleans the data and performs initial analysis
- **Statistician**: Performs comprehensive statistical analysis

**Tools:**
- Dataset download from URL
- Data loading and validation
- Data cleaning (duplicates, missing values)
- Statistical analysis and correlation

**Run:**
```bash
python titanic/titanic.py
```

**Expected Outputs:**
- `titanic/data/titanic_raw.csv` - Downloaded dataset
- `titanic/data/titanic_cleaned.csv` - Cleaned dataset
- Console output with analysis results

---

### 2. RestCountries API Analysis

**Objective:** Query the RestCountries API and analyze global demographic and geographic data.

**Agents:**
- **API Developer**: Fetches data from the RestCountries API
- **Data Processor**: Processes JSON data and converts to CSV format
- **Data Analyst**: Performs statistical analysis on countries data

**Tools:**
- REST API requests and response handling
- JSON data processing
- Data transformation and CSV export
- Statistical analysis by region

**Run:**
```bash
python restcountries/restcountries.py
```

**Expected Outputs:**
- `restcountries/data/countries_raw.json` - Raw API response
- `restcountries/data/countries.csv` - Processed countries data
- Console output with statistical analysis
  - Population statistics by region
  - Area statistics by region
  - Population density analysis
  - Regional distribution summary

---

### 3. APOD (Astronomy Picture of the Day) Analysis

**Objective:** Fetch and analyze data from NASA's APOD API.

**Agents:**
- **API Developer**: Fetches data from NASA APOD API
- **Image Processor**: Extracts and processes image metadata
- **Image Analyst**: Performs content analysis and generates reports

**Tools:**
- NASA APOD API requests
- Metadata extraction
- Content analysis (text length, media types)
- Report generation

**Run:**
```bash
python apod/apod.py
```

**Expected Outputs:**
- `apod/data/apod_data.json` - Raw APOD data (30 days)
- `apod/data/apod_metadata.csv` - Processed metadata
- Console output with analysis:
  - Media type distribution (images vs videos)
  - Content characteristics
  - Comprehensive analysis report

---

## Generic Tools Module

The `tools.py` file provides reusable tools that can be used across multiple exercises:

### DataDownloader
- `download_csv(url, filepath)` - Download CSV files from URL
- `download_json(url, filepath)` - Download JSON files from URL

### DataProcessor
- `load_csv(filepath)` - Load and display CSV information
- `clean_data(filepath, output_filepath)` - Clean data (remove duplicates, handle missing values)
- `filter_data(filepath, column, value, output_filepath)` - Filter data by column value

### DataAnalyzer
- `calculate_statistics(filepath)` - Calculate descriptive statistics
- `analyze_column(filepath, column)` - Analyze specific column
- `correlation_analysis(filepath)` - Calculate correlations between columns

### APIClient
- `get_request(url, params)` - Make GET request to API
- `save_api_response(url, filepath, params)` - Save API response to file

---

## CrewAI Concepts

Each exercise demonstrates key CrewAI concepts:

1. **Agents**: AI entities with specific roles and goals
2. **Tools**: Functions that agents can use to perform tasks
3. **Tasks**: Work items assigned to agents
4. **Crew**: Orchestrates multiple agents to complete complex workflows
5. **Dependencies**: Tasks can depend on other tasks being completed first

---

## Customization

### Adding New Tools

Add new tools to `tools.py` following the same structure:

```python
class NewToolName:
    @staticmethod
    def tool_method(param1, param2):
        """Tool description"""
        # Implementation
        return result
```

Then import and use in your exercise script:

```python
from tools import NewToolName

@tool
def my_tool():
    """Tool wrapper for CrewAI"""
    return NewToolName.tool_method(param1, param2)
```

### Modifying Agents

Edit the agent definitions in each exercise script to change:
- Role and goal
- Available tools
- Backstory and expertise

### Adjusting Tasks

Modify task descriptions and expected outputs to customize the workflow.

---

## Notes

- All exercises use local LLMs (Mistral) as specified in requirements
- API keys are not required for demo access (except APOD uses DEMO_KEY)
- Data is stored in exercise-specific `data/` directories
- Tools are designed to be generic and reusable across projects

---

## License

These exercises are for educational purposes.
