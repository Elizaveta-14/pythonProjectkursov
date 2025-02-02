import pytest
import unittest
from unittest.mock import patch
import pandas as pd
import logging
from src.utils import (reading_xlsx , get_mask_account, get_convert_amount, analyze_transactions,stock_prices,
                       hello_person)

logging.basicConfig(level=logging.INFO)


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


class TestReadingXlsx(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_reading_xlsx_success(self, mock_read_excel):
        """Тест для успешного считывания данных из EXCEL файла"""
        data = {
            'Дата операции': ['01.01.2023', '02.01.2023'],
            'Номер карты': ['1234567890', '0987654321'],
            'Сумма операции': [100.0, 200.0],
        }
        df = pd.DataFrame(data)
        mock_read_excel.return_value = df
        result = reading_xlsx("test_file.xlsx")
        expected_result = [
            {'Дата операции': '01.01.2023', 'Номер карты': '1234567890', 'Сумма операции': 100.0},
            {'Дата операции': '02.01.2023', 'Номер карты': '0987654321', 'Сумма операции': 200.0},
        ]
        self.assertEqual(result, expected_result)


    @patch("pandas.read_excel")
    def test_reading_xlsx_empty_file(self, mock_read_excel):
        """Тест для случая с пустым файлом"""
        df = pd.DataFrame()
        mock_read_excel.return_value = df
        result = reading_xlsx("empty_file.xlsx")
        self.assertEqual(result, [])


    @patch("pandas.read_excel")
    def test_reading_xlsx_invalid_format(self, mock_read_excel):
        """Тест для случая с файлом неправильного формата"""
        mock_read_excel.side_effect = ValueError("Ошибка формата файла")
        result = reading_xlsx("invalid_format_file.xlsx")
        self.assertEqual(result, "Ошибка Ошибка формата файла. повторите попытку")


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


@pytest.mark.parametrize(
    "input_stock, exit_stock",
    [
        (
            {},
            {
                "stock_prices": [
                    {"stock": "S&P 500", "price": 4500.5},
                    {"stock": "Dow Jones", "price": 34000.75},
                    {"stock": "NASDAQ", "price": 15000.25},
                ]
            },
        )
    ],
)
def test_stock_prices(input_stock, exit_stock):
    assert stock_prices(input_stock) == exit_stock