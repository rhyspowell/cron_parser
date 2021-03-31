import pytest

from cron_parser import __version__
from cron_parser.cron_parser import create_value_string, process_values, main, help


def test_version():
    assert __version__ == "0.1.0"


def test_help(capsys):
    help()
    out, err = capsys.readouterr()
    assert "Expected" in out
    assert err == ""


def test_main(capsys):
    with pytest.raises(SystemExit):
        main("")
    out, err = capsys.readouterr()
    assert "Expected" in out

    with pytest.raises(SystemExit):
        main("1-5 * * * * ")
    out, err = capsys.readouterr()
    assert "Expected" in out


@pytest.mark.parametrize(
    "value, n, expected_result", [("", "0", "0"), ("1", "2", "1 2")]
)
def test_create_value_string(value, n, expected_result):
    returned_value = create_value_string(value, n)
    assert expected_result == returned_value


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        (
            "*",
            "minutes",
            "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59",
        ),
        ("*/15", "minutes", "0 15 30 45"),
        ("0-5", "minutes", "0 1 2 3 4 5"),
        ("1", "minutes", "1"),
        (
            "0-61",
            "minutes",
            "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59",
        ),
        ("*/61", "minutes", "0"),
    ],
)
def test_good_process_values_minutes(requested_input, value_type, expected_result):
    returned_value = process_values(requested_input, value_type)
    assert expected_result == returned_value


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("?", "minutes", "invalid literal for int\(\) with base 10: '\?'"),
        ("-1", "minutes", "invalid literal for int\(\) with base 10: ''"),
    ],
)
def test_bad_process_values_minutes(requested_input, value_type, expected_result):
    with pytest.raises(SystemExit, match=r"" + expected_result):
        process_values(requested_input, value_type)


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("*", "hours", "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23"),
        ("*/15", "hours", "0 15"),
        ("0-5", "hours", "0 1 2 3 4 5"),
        ("1", "hours", "1"),
        (
            "0-61",
            "hours",
            "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23",
        ),
        ("*/61", "hours", "0"),
    ],
)
def test_good_process_values_hours(requested_input, value_type, expected_result):
    returned_value = process_values(requested_input, value_type)
    assert expected_result == returned_value


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("?", "hours", "invalid literal for int\(\) with base 10: '\?'"),
        ("-1", "hours", "invalid literal for int\(\) with base 10: ''"),
    ],
)
def test_bad_process_values_hours(requested_input, value_type, expected_result):
    with pytest.raises(SystemExit, match=r"" + expected_result):
        process_values(requested_input, value_type)


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        (
            "*",
            "day of month",
            "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
        ),
        ("*/15", "day of month", "1 16 31"),
        ("1-5", "day of month", "1 2 3 4 5"),
        ("1", "day of month", "1"),
        (
            "1-61",
            "day of month",
            "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
        ),
        ("*/61", "day of month", "1"),
    ],
)
def test_good_process_values_dom(requested_input, value_type, expected_result):
    returned_value = process_values(requested_input, value_type)
    assert expected_result == returned_value


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("?", "day of month", "invalid literal for int\(\) with base 10: '\?'"),
        ("-1", "day of month", "invalid literal for int\(\) with base 10: ''"),
        ("0", "day of month", "Input does not match patterns"),
    ],
)
def test_bad_process_values_dom(requested_input, value_type, expected_result):
    with pytest.raises(SystemExit, match=r"" + expected_result):
        process_values(requested_input, value_type)


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("*", "month", "1 2 3 4 5 6 7 8 9 10 11 12"),
        ("*/6", "month", "1 7"),
        ("0/6", "month", "1 7"),
        ("1-5", "month", "1 2 3 4 5"),
        ("0-5", "month", "1 2 3 4 5"),
        ("1", "month", "1"),
        ("1-61", "month", "1 2 3 4 5 6 7 8 9 10 11 12"),
        ("*/61", "month", "1"),
    ],
)
def test_good_process_values_month(requested_input, value_type, expected_result):
    returned_value = process_values(requested_input, value_type)
    assert expected_result == returned_value


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("?", "month", "invalid literal for int\(\) with base 10: '\?'"),
        ("-1", "month", "invalid literal for int\(\) with base 10: ''"),
        ("0", "month", "Input does not match patterns"),
    ],
)
def test_bad_process_values_month(requested_input, value_type, expected_result):
    with pytest.raises(SystemExit, match=r"" + expected_result):
        process_values(requested_input, value_type)


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("*", "day of week", "0 1 2 3 4 5 6"),
        ("*/15", "day of week", "0"),
        ("0-5", "day of week", "0 1 2 3 4 5"),
        ("1", "day of week", "1"),
        ("0-61", "day of week", "0 1 2 3 4 5 6"),
        ("*/61", "day of week", "0"),
    ],
)
def test_good_process_values_dow(requested_input, value_type, expected_result):
    returned_value = process_values(requested_input, value_type)
    assert expected_result == returned_value


@pytest.mark.parametrize(
    "requested_input, value_type, expected_result",
    [
        ("?", "day of week", "invalid literal for int\(\) with base 10: '\?'"),
        ("-1", "day of week", "invalid literal for int\(\) with base 10: ''"),
    ],
)
def test_bad_process_values_dow(requested_input, value_type, expected_result):
    with pytest.raises(SystemExit, match=r"" + expected_result):
        process_values(requested_input, value_type)
