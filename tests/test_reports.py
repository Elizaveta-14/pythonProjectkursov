import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame(
                {
                    "Дата платежа": ["01.01.2025", "01.01.2025", "02.01.2025", "03.01.2025"],
                    "Категория": ["Такси", "Еда", "Такси", "Супермаркеты"],
                    "Сумма операции": [-777, -555, -1312, -666],
                }
            ),
            pd.DataFrame({"Категория": ["Еда"], "Сумма трат": [555]}),
        )
    ],
)
def test_spending_by_category(df, expected):
    result = spending_by_category(df, "Еда", "01.01.2025")
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "df, expected",
    [
        (
            pd.DataFrame(
                {
                    "Дата платежа": ["01.01.2025", "01.01.2025", "02.01.2025", "03.01.2025"],
                    "Категория": ["Такси", "Еда", "Такси", "Супермаркеты"],
                    "Сумма операции": [-777, -555, -1312, -666],
                }
            ),
            pd.DataFrame({"Категория": ["Еда"], "Сумма трат": [555]}),
        )
    ],
)
def test_spending_by_category_not_date(df, expected):
    result = spending_by_category(df, "Еда")
    pd.testing.assert_frame_equal(result, expected)
