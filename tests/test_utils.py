from unittest.mock import patch
import pytest
from src.utils import (reading_xlsx , get_transactions, get_mask_account, get_convert_amount, analyze_transactions,
                       hello_person)

import pandas as pd

@patch("json.loads")
def test_get_transactions(mock_get):
    """Проверяет на возвращение списка"""
    mock_get.return_value = ""
    assert get_transactions(mock_get) == ""


def test_get_transactions_file_not_found():
    """Тестирует обработку ошибки отсутствующего файла."""
    result = get_transactions("non_existent.json")
    assert result == [], "Функция должна возвращать пустой список, если файл отсутствует"


@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_no_found(mock_file):
    """Проверяет на возвращение пустого списка при ошибке"""
    transactions = get_transactions("data/operations.json")
    assert transactions == []


def test_get_mask_account_valid():
    """Тестирует корректную маскировку номера карты"""
    assert get_mask_account(1234567890123456) == "1234 ** 3456", "Ошибка в маскировании номера карты"


def test_get_mask_account_short_number():
    """Тестирует поведение при слишком коротком номере карты"""
    assert get_mask_account(12345) == "Ошибка: Неверный номер карты", "Ошибка при обработке короткого номера"


def test_get_mask_account_edge_case():
    """Тестирует граничный случай (ровно 6 цифр)"""
    assert get_mask_account(123456) == "1234 ** 3456", "Ошибка при обработке 6-значного номера"


def test_get_mask_account_large_number():
    """Тестирует длинный номер карты"""
    assert get_mask_account(9876543210987654321) == "9876 ** 4321", "Ошибка при обработке длинного номера"


@patch("json.loads")
def test_get_convert_amount(mock_get):
    """Проверяет статус коде 200"""
    mock_get.return_value.status_code = 200
    assert get_convert_amount != 0


@pytest.fixture
def sample_xlsx_file(tmp_path):
    """Создает временный XLSX-файл для тестирования."""
    data = {
        "Дата операции": ["01.01.2024", "15.01.2024"],
        "Номер карты": ["1234", "5678"],
        "Статус": ["Успешно", "Отмена"],
        "Сумма операции": [1000.5, 500.0],
        "Валюта операции": ["RUB", "USD"],
        "Сумма платежа": [1000.5, 500.0],
        "Валюта платежа": ["RUB", "USD"],
        "Категория": ["Продукты", "Развлечения"],
        "Описание": ["Покупка в магазине", "Кинотеатр"]
    }

    df = pd.DataFrame(data)
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    return file_path


def test_reading_xlsx_valid_file(sample_xlsx_file):
    """Тест чтения корректного файла."""
    df = reading_xlsx(str(sample_xlsx_file))

    assert not df.empty, "Датафрейм не должен быть пустым"
    assert list(df.columns) == ["Дата операции", "Номер карты", "Статус", "Сумма операции",
                                "Валюта операции", "Сумма платежа", "Валюта платежа",
                                "Категория", "Описание"], "Колонки не совпадают"
    assert df["Дата операции"].dtype == "datetime64[ns]", "Дата должна быть в формате datetime"


def test_reading_xlsx_file_not_found():
    """Тест обработки отсутствующего файла."""
    df = reading_xlsx("non_existent_file.xlsx")
    assert df.empty, "Функция должна возвращать пустой DataFrame при отсутствии файла"


def test_analyze_transactions():
    """Тестирует расчет расходов, кэшбэка и топ-5 транзакций"""
    data = {
        "Дата операции": ["01.01.2024", "02.01.2024", "03.01.2024", "04.01.2024", "05.01.2024", "06.01.2024"],
        "Сумма платежа": [500, 1500, 3000, 1200, 7000, 2500]
    }
    df = pd.DataFrame(data)

    result = analyze_transactions(df)

    assert result["total_spent"] == 15700, "Неверная общая сумма расходов"
    assert result["cashback"] == 157, "Неверный кэшбэк"

    top_5_expected = [7000, 3000, 2500, 1500, 1200]
    top_5_actual = result["top_5_transactions"]["Сумма платежа"].tolist()

    assert top_5_actual == top_5_expected, "Топ-5 транзакций определены неверно"


def test_analyze_transactions_empty():
    """Тестирует поведение с пустым DataFrame"""
    df = pd.DataFrame(columns=["Дата операции", "Сумма платежа"])

    result = analyze_transactions(df)

    assert result["total_spent"] == 0, "Общая сумма должна быть 0 для пустого DataFrame"
    assert result["cashback"] == 0, "Кэшбэк должен быть 0 для пустого DataFrame"
    assert result["top_5_transactions"].empty, "Топ-5 должен быть пустым для пустого DataFrame"
@pytest.mark.parametrize("time_str, expected_greeting", [
    ("30.01.2024 08:00:00", "Доброе утро"),
    ("30.01.2024 14:00:00", "Добрый день"),
    ("30.01.2024 19:00:00", "Добрый вечер"),
    ("30.01.2024 23:00:00", "Доброй ночи"),
    ("30.01.2024 03:00:00", "Доброй ночи")])

def test_hello_person_valid_time(time_str, expected_greeting):
    """Тестирование приветствия в зависимости от времени суток"""
    assert hello_person(time_str) == expected_greeting

def test_hello_person_invalid_format():
    """Тестирование обработки некорректного формата времени"""
    with pytest.raises(ValueError, match="Некорректный формат времени"):
        hello_person("2024-01-30 08:00:00")