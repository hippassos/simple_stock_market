import logging
from . import stocks_bp
from flask import request
from app.stocks.models import Stock, StockMarket

available_stocks = {
    "TEA": Stock("TEA", "Common", 0, 0, 100),
    "POP": Stock("POP", "Common", 8, 0, 100),
    "ALE": Stock("ALE", "Common", 23, 0, 60),
    "GIN": Stock("GIN", "Preferred", 8, 0.2, 100),
    "JOE": Stock("JOE", "Common", 13, 0, 250)
}

stock_market = StockMarket([], available_stocks)


@stocks_bp.route('/list_stocks', methods=['GET'])
def list_stocks():
    stocks = stock_market.list_stocks()
    return {
        "stocks": [s.__dict__ for s in stocks]
    }


@stocks_bp.route('/dividend_yield', methods=['GET'])
def dividend_yield():
    symbol = request.args.get('symbol')
    price = float(request.args.get('price', 0))
    stock = stock_market.get_stock(symbol)
    if not stock:
        logging.warning("Stock not found")
        return {"error": "Stock not found"}, 404
    return {
        "dividend_yield": stock.calculate_dividend_yield(price)
    }


@stocks_bp.route('/pe_ratio', methods=['GET'])
def pe_ratio():
    return {
        "pe_ratio": "hello world"
    }


@stocks_bp.route('/trade', methods=['POST'])
def trade():
    return {
        "trade": "hello world"
    }


@stocks_bp.route('/volume_weighted_price', methods=['GET'])
def volume_weighted_price():
    return {
        "volume_weighted_price": "hello world"
    }


@stocks_bp.route('/gbce_index', methods=['GET'])
def gbce_index():
    return {
        "gbce_index": "hello world"
    }
