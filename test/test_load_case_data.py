#!/usr/bin/env python3

"""
Unit tests for load_case_data.py.
"""

import pytest
import requests
import requests_mock
import pandas as pd
from redcap_eda.load_case_data import load_data

# Mock base URL
MOCK_URL = "https://raw.githubusercontent.com/redcap-tools/redcap-test-datasets/master/case-01/test-case-01-records.csv"


def test_load_valid_dataset():
    """Test that a valid dataset loads correctly."""
    with requests_mock.Mocker() as m:
        mock_csv = "record_id,gender,bmi\n1,Male,25.6\n2,Female,22.3"
        m.get(MOCK_URL, text=mock_csv)

        df = load_data("01", "records")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert df.shape == (2, 3)  # 2 rows, 3 columns
        assert list(df.columns) == ["record_id", "gender", "bmi"]


def test_invalid_dataset_name():
    """Test that an invalid dataset name raises a ValueError."""
    with pytest.raises(ValueError, match="Invalid dataset name"):
        load_data("01", "invalid_dataset")


def test_non_existent_case():
    """Test that trying to load a non-existent case returns an error."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://raw.githubusercontent.com/redcap-tools/redcap-test-datasets/master/case-99/test-case-99-records.csv",
            status_code=404,
        )
        with pytest.raises(RuntimeError, match="Failed to fetch records"):
            load_data("99", "records")


def test_network_failure():
    """Test that a network failure raises a RuntimeError."""
    with requests_mock.Mocker() as m:
        m.get(MOCK_URL, exc=requests.exceptions.ConnectionError)
        with pytest.raises(RuntimeError, match="Failed to fetch records"):
            load_data("01", "records")


def test_csv_parsing_error():
    """Test that a CSV parsing error raises a RuntimeError."""
    with requests_mock.Mocker() as m:
        m.get(MOCK_URL, text="invalid,csv,data\n,,")  # Bad CSV format
        with pytest.raises(RuntimeError, match="Failed to parse records"):
            load_data("01", "records")
