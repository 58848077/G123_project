import requests
import os
import datetime
from dotenv import load_dotenv

# Required settings to use Django ORM directly; they should be imported before accessing ORM models.
import django
os.environ['DJANGO_SETTINGS_MODULE'] = "financial.financial.settings"
django.setup()

from financial.fin_data.models import financial_data


def get_date_two_weeks_ago():
    """
    Returns:
        String: The date string for two weeks ago (yyyy-mm-dd).
    """
    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(days=14)
    two_weeks_ago_month = f"0{two_weeks_ago.month}" if len(str(two_weeks_ago.month)) == 1 else two_weeks_ago.month
    two_weeks_ago_day = f"0{two_weeks_ago.day}" if len(str(two_weeks_ago.day)) == 1 else two_weeks_ago.day
    return f"{two_weeks_ago.year}-{two_weeks_ago_month}-{two_weeks_ago_day}"

def get_stock_data():
    """
    Get the financial data of TWO given stocks(IBM, Apple Inc.) for the past two weeks.
    """
    # Get ALPHAVANTAGE API KEY from .env file. 
    load_dotenv()
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

    date_two_weeks_ago = get_date_two_weeks_ago()
    stocks = ["IBM", "AAPL"]
    data = []

    # Retrieve IBM and Apple Inc. financial data recursively.
    for stock in stocks:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&apikey={ALPHAVANTAGE_API_KEY}'
        response = requests.get(url)
        response = response.json()
        fin_data = [ financial_data(symbol=stock, date=date, open_price=float(value["1. open"]), close_price=float(value["4. close"]), volume=value["6. volume"]) for date, value in response["Time Series (Daily)"].items() if date > date_two_weeks_ago ]
        data += fin_data
    
    # Django ORM provides a function that allows the insertion of a batch of data. When the ignore_conflicts parameter is set to True, any duplicate records will be ignored.
    financial_data.objects.bulk_create(data, ignore_conflicts=True)
    
    return

if __name__ == '__main__':
    get_stock_data()
