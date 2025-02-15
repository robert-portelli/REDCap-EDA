#!/usr/bin/env python3

import pandas as pd
import requests
from redcap_eda.logger import logger

"""
Dynamically load REDCap test datasets from GitHub for any given test case.
"""

# Base URL for raw GitHub files
BASE_URL = "https://raw.githubusercontent.com/redcap-tools/redcap-test-datasets/master/"

# Dataset file patterns
DATASETS = {
    "records": "test-case-{case}-records.csv",
    "records_api": "test-case-{case}-records-api.csv",
    "records_api_eav": "test-case-{case}-records-api-eav.csv",
    "data_dictionary": "test-case-{case}-data-dictionary.csv",
    "project_info": "test-case-{case}-project-information.csv",
}


def load_data(case="01", dataset_name="records_api"):
    """
    Load a dataset from the REDCap test dataset repository for a specific case.

    Args:
        case (str): The test case number (e.g., "01", "07", "20").
        dataset_name (str): The dataset to load. Must be one of:
                            ['records', 'records_api', 'records_api_eav', 'data_dictionary', 'project_info'].

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the dataset.

    Raises:
        ValueError: If the dataset name is invalid.
        RuntimeError: If the dataset fails to download or parse.
    """
    if dataset_name not in DATASETS:
        error_msg = f"❌ Invalid dataset name: {dataset_name}. Choose from {list(DATASETS.keys())}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if case != "01":
        error_msg = "❌ Case number given: {case} \nThis package currently only supports test case data '01'"
        logger.error(error_msg)
        raise ValueError(error_msg)

    url = BASE_URL + f"case-{case}/" + DATASETS[dataset_name].format(case=case)
    logger.info(f"🔄 Fetching dataset: {dataset_name} from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure HTTP errors are raised

        df = pd.read_csv(url)
        logger.info(f"✅ Successfully loaded {dataset_name} for Case {case}")
        return df

    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Failed to fetch {dataset_name} for Case {case}: {e}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg)

    except pd.errors.ParserError as e:
        error_msg = f"❌ Failed to parse {dataset_name} for Case {case}: {e}"
        logger.error(error_msg, exc_info=True)
        raise RuntimeError(error_msg)
