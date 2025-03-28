from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app.stocks import bp


def error_response(status_code, message=None):
    """Universaly inject short descriptions of HTTP status codes to the error response."""
    payload = {
        'code': status_code,
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
    }
    if message:
        payload['message'] = message
    return payload, status_code


def bad_request(message):
    """Quality of life function for the most common error API response."""
    return error_response(400, message)


@bp.errorhandler(HTTPException)
def handle_exception(e):
    """Catch-all error handler, usually raised through flask.abort()."""
    return error_response(e.code)
