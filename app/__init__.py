from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # register blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.stocks import bp as stocks_bp
    app.register_blueprint(stocks_bp, url_prefix='/stocks')

    return app
