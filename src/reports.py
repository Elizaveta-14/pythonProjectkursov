import functools
from datetime import datetime, timedelta
import os
import logging
from typing import Any, Callable
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_log_file_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\pythonProjectkursov\\logs\\reports.log")
abs_log_file_path = os.path.abspath(rel_log_file_path)
logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file_default(func: Callable) -> Callable:
    """Записывает в файл результат, который возвращает функция, формирующая отчет."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        with open("function_operation_report.txt", "w") as file:
            file.write(str(result))
        logger.info(f"Записан результат работы функции {func}")
        return result

    return wrapper


def report_to_file(filename: str = "function_operation_report.txt") -> Callable:
    """Записывает в переданный файл результат, который возвращает функция, формирующая отчет."""

    def decorator(func: Callable[[tuple[Any, ...], dict[str, Any]], Any]) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            with open(filename, "w") as file:
                file.write(str(result))
            logger.info(f"Записан результат работы функции {func} в файл {filename}")
            return result

        return wrapper

    return decorator


@report_to_file_default
def spending_by_category(transactions: pd.DataFrame, category: str, date: Any = None) -> Any:
    """Функция возвращает траты по заданной категории за последние три месяца
    (от переданной даты, если дата не передана берет текущую)"""
    try:
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        if date is None:
            date = datetime.now()
        else:
            date = datetime.strptime(date, "%Y.%m.%d")
        start_date = date - timedelta(days=date.day - 1) - timedelta(days=3 * 30)
        filtered_transactions = transactions[
            (transactions["Дата операции"] >= start_date)
            & (transactions["Дата операции"] <= date)
            & (transactions["Категория"] == category)
        ]
        grouped_transactions = filtered_transactions.groupby(pd.Grouper(key="Дата операции", freq="ME")).sum()
        logger.info(f"Траты за последние три месяца от {date} по категории {category}")
        return grouped_transactions.to_dict(orient="records")
    except Exception as e:
        print(f"Возникла ошибка {e}")
        logger.error(f"Возникла ошибка {e}")
        return ""
