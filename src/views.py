import pandas as pd
from src.utils import hello_person, get_mask_account, get_convert_amount, analyze_transactions, stock_prices


def generate_main_page(data: pd.DataFrame, currency_code: str, amount: float, transaction_content: int) -> dict:
    """Формирует главную страницу приложения с анализом данных и информацией о пользователе."""
    greeting = hello_person()
    masked_account = get_mask_account(transaction_content)
    converted_amount = get_convert_amount(currency_code, amount)
    transaction_analysis = analyze_transactions(data)
    stock_pricess = stock_prices()

    main_page_data = {
        "greeting": greeting,
        "masked_account": masked_account,
        "converted_amount": converted_amount,
        "transaction_analysis": transaction_analysis,
        "stock_pricess": stock_pricess,
    }

    return main_page_data
