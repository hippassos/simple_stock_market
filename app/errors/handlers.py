from app.errors import bp
from app.stocks.errors import error_response


@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    return error_response(500)
