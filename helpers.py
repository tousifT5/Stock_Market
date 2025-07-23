import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import yfinance as yf
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol using yfinance."""

    try:
        # Create a Ticker object for the given symbol
        ticker = yf.Ticker(symbol.upper())

        # Get historical data for a short period (e.g., 1 day)
        # This is usually sufficient to get the latest price.
        # Use '1d' for the most recent day's data, or '5d' to ensure some data is returned
        # even if the market is closed or there's a temporary issue with '1d'.
        # auto_adjust=True ensures prices are adjusted for splits and dividends.
        hist = ticker.history(period="1d", auto_adjust=True)

        # If no data is returned (e.g., invalid symbol or no trading data for the period)
        if hist.empty:
            # Try a slightly longer period if 1d fails, just in case of temporary data gaps
            hist = ticker.history(period="5d", auto_adjust=True)
            if hist.empty:
                return None # Still no data, so symbol is likely invalid or untradeable

        # Get the latest adjusted close price
        # .iloc[-1] gets the last row (most recent data)
        # ['Close'] gets the 'Close' column (which is 'Adj Close' due to auto_adjust=True)
        price = round(float(hist["Close"].iloc[-1]), 2)

        # Get the company name (longName)
        # Use .info to get a dictionary of various company details
        # Use .get() with a default value to prevent KeyError if 'longName' is missing
        company_info = ticker.info
        name = company_info.get("longName", symbol.upper()) # Fallback to symbol if name not found

        return {
            "name": name,
            "price": price,
            "symbol": symbol.upper()
        }

    except Exception as e:
        # Catch any exceptions that might occur (e.g., network issues, invalid symbol format)
        print(f"Error looking up {symbol}: {e}")
        return None



# def lookup(symbol):
#     """Look up quote for symbol."""

#     # Prepare API request
#     symbol = symbol.upper()
#     end = datetime.datetime.now(pytz.timezone("US/Eastern"))
#     start = end - datetime.timedelta(days=7)

#     # Yahoo Finance API
#     url = (
#         f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
#         f"?period1={int(start.timestamp())}"
#         f"&period2={int(end.timestamp())}"
#         f"&interval=1d&events=history&includeAdjustedClose=true"
#     )
#     print("a")
#     # Query API
#     try:
#         response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
#         response.raise_for_status()
#         print(response)
#         # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
#         quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
#         quotes.reverse()
#         price = round(float(quotes[0]["Adj Close"]), 2)
#         return {
#             "name": symbol,
#             "price": price,
#             "symbol": symbol
#         }
#     except (requests.RequestException, ValueError, KeyError, IndexError):
#         return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
