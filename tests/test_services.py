import unittest
from unittest.mock import patch
import json

from src.services import get_profitable_cashback_categories


class TestProfitableCashbackCategories(unittest.TestCase):

    @patch("src.services.logger")
    def test_get_profitable_cashback_categories_valid_data(self, mock_logger):
        """Тестируем работу функции с валидными данными"""
        data = [
            {"Дата операции": "15.03.2023 10:15:00", "Категория": "Еда", "Сумма операции": -120.0},
            {"Дата операции": "20.03.2023 14:00:00", "Категория": "Еда", "Сумма операции": -250.0},
            {"Дата операции": "25.03.2023 12:30:00", "Категория": "Техника", "Сумма операции": -500.0},
            {"Дата операции": "10.03.2023 16:45:00", "Категория": "Техника", "Сумма операции": -300.0},
            {"Дата операции": "05.03.2023 18:00:00", "Категория": "Переводы", "Сумма операции": -100.0},
        ]
        expected_result = {"Техника": 5.0, "Еда": 1.2}
        expected_json_result = json.dumps(expected_result, ensure_ascii=False)
        result = get_profitable_cashback_categories(data, "2023", "03")
        self.assertEqual(result, expected_json_result)

    @patch("src.services.logger")
    def test_get_profitable_cashback_categories_invalid_data(self, mock_logger):
        """Тестируем работу функции с некорректными данными (невалидный год и месяц)"""
        data = [
            {"Дата операции": "15.03.2023 10:15:00", "Категория": "Еда", "Сумма операции": -120.0},
            {"Дата операции": "20.03.2023 14:00:00", "Категория": "Еда", "Сумма операции": -250.0},
        ]
        result = get_profitable_cashback_categories(data, "2023", "13")  # Месяц не существует
        self.assertEqual(result, "{}")  # Ожидаем пустой результат

        result = get_profitable_cashback_categories(data, "20X3", "03")  # Некорректный формат года
        self.assertEqual(result, "{}")  # Ожидаем пустой результат

    @patch("src.services.logger")
    def test_get_profitable_cashback_categories_empty_data(self, mock_logger):
        """Тестируем работу функции с пустыми данными"""
        data = []
        result = get_profitable_cashback_categories(data, "2023", "03")
        self.assertEqual(result, "{}")

    @patch("src.services.logger")
    def test_get_profitable_cashback_categories_no_matching_month(self, mock_logger):
        """Тестируем случай, когда нет транзакций, соответствующих месяцу и году"""
        data = [
            {"Дата операции": "15.01.2023 10:15:00", "Категория": "Еда", "Сумма операции": -120.0},
            {"Дата операции": "20.01.2023 14:00:00", "Категория": "Еда", "Сумма операции": -250.0},
        ]
        result = get_profitable_cashback_categories(data, "2023", "03")
        self.assertEqual(result, "{}")
