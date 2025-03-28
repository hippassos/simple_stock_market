from flask import Blueprint

bp = Blueprint('stocks', __name__)

from . import routes, models, errors  # noqa:F401
