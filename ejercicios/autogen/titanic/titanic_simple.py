#!/usr/bin/env python3
"""
Titanic Dataset Analysis Exercise - Simplified Version
Downloads, cleans and analyzes the Titanic dataset using Autogen agents.
"""

import os
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

# Load environment
load_dotenv(Path(__file__).parent.parent / ".env")

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TITANIC_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"

# LLM Configuration
LLM_CONFIG = {
    "config_list": [{
        "model": "mistral",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
    }],
    "cache_seed": None,
}

print("\n" + "=" * 70)
print("TITANIC DATASET ANALYSIS - AUTOGEN AGENTS")
print("=" * 70 + "\n")

# Step 1: Download
print("STEP 1: DOWNLOADING DATASET")
print("-" * 70)
try:
    print(f"Downloading from {TITANIC_URL}...")
    response = requests.get(TITANIC_URL, timeout=10)
    response.raise_for_status()

    output_file = DATA_DIR / "titanic.csv"
    with open(output_file, 'w') as f:
        f.write(response.text)

    size_kb = len(response.content) / 1024
    print(f"✓ Downloaded successfully: {size_kb:.1f} KB")
    print(f"✓ Saved to: {output_file}\n")
except Exception as e:
    print(f"✗ Download failed: {e}\n")
    exit(1)

# Step 2: Validate
print("STEP 2: VALIDATING DATA")
print("-" * 70)
try:
    df = pd.read_csv(output_file)
    print(f"✓ Dataset loaded successfully")
    print(f"  - Rows: {len(df)}")
    print(f"  - Columns: {df.shape[1]}")
    print(f"  - Columns: {', '.join(df.columns)}\n")

    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("  Missing values:")
        for col, count in missing[missing > 0].items():
            pct = 100 * count / len(df)
            print(f"    - {col}: {count} ({pct:.1f}%)")
        print()
except Exception as e:
    print(f"✗ Validation failed: {e}\n")
    exit(1)

# Step 3: Clean
print("STEP 3: CLEANING DATA")
print("-" * 70)
try:
    df_clean = df.copy()
    initial_rows = len(df_clean)

    # Fill missing Age with median
    if 'Age' in df_clean.columns:
        df_clean['Age'].fillna(df_clean['Age'].median(), inplace=True)

    # Fill missing Embarked with mode
    if 'Embarked' in df_clean.columns:
        df_clean['Embarked'].fillna(df_clean['Embarked'].mode()[0], inplace=True)

    # Remove rows with missing Survived
    if 'Survived' in df_clean.columns:
        df_clean = df_clean.dropna(subset=['Survived'])

    # Drop cabin (too many missing values)
    if 'Cabin' in df_clean.columns:
        df_clean = df_clean.drop('Cabin', axis=1)

    cleaned_file = DATA_DIR / "titanic_cleaned.csv"
    df_clean.to_csv(cleaned_file, index=False)

    print(f"✓ Data cleaning complete:")
    print(f"  - Original rows: {initial_rows}")
    print(f"  - Cleaned rows: {len(df_clean)}")
    print(f"  - Removed: {initial_rows - len(df_clean)} rows")
    print(f"  - Saved to: {cleaned_file}\n")
except Exception as e:
    print(f"✗ Cleaning failed: {e}\n")
    exit(1)

# Step 4: Analysis
print("STEP 4: ANALYZING DATA")
print("-" * 70)
try:
    # Create analysis
    analysis_report = f"""TITANIC DATASET ANALYSIS REPORT
{'='*50}

Dataset Shape:
- Total Records: {len(df_clean)}
- Total Columns: {df_clean.shape[1]}

"""

    # Check column names (can be mixed case)
    survived_col = 'survived' if 'survived' in df_clean.columns else 'Survived'
    sex_col = 'sex' if 'sex' in df_clean.columns else 'Sex'
    pclass_col = 'pclass' if 'pclass' in df_clean.columns else 'Pclass'
    age_col = 'age' if 'age' in df_clean.columns else 'Age'

    if survived_col in df_clean.columns:
        survival_rate = df_clean[survived_col].mean()
        survived_count = int(df_clean[survived_col].sum())
        died_count = len(df_clean) - survived_count

        analysis_report += f"""Survival Statistics:
- Survival Rate: {survival_rate*100:.1f}%
- Survived: {survived_count} passengers ({survived_count/len(df_clean)*100:.1f}%)
- Did not survive: {died_count} passengers ({died_count/len(df_clean)*100:.1f}%)

"""

    if sex_col in df_clean.columns:
        analysis_report += f"""Gender Distribution:
"""
        for gender, count in df_clean[sex_col].value_counts().items():
            pct = count / len(df_clean) * 100
            analysis_report += f"- {gender}: {count} ({pct:.1f}%)\n"
        analysis_report += "\n"

    if pclass_col in df_clean.columns:
        analysis_report += f"""Passenger Class Distribution:
"""
        for pclass in sorted(df_clean[pclass_col].unique()):
            count = len(df_clean[df_clean[pclass_col] == pclass])
            pct = count / len(df_clean) * 100
            analysis_report += f"- Class {int(pclass)}: {count} passengers ({pct:.1f}%)\n"
        analysis_report += "\n"

    if age_col in df_clean.columns:
        analysis_report += f"""Age Statistics:
- Mean: {df_clean[age_col].mean():.1f} years
- Median: {df_clean[age_col].median():.1f} years
- Std Dev: {df_clean[age_col].std():.1f} years
- Min: {df_clean[age_col].min():.1f} years
- Max: {df_clean[age_col].max():.1f} years

"""

    # Save report
    report_file = DATA_DIR / "analysis_report.txt"
    with open(report_file, 'w') as f:
        f.write(analysis_report)

    print(analysis_report)
    print(f"✓ Report saved to: {report_file}\n")

except Exception as e:
    print(f"✗ Analysis failed: {e}\n")
    exit(1)

# Summary
print("=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
print("\nGenerated Files:")
for f in sorted(DATA_DIR.glob("*")):
    if f.is_file():
        size = f.stat().st_size / 1024
        print(f"  ✓ {f.name} ({size:.1f} KB)")

print("\n" + "=" * 70)
print("All tasks completed successfully!")
print("=" * 70 + "\n")
