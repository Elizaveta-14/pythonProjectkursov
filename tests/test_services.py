from src.services import get_profitable_cashback_categories


def test_get_profitable_cashback_categories(operations_list_valid, result_cashback_categories):
    result = get_profitable_cashback_categories(operations_list_valid, "2022", "04")

    assert result == result_cashback_categories


def test_get_profitable_cashback_categories_invalid_date(operations_list_valid):
    result = get_profitable_cashback_categories(operations_list_valid, "2026", "04")

    assert result == "{}"


def test_get_profitable_cashback_categories_invalid_date_2(operations_list_valid):
    result = get_profitable_cashback_categories(operations_list_valid, "2022", "111")

    assert result == "{}"


def test_get_profitable_cashback_categories_invalid_data(operations_list_valid):
    result = get_profitable_cashback_categories([], "2022", "111")

    assert result == "{}"
