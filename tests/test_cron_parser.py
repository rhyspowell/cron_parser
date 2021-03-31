import pytest

from cron_parser import __version__
from cron_parser.cron_parser import create_value_string, process_values, main, help


def test_version():
    assert __version__ == '0.1.0'

def test_help(capsys):
    help()
    out, err = capsys.readouterr()
    assert "Expected" in out
    assert err == ''

def test_main(capsys):
    with pytest.raises(SystemExit):
        main('')
    out, err = capsys.readouterr()
    assert "Expected" in out

@pytest.mark.parametrize("value, n, expected_result", [
    ("", "0", "0"),
    ("1", "2", "1 2")
])
def test_create_value_string(value, n, expected_result):
    returned_value = create_value_string(value, n)
    assert expected_result == returned_value

@pytest.mark.parametrize("requested_input, value_type, expected_result", [
    ("*", "minutes", "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59"),
    ("*/15", "minutes", "0 15 30 45"),
    ("0-5", "minutes", "0 1 2 3 4 5"),
    ("1", "minutes", "1")
])
def test_process_values(requested_input, value_type, expected_result):
    returned_value = process_values(requested_input, value_type)
    assert expected_result == returned_value

def test_minute_spaced():
    pass

def test_minutes_multi_specific():
    pass


