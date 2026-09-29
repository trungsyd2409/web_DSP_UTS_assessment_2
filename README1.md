# FX Converter

## Author
Name: Quang Trung Nguyen
Student ID: 26643559

## Description

A Streamlit web app that converts an amount between two currencies using live and
historical exchange rate data from the [Frankfurter API](https://www.frankfurter.app/).
Users can:
- Enter an amount and pick a "From" and "To" currency from the full list of currencies
  supported by Frankfurter
- Fetch the **latest** conversion rate, converted amount and inverse rate
- Pick a **past date** and fetch the historical conversion rate for that date
- (Bonus) View a quarterly exchange-rate trend chart for the past 3 years between the
  selected currencies

### Challenges faced

- The assignment brief's general text convention for the output message and its own
  "For example" text differ slightly in punctuation. The screenshot mockup matched the
  "For example" version (a period before "The inverse rate"), so that convention was
  followed in `format_output()`.
- Decided to round **both** the rate and the converted amount to 4 decimal places using
  the same `round_rate()` helper, for internal consistency, even though the mockup
  screenshot displays the converted amount to 2 decimal places. Prioritised having one
  single, reusable rounding rule over matching the screenshot pixel-for-pixel.
- `get_historical_rate()` only returns the rate (not the date), per the function's
  defined signature. Frankfurter automatically rolls the rate back to the last business
  day if the requested date falls on a weekend or public holiday. Because the function
  cannot return the adjusted date, the app currently displays the date the user
  **selected**, which may not exactly be the date the underlying rate was published for.
- For the bonus rate-trend feature, quarterly data points are aligned to fixed calendar
  quarters (Jan/Apr/Jul/Oct) rather than counting exactly 3 months back from today. This
  avoids edge cases with invalid dates when adding months (e.g. 31 March + 1 month).
- `get_rate_trend()` uses a `ThreadPoolExecutor` to fetch the ~12 quarterly historical
  rates concurrently instead of one after another, since each call is I/O-bound
  (waiting on the network) rather than CPU-bound. Results are explicitly re-sorted by
  date afterwards, since threads can finish out of submission order.

### Features to implement in future

- Cache API responses so repeated look-ups for the same currency pair/date don't
  re-hit the network
- Let the user choose the number of years and currency pair used for the trend chart
- Add automated unit tests for the pure functions in `currency.py`

## How to Setup

- Python version: 3.x (developed with Python 3.11)
- Packages used:
  - `streamlit`
  - `requests`
  - `matplotlib` (used only for the bonus trend chart, to get the "month, then year only
    when it changes" x-axis labels via `matplotlib.dates.ConciseDateFormatter`)

Install dependencies:
```bash
pip install streamlit requests matplotlib
```

## How to Run the Program

From the folder containing all the project files:
```bash
streamlit run app.py
```
Streamlit will print a local URL (usually `http://localhost:8501`) — open it in a
browser to use the app.

## Project Structure

- `app.py` — main Streamlit script. Builds the UI (inputs, buttons) and wires together
  the functions from `frankfurter.py` and `currency.py` to display results.
- `api.py` — generic HTTP layer, knows nothing about currencies specifically.
- `frankfurter.py` — Frankfurter-specific service layer: builds the right URLs, calls
  `api.py`, and parses the JSON responses.
- `currency.py` — pure calculation/formatting helpers with no network calls.
- `README.md` — this file.

### List of functions

**`api.py`**
- `get_url(url)` — sends a GET request to `url` and returns `(status_code, text)`,
  returning a 4xx/5xx-style status with an error message string if the network call
  itself fails.

**`frankfurter.py`**
- `get_currencies_list()` — returns the list of all currency codes Frankfurter
  supports, or `None` on error.
- `get_latest_rates(from_currency, to_currency, amount)` — returns `(date, rate)` for
  the latest available conversion rate, or `(None, None)` on error.
- `get_historical_rate(from_currency, to_currency, from_date, amount)` — returns the
  conversion `rate` for a specific past date, or `None` on error.
- `get_rate_trend(from_currency, to_currency, years)` *(bonus)* — returns a
  `{date: rate}` dictionary of quarterly historical rates over the past `years` years,
  fetched concurrently.

**`currency.py`**
- `round_rate(rate)` — rounds a float to 4 decimal places.
- `reverse_rate(rate)` — returns the inverse of a rate (rounded), or `0` if the rate is
  `0`.
- `format_output(date, from_currency, to_currency, rate, amount)` — builds the display
  sentence shown in the app, including the converted amount and inverse rate.

## Citations

- Frankfurter API and documentation: https://www.frankfurter.app/
- Streamlit API reference (`st.line_chart`, `st.pyplot`, etc.): https://docs.streamlit.io/
- `matplotlib.dates.ConciseDateFormatter` documentation:
  https://matplotlib.org/stable/api/dates_api.html
