import logging
from flask import request
from functools import wraps
from app.stocks.errors import bad_request, error_msgs


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
