"""
redcap_eda - A Python CLI for REDCap Exploratory Data Analysis (EDA)
====================================================================

**redcap_eda** is a command-line tool designed to assist with
exploratory data analysis (EDA) of REDCap datasets.

Main Features
-------------
- Load REDCap case data.
- Perform basic summary statistics and data validation.
- Generate visualizations for quick insights.
- Log analysis details for reproducibility.

Modules
-------
- `cli`            - Command-line interface for interacting with REDCap-EDA.
- `load_case_data` - Functions for loading REDCap datasets.
- `analysis`       - Statistical and exploratory data analysis functions.
- `visualization`  - Tools for generating plots and visual summaries.
- `logger`         - Logging utilities for tracking analysis steps.
"""

# Import all submodules for direct access
from redcap_eda import cli, load_case_data, analysis, visualization, logger

# Define what is accessible via "from redcap_eda import *"
__all__ = ["cli", "load_case_data", "analysis", "visualization", "logger"]
