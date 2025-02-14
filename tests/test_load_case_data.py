#!/usr/bin/env python3

"""
Unit tests for load_case_data.py.
"""

import pytest
import requests
import requests_mock
from redcap_eda.load_case_data import load_data

# Mock base URL
MOCK_URL = "https://raw.githubusercontent.com/redcap-tools/redcap-test-datasets/master/case-01/test-case-01-records.csv"

"""
@pytest.mark.usefixtures("requests_mock")
def test_load_valid_dataset(requests_mock):
    #Test that a valid dataset loads correctly.
    mock_csv = "record_id,gender,bmi\n1,Male,25.6\n2,Female,22.3"

    # Ensure the URL matches exactly to intercept the request
    requests_mock.get(MOCK_URL, text=mock_csv)

    df = load_data("01", "records")

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape == (2, 3)  # 2 rows, 3 columns
    assert list(df.columns) == ["record_id", "gender", "bmi"]
"""


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


"""
@pytest.mark.usefixtures("requests_mock")
def test_csv_parsing_error(requests_mock):
    #Test that a CSV parsing error raises a RuntimeError.
    malformed_csv = "invalid,csv,data\n,,\n"  # More malformed data

    requests_mock.get(MOCK_URL, text=malformed_csv)

    with pytest.raises(RuntimeError, match="Failed to parse records"):
        load_data("01", "records")
"""
