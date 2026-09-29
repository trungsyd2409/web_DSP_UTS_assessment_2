from api import get_url
import json
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
BASE_URL = "https://api.frankfurter.app"


def get_currencies_list():
    """
    Function that will call the relevant API endpoint from Frankfurter in order to get the list of available currencies.
    After the API call, it will perform a check to see if the API call was successful.
    If it is the case, it will load the response as JSON, extract the list of currency codes and return it as Python list.
    Otherwise it will return the value None.

    Parameters
    ----------
    None

    Returns
    -------
    list
        List of available currencies or None in case of error
    """
    code, response = get_url(f"{BASE_URL}/currencies")
    if code == 200:
        currencies_dict = json.loads(response)
        currency_list = list(currencies_dict.keys())
        return currency_list
    else:
        return None


def get_latest_rates(from_currency, to_currency, amount):
    """
    Function that will call the relevant API endpoint from Frankfurter in order to get the latest conversion rate between the provided currencies. 
    After the API call, it will perform a check to see if the API call was successful.
    If it is the case, it will load the response as JSON, extract the latest conversion rate and the date and return them as 2 separate objects.
    Otherwise it will return the value None twice.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    amount : float
        The amount (in origin currency) to be converted

    Returns
    -------
    str
        Date of latest FX conversion rate or None in case of error
    float
        Latest FX conversion rate or None in case of error
    """
    url = f"{BASE_URL}/latest?from={from_currency}&to={to_currency}"
    code, response = get_url(url)
    if code == 200:
        data = json.loads(response)
        date = data["date"]
        rate = data["rates"][to_currency]
        return date, rate
    else:
        return None, None


def get_historical_rate(from_currency, to_currency, from_date, amount):
    """
    Function that will call the relevant API endpoint from Frankfurter in order to get the conversion rate for the given currencies and date
    After the API call, it will perform a check to see if the API call was successful.
    If it is the case, it will load the response as JSON, extract the conversion rate and return it.
    Otherwise it will return the value None.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    amount : float
        The amount (in origin currency) to be converted
    from_date : str
        Date when the conversion rate was recorded

    Returns
    -------
    float
        Latest FX conversion rate or None in case of error
    """
    url = f"{BASE_URL}/{from_date}?from={from_currency}&to={to_currency}"
    code, response = get_url(url)
    if code == 200:
        data = json.loads(response)
        rate = data["rates"][to_currency]
        return rate
    else:
        return None


def get_rate_trend(from_currency: str, to_currency: str, years: int) -> dict:
    """
    Fetches historical rates for the past N years on a quarterly basis and returns a dictionary with dates as keys and rates as values.

    Parameters
    ----------
    from_currency : str
        Code for the origin currency
    to_currency : str
        Code for the destination currency
    years : int
        Number of years in the past for which to fetch rates

    Returns
    -------
    dict
        Dictionary containing dates and their corresponding rates
    """
    end_date = datetime.date.today()
    year = end_date.year
    month = ((end_date.month - 1) // 3) * 3 + 1

    # pre-generate the list of dates to fetch without any API calls
    quarter_dates = []
    for i in range(years * 4):
        quarter_dates.append(datetime.date(year, month, 1))
        month -= 3
        if month <= 0:
            month += 12
            year -= 1

    # fetch the rates concurrently using a thread pool
    trend_data = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_date = {
            executor.submit(
                get_historical_rate, from_currency, to_currency,
                d.strftime("%Y-%m-%d"), 1
            ): d
            for d in quarter_dates
        }
        for future in as_completed(future_to_date):
            d = future_to_date[future]
            rate = future.result()
            if rate is not None:
                trend_data[d.strftime("%Y-%m-%d")] = rate

    # return result
    return dict(sorted(trend_data.items()))
