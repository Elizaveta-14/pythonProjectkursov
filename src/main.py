from typing import Any
from views import generate_main_page
from src.services import get_profitable_cashback_categories
from reports import spending_by_category
def main() -> Any:
    """Функция для запуска всего проекта"""
# Главная страница
print("\nГЛАВНАЯ\n")
print(generate_main_page("currency_code",  "transaction_content"))

# Страница Событие
print("\nСОБЫТИЕ\n")
print(get_profitable_cashback_categories)


# Страница Отчеты
print("\nОТЧЕТЫ\n")
print(spending_by_category)


if __name__ == '__main__':
    main()