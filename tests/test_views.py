import pytest

from src.views import get_card_info, get_top_transactions, greetings, sort_by_date


@pytest.mark.parametrize(
    "input_time, expected_greet",
    [
        ("15:30:00", "Добрый день!"),
        ("00:30:00", "Доброй ночи!"),
        ("23:59:59", "Добрый вечер!"),
        ("04:30:03", "Доброе утро!"),
    ],
)
def test_greetings_valid(input_time, expected_greet):
    result = greetings(input_time)

    assert result == expected_greet


@pytest.mark.parametrize(
    "invalid_time, expected_error",
    [
        ("", "Неверный формат времени"),
        ("5", "Неверный формат времени"),
        ("какое-то время", "Неверный формат времени"),
        ("17.03.00", "Неверный формат времени"),
        ("17-03-00", "Неверный формат времени"),
    ],
)
def test_greetings_invalid(invalid_time, expected_error):
    with pytest.raises(ValueError):
        assert greetings(invalid_time) == expected_error


def test_sort_by_date(operations_list_valid, list_sorted_by_date):
    result = sort_by_date(operations_list_valid, "05.04.2022")

    assert result == list_sorted_by_date


@pytest.mark.parametrize("invalid_date", ["", "04-04-2022", "04.04.22"])
def test_sort_by_date_error_date(operations_list_valid, invalid_date):
    result = sort_by_date(operations_list_valid, invalid_date)

    assert result == []


def test_get_card_info(operations_list_valid, card_info_result):
    result = get_card_info(operations_list_valid)

    assert result == card_info_result


def test_get_card_info_empty_list():
    result = get_card_info([])

    assert result == []


def test_get_card_info_invalid_list(operations_list_invalid):
    result = get_card_info(operations_list_invalid)

    assert result == []


def test_get_top_transactions(operations_list_valid, top_5_operations):
    result = get_top_transactions(operations_list_valid)

    assert result == top_5_operations


def test_get_top_transaction_invalid_list(operations_list_invalid):
    result = get_top_transactions(operations_list_invalid)

    assert result == []
