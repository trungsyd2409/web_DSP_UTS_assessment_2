# FX Converter

## Author
Name: Quang Trung Nguyen
Student ID: 26643559

## Description
A Streamlit web app that converts an amount between 2 currencies using live and histogical exchange rate data from [Frankfurter API](https://www.frankfurter.app/).

Users can:
- Enter an amount and pick a "From" and "To" currency from the full list of currencies supported by Frankfurter.
- Fetch the lastest conversion rate, converted amount and inverse rate.
- Pick a past date and fetch the historical conversion rate for the date.
- View a quaterly exchange-rate trend chart for the past 3 years between the selected currencies.

### Challenges faced
- Chart rendering doesn't fully match the referance mockup.
- Sequential API calls made the trend chart slow to load: Fetching approximately 12 quaterly rates one by one made the app feel slow. A ThreadPoolExecutor was used to fire all reqeusts concurrently instead, cutting the wait to roughly one request's time.

### Feature to implement in future
- Improve the rendering performance of the trend chart, and allow users to select number of years.

## How to Setup
- Python version: 3.x (developed with Python 3.11)
- Pakages used: `streamlit` and `requests`


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
Streamlit will print a local URL (usually `http://localhost:8501`) - open it in a brower to use the app.

## Project Structure
- `app.py` — main Streamlit script. Builds the UI (inputs, buttons) and wires together
  the functions from `frankfurter.py` and `currency.py` to display results.
- `api.py` — generic HTTP layer, knows nothing about currencies specifically.
- `frankfurter.py` — Frankfurter-specific service layer: builds the right URLs, calls
  `api.py`, and parses the JSON responses.
- `currency.py` — pure calculation/formatting helpers with no network calls.
- `README.md` — this file.

## Citations
- Frankfurter API and documentation: https://www.frankfurter.app/
- Streamlit API reference (`st.line_chart`, `st.pyplot`, etc.): https://docs.streamlit.io/
