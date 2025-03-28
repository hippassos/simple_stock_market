import logging
from flask import request
from functools import wraps
from app.stocks.errors import bad_request


def price_validation(f):
    """Assert that the price is"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        price = request.args.get('price')
        # This should be strengthened if localisation comes into play
        if price is None or not price.isdigit():
            logging.error("Invalid price input")
            return bad_request("Price must be a valid non-negative integer representing the value in pennies")
        return f(*args, **kwargs)
    return decorated_function
