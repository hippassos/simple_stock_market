import logging
from flask import request
from functools import wraps
from app.stocks.errors import bad_request, error_msgs, error_response
from app.stocks.models import stock_market


def numbers_validated(args_to_validate: list):
    def numeric_validation(f):
        """Assert that a value is a non-negative interger (natural number)."""

        @wraps(f)
        def decorated_function(*args, **kwargs):
            for arg in args_to_validate:
                if request.method == "GET":
                    value = request.args.get(arg)
                    # isdigit() condition should be strengthened if localisation comes into play
                    if value is None or not value.isdigit():
                        logging.error(f"Invalid {arg} input, {value}")
                        return bad_request(error_msgs.get(arg))
                else:
                    value = request.json.get(arg)
                    if value is None or not isinstance(value, int):
                        logging.error(f"Invalid {arg} input, {value}")
                        return bad_request(error_msgs.get(arg))
            return f(*args, **kwargs)

        return decorated_function

    return numeric_validation


def trade_type_validation(f):
    """Assert that a value is a non-negative interger (natural number)."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        value = request.json.get("type")
        if value is None or value not in ["buy", "sell"]:
            logging.error(f"Invalid trade type input, {value}")
            return bad_request(error_msgs.get("trade_type"))
        return f(*args, **kwargs)

    return decorated_function


def symbol_validation(f):
    """Assert that a value is a non-negative interger (natural number)."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "GET":
            value = request.args.get("symbol")
        else:
            value = request.json.get("symbol")
        stock_symbol = stock_market.get_stock(value)
        if value is None or stock_symbol is None:
            # keep track to understand if there is trend on stocks requested that are not available
            logging.error(f"Stock requested is not available, {value}")
            return error_response(404, error_msgs.get("symbol"))
        return f(*args, **kwargs)

    return decorated_function
