import datetime
import logging
import os
from typing import Any
import json
import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_KEY")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def hello_person(time_str: str) -> str:
    """Функция приветсвия во времени суток"""
    try:
        current_time = datetime.datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S")
    except ValueError as e:
        raise ValueError("Некорректный формат времени. Ожидается формат: '%d.%m.%Y %H:%M:%S'") from e

    hour = current_time.hour
    if 6 <= hour <= 11:
        return "Доброе утро"
    elif 12 <= hour <= 16:
        return "Добрый день"
    elif 17 <= hour <= 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def reading_xlsx(filename: str) -> Any:
    """Считывает данные с EXCEL файла и переобразовыввает их в JSON-формат"""
    logger.info("Начали считывание информации с EXCEL-файла")
    try:
        operations = pd.read_excel(filename)
        operations = operations.where(pd.notnull(operations), operations.fillna("Отсутствует"))
        file_dict = operations.to_dict(orient="records")
        logger.info("Окончили считывание информации с EXCEL-файла")
        return file_dict
    except Exception as e:
        logger.error(f"Произошла ошибка {e} при считывание информации с EXCEL-файла")
        return f"Ошибка {e}. повторите попытку"


def get_mask_account(transaction_content: int) -> str:
    """Функция принимает на вход номер карты и возвращает маскированный номер по правилу
    XXXX"""
    str_number_card = str(transaction_content)
    if len(str_number_card) < 6:
        return "Ошибка: Неверный номер карты"
    logger.info("Успешно")
    return f"{str_number_card[:4]} ** {str_number_card[-4:]}"


def analyze_transactions(df: pd.DataFrame):
    """
    Анализирует транзакции по карте:
    - Общая сумма расходов
    - Кэшбэк (1 рубль за каждые 100 рублей)
    - Топ-5 транзакций по сумме платежа
    """
    if df.empty:
        return {"total_spent": 0, "cashback": 0, "top_5_transactions": pd.DataFrame()}

    total_spent = df["Сумма платежа"].sum()
    cashback = total_spent // 100

    top_5_transactions = df.nlargest(5, "Сумма платежа")

    return df.DataFrame({"total_spent": total_spent, "cashback": cashback, "top_5_transactions": top_5_transactions})


def get_convert_amount() -> list:
    """Функция выводит курс валют для необходимой валюты из файла"""
    logger.info("Получаем информацию с файла о необходимой цены валюты")
    with open("../data/user_setings.json", "r") as file:
        reading = json.load(file)["user_currencies"]

    load_dotenv()
    api_key = os.getenv("API_KEY")

    currency_rate = []
    logger.info("Производим запрос по API по небходимым валютам")
    for i in reading:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={i}"

        headers = {"apikey": f"{api_key}"}

        response = requests.get(url, headers=headers)

        get_value = round(response.json()["rates"]["RUB"], 2)
        currency_rate.append(dict(Валюта=i, Цена=get_value))
#        status_code = response.status_code
    logger.info("Окончили сбор информации по валютам")
    return currency_rate


def stock_prices() -> list:
    """Функция получает результаты по API цену акций"""
    logger.info("Получаем информацию с файла о необходимых цен на АКЦИИ")
    with open("../data/user_setings.json", "r") as file:
        reading = json.load(file)["user_stocks"]

        API_KEY = os.getenv("API_TOKEN_SP_SECOND")
        logger.info("Производим запрос по API")
        url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY}"
        response = requests.get(url)

        data = response.json()
        stock_price = []
        logger.info("Фильтруем список согласна необходимых данных")
        for i in data:
            for element in reading:
                if i["symbol"] == element:
                    stock_prices.append(dict(Акция=element, Цена=i["price"]))
        logger.info("Окончили сбор данных цен на АКЦИИ")
        return stock_price
