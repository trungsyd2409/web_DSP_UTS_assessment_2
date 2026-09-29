# FX Converter

## Author
Name: Quang Trung Nguyen
Student ID: 26643559

## Description
A Streamlit web app that converts an amount between 2 currencies using live and historical exchange rate data from [Frankfurter API](https://www.frankfurter.app/).

Users can:
- Enter an amount and pick a "From" and "To" currency from the full list of currencies supported by Frankfurter.
- Fetch the latest conversion rate, converted amount and inverse rate.
- Pick a past date and fetch the historical conversion rate for the date.
- View a quarterly exchange-rate trend chart for the past 3 years between the selected currencies.

### Challenges faced
- Chart rendering doesn't fully match the reference mockup.
- Sequential API calls made the trend chart slow to load: Fetching approximately 12 quarterly rates one by one made the app feel slow. A ThreadPoolExecutor was used to fire all requests concurrently instead, cutting the wait to roughly one request's time.
- For the bonus rate-trend feature, quarterly data points are aligned to fixed calendar quarters (Jan/Apr/Jul/Oct) rather than counting exactly 3 months back from today. This avoids edge cases with invalid dates when adding months.
- `get_historical_rate()` only returns the rate, not the date, so when the requested date falls on a weekend or public holiday (and Frankfurter rolls the rate back to the last business day), the app still displays the date the user selected rather than the actual rate date.

### Feature to implement in future
- Improve the rendering performance of the trend chart, and allow users to select number of years.

## How to Setup
- Python version: 3.x (developed with Python 3.11)
- Packages used: `streamlit` and `requests`


- Create and activate a virtual environment (Windows):
```bash
python -m venv .venv
.venv\Scripts\activate
```


- Install dependencies:
```bash
pip install streamlit requests
```

## How to Run the Program
From the folder containing all the project files
```bash
streamlit run app.py
```
Streamlit will print a local URL (usually `http://localhost:8501`) - open it in a browser to use the app.

## Project Structure
- `app.py` - main Streamlit script. Builds the UI (inputs, buttons) and wires together the functions from `frankfurter.py` and `currency.py` to display results.
- `api.py` - generic HTTP layer, knows nothing about currencies specifically.
- `frankfurter.py` - Frankfurter-specific service layer: builds the right URLs, calls `api.py`, and parses the JSON responses.
- `currency.py` - pure calculation/formatting helpers with no network calls.
- `README.md` - this file.


### List of functions

**`api.py`**
- `get_url(url)` - sends a GET request to `url` and returns `(status_code, text)`, returning a 4xx/5xx-style status with an error message string if the network call itself fails.

**`frankfurter.py`**
- `get_currencies_list()` - returns the list of all currency codes Frankfurter supports, or `None` on error.
- `get_latest_rates(from_currency, to_currency, amount)` - returns `(date, rate)` for the latest available conversion rate, or `(None, None)` on error.
- `get_historical_rate(from_currency, to_currency, from_date, amount)` - returns the conversion `rate` for a specific past date, or `None` on error.
- `get_rate_trend(from_currency, to_currency, years)` *(bonus)* - returns a `{date: rate}` dictionary of quarterly historical rates over the past `years` years, fetched concurrently.

**`currency.py`**
- `round_rate(rate)` - rounds a float to 4 decimal places.
- `reverse_rate(rate)` - returns the inverse of a rate (rounded), or `0` if the rate is `0`.
- `format_output(date, from_currency, to_currency, rate, amount)` - builds the display sentence shown in the app, including the converted amount and inverse rate.



## Citations
- Frankfurter API and documentation: https://www.frankfurter.app/
- Streamlit API reference: https://docs.streamlit.io/
