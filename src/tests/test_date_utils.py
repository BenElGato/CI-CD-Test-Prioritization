import pytest
from src.targets.date_utils import DateUtils
from datetime import datetime

du = DateUtils()

def test_current_date():
    d = du.current_date()
    assert isinstance(d, datetime.date)

def test_add_subtract_days():
    assert du.add_days("2025-01-01", 5).isoformat() == "2025-01-06"
    assert du.subtract_days("2025-01-10", 3).isoformat() == "2025-01-07"

def test_days_between():
    assert du.days_between("2025-01-01", "2025-01-10") == 9
    assert du.days_between("2025-01-10", "2025-01-01") == 9

def test_is_weekend():
    assert du.is_weekend("2025-01-05")
    assert du.is_weekend("2025-01-04")

def test_next_weekday():
    assert du.next_weekday("2025-01-01", 0).isoformat() == "2025-01-06"

def test_is_leap_year():
    assert du.is_leap_year(2020)
    assert not du.is_leap_year(2019)
def test_leap_year_edge_case():
    assert not du.is_leap_year(1900)
