import json
import logging
import re
from datetime import datetime

from logging_config import setup_logging

setup_logging()
logger = logging.getLogger("my_log")


def get_profitable_cashback_categories(data: list, year: str, month: str) -> str:
    """
    На вход функции поступают данные для анализа, год и месяц.
    На выходе — JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года,
    в формате:
    {"Категория 1": 1000,
    "Категория 2": 2000,
    "Категория 3": 500}
    """
    filtered_data = []
    result = {}

    pattern_year = re.compile(r"\d{4}")
    pattern_month = re.compile(r"\d{2}")

    logger.info("Проверка на корректность введенных данных")

    if isinstance(data, list) and pattern_year.fullmatch(year) and pattern_month.fullmatch(month):
        if data and 12 >= int(month) > 0:

            for x in data:
                date_obj = datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S")
                year_part = date_obj.strftime("%Y")
                month_part = date_obj.strftime("%m")

                logger.info("Проверка операции на совпадение месяца и года для поиска")

                if year_part == year and month_part == month:

                    logger.info("Добавление подходящих операций в новый список")

                    filtered_data.append(x)
                    category = x["Категория"]
                    amount = x["Сумма операции"]

                    if category not in result and amount < 0:
                        if category != "Переводы":
                            result[category] = 0.0

                            logger.info("Формирование результата с категориями и подсчет кэшбека")

                            result[category] += abs(amount * 0.01)

                else:
                    logger.warning("Дата операции отличается от запроса")

    else:
        logger.error("Передан неверный тип данных")

    logger.info("Приводим результат к формату json")

    filtered_result = dict(sorted(result.items(), key=lambda value: value[1], reverse=True))
    parsed_result = json.dumps(filtered_result, ensure_ascii=False)

    return parsed_result
