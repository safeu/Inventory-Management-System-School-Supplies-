import os

class Settings:
    BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    DATABASE = "inventory.db"
    DATABASE_PATH = os.path.join(BASE_DIRECTORY, DATABASE)

    LOW_STOCK_THRESHOLD = 10
    #MARKUP_PERCENTAGE = 0.20
    #AX_RATE = 0.07
    #SALES_REPORT_DAYS = 30
