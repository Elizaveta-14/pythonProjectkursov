from typing import Any
from src.views import generate_main_page
from src.services import get_profitable_cashback_categories
from src.reports import spending_by_category


def main(data, year, month,transaction_content, time_str) -> Any:
    """Функция для запуска проекта"""
    if __name__ == "__main__":
        main()
        # Главная страница
        print("\nГЛАВНАЯ\n")
        print(generate_main_page(transaction_content, time_str))
        # Страница Событие
        print("\nСОБЫТИЕ\n")
        print(get_profitable_cashback_categories(data, year, month))
        # Страница Отчеты
        print("\nОТЧЕТЫ\n")
        print(spending_by_category())
