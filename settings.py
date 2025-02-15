from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

EXCEL_PATH = BASE_DIR.joinpath("data/operations.xlsx")
JSON_PATH = BASE_DIR.joinpath("user_settings.json")
LOG_PATH = BASE_DIR.joinpath("logs/app.log")
REPORTS_PATH = BASE_DIR.joinpath("reports.json")
