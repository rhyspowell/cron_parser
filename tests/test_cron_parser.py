import pytest

from cron_parser import __version__, process_values


def test_version():
    assert __version__ == '0.1.0'

@pytest.mark.parametrize("when, expected_result", [
    ("*", list(range(0,60))),
    ("*/15", "0, 15, 30, 45"),
    ("0,15,30,45", "0, 15, 30, 45"),
    ("0-5", "0, 1, 2, 3, 4, 5"),
    ("32", "32")
])
def test_minute_all(when, expected_result):
    pass

def test_minute_specific():
    pass

def test_minute_spaced():
    pass

def test_minutes_multi_specific():
    pass


