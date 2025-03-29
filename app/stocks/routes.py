import logging
from app.stocks import bp
from flask import request
from app.stocks.models import Stock, StockMarket
from app.stocks.decorators import numbers_validated, trade_type_validation
from app.stocks.errors import error_response

available_stocks = {
    "TEA": Stock("TEA", "Common", 0, 0, 100),
    "POP": Stock("POP", "Common", 8, 0, 100),
    "ALE": Stock("ALE", "Common", 23, 0, 60),
    "GIN": Stock("GIN", "Preferred", 8, 0.2, 100),
    "JOE": Stock("JOE", "Common", 13, 0, 250)
}

stock_market = StockMarket([], available_stocks)


@bp.route("/list_stocks", methods=["GET"])
def list_stocks():
    stocks = stock_market.list_stocks()
    return {
        "stocks": [s.__dict__ for s in stocks]
    }


@bp.route("/list_trades", methods=["GET"])
def list_trades():
    trades = stock_market.list_trades()
    return {
        "trades": [t.__dict__ for t in trades]
    }


@bp.route("/dividend_yield", methods=["GET"])
@numbers_validated(["price"])  # input validation
def dividend_yield():
    symbol = request.args.get("symbol")
    price = int(request.args.get("price", 0))
    stock = stock_market.get_stock(symbol)
    if not stock:
        # keep track to understand if there is trend on stocks requested that are not available
        logging.error(f"Stock requested is not available, {symbol}")
        return error_response(404, "Stock not found")
    logging.info(f"Calculating dividend yield for {symbol} at price {price}")
    return {
        "dividend_yield": stock.calculate_dividend_yield(price)
    }


@bp.route("/pe_ratio", methods=["GET"])
@numbers_validated(["price"])  # input validation
def pe_ratio():
    symbol = request.args.get("symbol")
    price = int(request.args.get("price", 0))
    stock = stock_market.get_stock(symbol)
    if not stock:
        logging.error(f"Stock requested is not available, {symbol}")
        return error_response(404, "Stock not found")
    logging.info(f"Calculating P/E ratio for {symbol} at price {price}")
    return {
        "pe_ratio": stock.calculate_pe_ratio(price)
    }


@bp.route("/trade", methods=["POST"])
@numbers_validated(["price", "quantity"])  # input validation
@trade_type_validation
def trade():
    data = request.get_json()
    symbol = data.get("symbol")
    quantity = data.get("quantity")
    price = data.get("price")
    trade_type = data.get("type")

    stock = stock_market.get_stock(symbol)
    if not stock:
        logging.error(f"Stock requested is not available, {symbol}")
        return error_response(404, "Stock not found")
    stock_market.trade(symbol, quantity, price, trade_type)
    return {
        "message": f"Traded for {symbol}: {quantity} shares at {price}, type: {trade_type}"
    }


@bp.route("/volume_weighted_price", methods=["GET"])
def volume_weighted_price():
    return {
        "volume_weighted_price": "hello world"
    }


@bp.route("/gbce_index", methods=["GET"])
def gbce_index():
    return {
        "gbce_index": "hello world"
    }
