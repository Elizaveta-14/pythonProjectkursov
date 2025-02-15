import logging
from datetime import datetime
from typing import Optional

import pandas as pd

from logging_config import setup_logging
from settings import REPORTS_PATH
from src.decorators import decorator_record_file

setup_logging()
logger = logging.getLogger("my_log")


@decorator_record_file(REPORTS_PATH)
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция принимает на вход датафрейм с транзакциями, название категории, и опциональную дату в формате ДД.ММ.ГГГГ.
    Если дата не передана, то берется текущая дата.
    И возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    try:
        if not date:
            stop_date = datetime.now()

        else:
            stop_date = datetime.strptime(date, "%d.%m.%Y")

        logger.info("Определение даты, начиная с которой будут взяты операции для подсчета трат по категориям")

        start_date = stop_date - pd.Timedelta(days=90)

        logger.info("Проверка на наличие необходимых столбцов в датафрейм")

        required_columns = ["Дата платежа", "Категория", "Сумма операции"]
        for column in required_columns:

            if column not in transactions.columns:
                logger.error(f"Отсутствует необходимый столбец: {column}")

                return pd.DataFrame()

        logger.info("Преобразование дат операций в объект datatime")

        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

        logger.info("Формирование списка операций для формирования отчета")

        filtered_transactions = transactions[
            (transactions["Дата платежа"] >= start_date)
            & (transactions["Дата платежа"] <= stop_date)
            & (transactions["Категория"] == category)
            & (transactions["Сумма операции"] < 0)
        ]

        logger.info("Инициализация отчета")

        total_spending = filtered_transactions["Сумма операции"].abs().sum()

        result = pd.DataFrame({"Категория": [category], "Сумма трат": [total_spending]})

    except ValueError as ve:
        logger.error(f"Ошибка значения: {ve}")
        return pd.DataFrame()

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return pd.DataFrame()

    return result
