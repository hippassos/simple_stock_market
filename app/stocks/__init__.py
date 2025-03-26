from flask import Blueprint

stocks = Blueprint('stocks', __name__)

from . import routes, models  # noqa:F401