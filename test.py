import pytest
from src.main import parse_clean

@pytest.mark.parametrize("input_data,expected_count", [
    ([{"transaction_id": "TX1", "price": "€10.50"}], 1),
    ([{"transaction_id": "TX2", "price": "-5.00"}], 0), # Negative dropped
    ([{"transaction_id": "TX3", "price": "invalid"}], 0), # Bad cast dropped
    ([{"price": "10.00"}], 0), # Missing ID dropped
])

def test_parse_and_clean(input_data, expected_count):
    result = test_parse_clean(input_data)
    assert len(result) == expected_count


import pytest
import requests
from src.main import fetch_data

def test_fetch_data(requests_mock):
    mock_url = "https://api.eu-sales.com/v1/data"
    mock_response = [{"id": 1, "value": 100}]

    requests_mock.get(mock_url, json=mock_response, status_code=200)

    result = fetch_data(mock_url)
    assert result == mock_response

    