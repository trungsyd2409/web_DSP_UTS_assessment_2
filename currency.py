def round_rate(rate):
    """
    Function that will round an input float to 4 decimals places.

    Parameters
    ----------
    rate: float
        Rate to be rounded

    Returns
    -------
    float
        Rounded rate
    """
    return round(rate, 4)


def reverse_rate(rate):
    """
    Function that will calculate the inverse rate from the provided input rate.
    It will check if the provided input rate is not equal to zero.
    If it not the case, it will calculate the inverse rate and round it to 4 decimal places.
    Otherwise it will return zero.

    Parameters
    ----------
    rate: float
        FX conversion rate to be inverted

    Returns
    -------
    float
        Inverse of input FX conversion rate
    """
    return round_rate(1 / rate) if rate != 0 else 0


def format_output(date, from_currency, to_currency, rate, amount):
    """
    Function that will format the text to be displayed in the Streamlit app.

    Parameters
    ----------
    date: str
        Date of the conversion rate
    from_currency: str
        Origin currency code
    to_currency: str
        Destination currency code
    rate: float
        Conversion rate
    amount: float
        Amount to be converted

    Returns
    -------
    str
        Formatted text for display
    """
    result = f"The conversion rate on {date} from {from_currency} to {to_currency} was {rate}. So {amount} in {from_currency} correspond to {round_rate(rate * amount)} in {to_currency}. The inverse rate was {reverse_rate(rate)}."
    return result
