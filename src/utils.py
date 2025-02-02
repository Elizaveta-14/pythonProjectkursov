import json
import os
import logging
import requests
from dotenv import load_dotenv
import pandas as pd
import datetime
from typing import Any
load_dotenv()
api_key = os.getenv("API_KEY")

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_log_file_path = os.path.join("C:\\Users\\Asus\\PycharmProjects\\pythonProjectkursov\\logs\\utils.log")
abs_log_file_path = os.path.abspath(rel_log_file_path)
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(abs_log_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def hello_person(current_time):
    """Функция приветсвия во времени суток"""
    try:
        current_time = datetime.datetime.strptime(current_time, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        raise ValueError("Некорректный формат времени")

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


def get_convert_amount(currency_code, amount):
    """Проверяет текущий курс валюты"""
    try:
        if currency_code == "USD" or currency_code == "EUR":
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}"
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        json_result = response.json()
        rub_amount = json_result["result"]
        return round(rub_amount, 2)

    except KeyError:
        return 0


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

    return {
        "total_spent": total_spent,
        "cashback": cashback,
        "top_5_transactions": top_5_transactions}

def stock_prices(info):
    """Подключаемся к API, получаем наименование акции и ее цену, добавляем в словарь info"""
    try:
        logger.info("Good stocks")
        data_json = {
            "data": {
                "trends": [
                    {"name": "S&P 500", "price": 4500.50},
                    {"name": "Dow Jones", "price": 34000.75},
                    {"name": "NASDAQ", "price": 15000.25},
                ]
            }
        }

        info["stock_prices"] = []

        for trend in data_json["data"]["trends"]:
            info["stock_prices"].append({"stock": trend["name"], "price": trend["price"]})
        return info
    except Exception as e:
        logger.error("Everybody has problems with foreign stocks.")
        print(f"We have a problem with stocks, Watson: {e}")

