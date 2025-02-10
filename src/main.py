from typing import Any

from src.reports import spending_by_category
from src.services import get_profitable_cashback_categories
from src.views import generate_main_page


def main(data, year, month,transaction_content, time_str) -> Any:
    """Функция для запуска проекта"""

     # Главная страница
    print("\nГЛАВНАЯ\n")
    print(generate_main_page(transaction_content, time_str, data))
    # Страница Событие
    print("\nСОБЫТИЕ\n")
    print(get_profitable_cashback_categories(data, year, month))
    # Страница Отчеты
    print("\nОТЧЕТЫ\n")
    print(spending_by_category())


#if __name__ == "__main__":
 #    main('data', 'year', 'month', 'transaction_content', "time_str")