import logging
from app.stocks import bp
from flask import request
from app.stocks.models import Stock, StockMarket
from app.stocks.decorators import price_validation
from app.stocks.errors import error_response

available_stocks = {
    "TEA": Stock("TEA", "Common", 0, 0, 100),
    "POP": Stock("POP", "Common", 8, 0, 100),
    "ALE": Stock("ALE", "Common", 23, 0, 60),
    "GIN": Stock("GIN", "Preferred", 8, 0.2, 100),
    "JOE": Stock("JOE", "Common", 13, 0, 250)
}

stock_market = StockMarket([], available_stocks)


@bp.route('/list_stocks', methods=['GET'])
def list_stocks():
    stocks = stock_market.list_stocks()
    return {
        "stocks": [s.__dict__ for s in stocks]
    }


@bp.route('/dividend_yield', methods=['GET'])
@price_validation
def dividend_yield():
    symbol = request.args.get('symbol')
    price = int(request.args.get('price', 0))
    stock = stock_market.get_stock(symbol)
    if not stock:
        # keep track for future analytics for client needs
        logging.error(f"Not available stock requested with symbol: {symbol}")
        return error_response(404, "Stock not found")
    logging.info(f"Calculating dividend yield for {symbol} at price {price}")
    return {
        "dividend_yield": stock.calculate_dividend_yield(price)
    }


@bp.route('/pe_ratio', methods=['GET'])
@price_validation
def pe_ratio():
    symbol = request.args.get('symbol')
    price = int(request.args.get('price', 0))
    stock = stock_market.get_stock(symbol)
    if not stock:
        # keep track for future analytics for client needs
        logging.error(f"Not available stock requested with symbol: {symbol}")
        return error_response(404, "Stock not found")
    logging.info(f"Calculating P/E ratio for {symbol} at price {price}")
    return {
        "pe_ratio": stock.calculate_pe_ratio(price)
    }


@bp.route('/trade', methods=['POST'])
def trade():
    return {
        "trade": "hello world"
    }


@bp.route('/volume_weighted_price', methods=['GET'])
def volume_weighted_price():
    return {
        "volume_weighted_price": "hello world"
    }


@bp.route('/gbce_index', methods=['GET'])
def gbce_index():
    return {
        "gbce_index": "hello world"
    }
