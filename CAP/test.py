here are the codes many of these codes and functions were new to me
so these are the three layers (cold, helped and code=needed diract code)

import pytest cold 

def test_add():
    assert add(2, 3) == 5


import pytest cold

def test_get_total():
    assert get_total([{"amount": 10}, {"amount": 5}]) == 15


import pytest cold 

def test_get_total():
    assert get_total([]) == 0


import pytest code

def test_completed_orders():
    orders = [
        {"id": 1, "status": "completed"},
        {"id": 2, "status": "pending"},
        {"id": 3, "status": "completed"},
    ]

    result = get_completed(orders)

    assert result == [
        {"id": 1, "status": "completed"},
        {"id": 3, "status": "completed"},
    ]


pytest -v test_main.py helped
pytest -v -k "test_completed_orders"


import pytest code

@pytest.mark.parametrize(
    "orders, expected",
    [
        ([], 0),
        ([{"amount": 10}, {"amount": 5}], 15),
        ([{"amount": 25}], 25),
    ],
)
def test_get_total(orders, expected):
    assert get_total(orders) == expected


import pytest code 

    def test_div():
        with pytest.raise(ZeroDivisionError):
            divide(1, 0)


import pytest code cause first time using match

def test_div_msg():
    with pytest.raises(ZeroDivisionError, match="division"):
        divide(1, 0)


import pytest code 

@pytest.fixture 
def sample_orders():
    return [
        {"id": 1, "status": "completed"},
        {"id": 2, "status": "pending"},
        {"id": 3, "status": "completed"},
    ]

def test_get_completed(sample_orders):
    result = get_completed(sample_orders)

    assert result == [
        {"id": 1, "status": "completed"},
        {"id": 3, "status": "completed"},
    ]


def test_write_report(path): code 
    report_file = path / "report.txt"
    content = "DMS"

    write_report(report_file, content)

    assert report_file.read_text(encoding="utf-8") == content 


from unittest.mock import patch code 

def test_fetch_prices():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"close": 190}

        result = fetch_prices("AAPL")

    assert result == {"close": 190}
    mock_get.assert_called_once()


import pytest code

def test_get_db_url_set_and_missing(monkeypatch):
    expected_url = "postgresql://localhost:5432/app"
    monkeypatch.setenv("DB_URL", expected_url)

    assert get_db_url() == expected_url

    monkeypatch.delenv("DB_URL", raising=False)

    with pytest.raise(KeyError):
        get_db_url()


from unittest.mock import patch code 
from requests.exceptions import Timeout

def test_fetch_prices_timeout_returns_none():
    with patch("requests.get", side_effect=Timeout("request timed out")):
        result = fetch_prices("AAPL")

    assert result in None 


import pytest code 

@pytest.fixture
def temp_resource():
    resource = {"connected": True}
    yield resource
    resource["connected"] = False 


here are the qs 

Why mock external APIs in unit tests, and what is the difference between a unit test and an integration test?

mock test happen within code and logic and unite tests happens in the conncection and integration part of the piplein

What three kinds of cases would you test for validate_records, and why?

valid data and invalid data and edge cases like nuls and empty records 