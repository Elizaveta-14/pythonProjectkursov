import json
import logging
from datetime import datetime

from logging_config import setup_logging
from settings import EXCEL_PATH, JSON_PATH
from src.reports import spending_by_category
from src.services import get_profitable_cashback_categories
from src.utils import get_currency_rate, get_json_currencies, get_json_stocks, get_stock_price, get_xlsx
from src.views import get_card_info, get_top_transactions, greetings, sort_by_date

setup_logging()
logger = logging.getLogger("utils")


def views_main(date: str) -> str:
    """
    Функция, принимающая на вход строку с датой и временем
    в формате YYYY-MM-DD HH:MM:SS и возвращающая JSON-ответ
    """
    actual_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    correct_date = actual_date.strftime("%d.%m.%Y")
    correct_time = actual_date.strftime("%H:%M:%S")

    sort_operations_list = sort_by_date(operations_list, correct_date)

    greeting = greetings(correct_time)
    cards = get_card_info(sort_operations_list)
    top_transactions = get_top_transactions(sort_operations_list)
    currency_rates = [get_currency_rate(cur) for cur in get_json_currencies(JSON_PATH)]
    stock_prices = [get_stock_price(st) for st in get_json_stocks(JSON_PATH)]

    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    parsed_result = json.dumps(result, ensure_ascii=False)

    return parsed_result


if __name__ == "__main__":
    operations_list, df = get_xlsx(EXCEL_PATH)
    my_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    json_main = views_main(my_date)
    services_main = get_profitable_cashback_categories(operations_list, "2022", "04")

    spending_by_category(df, "Рестораны", "25.02.2024")
#    print(views_main("2021-12-01 14:15:15"))
