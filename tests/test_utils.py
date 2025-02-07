import logging
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import pandas as pd
import pytest

from src.utils import (
    analyze_transactions,
    get_convert_amount,
    get_mask_account,
    hello_person,
    reading_xlsx,
    stock_prices,
)

logging.basicConfig(level=logging.INFO)


def test_get_mask_account_valid() -> None:
    """Тестирует корректную маскировку номера карты"""
    assert get_mask_account(1234567890123456) == "1234 ** 3456", "Ошибка в маскировании номера карты"


def test_get_mask_account_short_number() -> None:
    """Тестирует поведение при слишком коротком номере карты"""
    assert get_mask_account(12345) == "Ошибка: Неверный номер карты", "Ошибка при обработке короткого номера"


def test_get_mask_account_edge_case() -> None:
    """Тестирует граничный случай (ровно 6 цифр)"""
    assert get_mask_account(123456) == "1234 ** 3456", "Ошибка при обработке 6-значного номера"


def test_get_mask_account_large_number() -> None:
    """Тестирует длинный номер карты"""
    assert get_mask_account(9876543210987654321) == "9876 ** 4321", "Ошибка при обработке длинного номера"


class TestReadingXlsx(unittest.TestCase):

    @patch("pandas.read_excel")
    def test_reading_xlsx_success(self, mock_read_excel):
        """Тест для успешного считывания данных из EXCEL файла"""
        data = {
            "Дата операции": ["01.01.2023", "02.01.2023"],
            "Номер карты": ["1234567890", "0987654321"],
            "Сумма операции": [100.0, 200.0],
        }
        df = pd.DataFrame(data)
        mock_read_excel.return_value = df
        result = reading_xlsx("test_file.xlsx")
        expected_result = [
            {"Дата операции": "01.01.2023", "Номер карты": "1234567890", "Сумма операции": 100.0},
            {"Дата операции": "02.01.2023", "Номер карты": "0987654321", "Сумма операции": 200.0},
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




def test_analyze_transactions_empty() -> None:
    """Тестирует поведение с пустым DataFrame"""
    df = pd.DataFrame(columns=["Дата операции", "Сумма платежа"])

    result = analyze_transactions(df)

    assert result["total_spent"] == 0, "Общая сумма должна быть 0 для пустого DataFrame"
    assert result["cashback"] == 0, "Кэшбэк должен быть 0 для пустого DataFrame"
    assert result["top_5_transactions"].empty, "Топ-5 должен быть пустым для пустого DataFrame"


@pytest.mark.parametrize(
    "time_str, expected_greeting",
    [
        ("2024.01.30 08:00:00", "Доброе утро"),
        ("2024.01.30 14:00:00", "Добрый день"),
        ("2024.01.30 19:00:00", "Добрый вечер"),
        ("2024.01.30 23:00:00", "Доброй ночи"),
        ("2024.01.30 03:00:00", "Доброй ночи"),
    ],
)
def test_hello_person_valid_time(time_str, expected_greeting):
    """Тестирование приветствия в зависимости от времени суток"""
    assert hello_person(time_str) == expected_greeting


class TestGetConvertAmount(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"user_currencies": ["USD", "EUR"]}))
    @patch("os.getenv", return_value="fake_api_key")
    @patch("requests.get")
    def test_get_convert_amount(self, mock_requests_get, mock_getenv, mock_file):
        """Тестируем функцию на курс и конвертацию"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.50}}
        mock_requests_get.return_value = mock_response
        expected_result = [{"Валюта": "USD", "Цена": 75.50}, {"Валюта": "EUR", "Цена": 75.50}]
        result = get_convert_amount()
        self.assertEqual(result, expected_result)
        mock_requests_get.assert_any_call(
            "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
            headers={"apikey": "fake_api_key"},
        )
        mock_requests_get.assert_any_call(
            "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR",
            headers={"apikey": "fake_api_key"},
        )
        mock_getenv.assert_called_with("API_KEY")
        mock_file.assert_called_with("C:\\Users\\Asus\\PycharmProjects\\pythonProjectkursov\\.env", encoding="utf-8")


class TestStockPrices(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"user_stocks": ["AAPL", "GOOGL"]}))
    @patch("os.getenv", return_value="fake_api_key")
    @patch("requests.get")
    def test_stock_prices_no_matches(self, mock_requests_get, mock_getenv, mock_file):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"symbol": "MSFT", "price": 299.99},
            {"symbol": "TSLA", "price": 800.00},
        ]
        mock_requests_get.return_value = mock_response
        expected_result = []
        result = stock_prices()
        self.assertEqual(result, expected_result)
