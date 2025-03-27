from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # register blueprints
    from .stocks import stocks_bp as stocks_blueprint
    app.register_blueprint(stocks_blueprint, url_prefix='/stocks')

    return app