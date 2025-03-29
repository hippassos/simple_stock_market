import logging
from app.stocks import bp
from flask import request
from app.stocks.models import stock_market
from app.stocks.decorators import numbers_validated, trade_type_validation, symbol_validation


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
@symbol_validation
def dividend_yield():
    symbol = request.args.get("symbol")
    price = int(request.args.get("price", 0))
    stock = stock_market.get_stock(symbol)
    return {
        "dividend_yield": stock.calculate_dividend_yield(price)
    }


@bp.route("/pe_ratio", methods=["GET"])
@numbers_validated(["price"])  # input validation
@symbol_validation
def pe_ratio():
    symbol = request.args.get("symbol")
    price = int(request.args.get("price", 0))
    stock = stock_market.get_stock(symbol)
    return {
        "pe_ratio": stock.calculate_pe_ratio(price)
    }


@bp.route("/trade", methods=["POST"])
@numbers_validated(["price", "quantity"])  # input validation
@trade_type_validation
@symbol_validation
def trade():
    data = request.get_json()
    symbol = data.get("symbol")
    quantity = data.get("quantity")
    price = data.get("price")
    trade_type = data.get("type")

    stock_market.trade(symbol, quantity, price, trade_type)
    return {
        "message": f"Traded for {symbol}: {quantity} shares at {price}, type: {trade_type}"
    }


@bp.route("/volume_weighted_price", methods=["GET"])
@symbol_validation
def volume_weighted_price():
    symbol = request.args.get('symbol')
    vwp = stock_market.calculate_volume_weighted_stock_price(symbol)
    return {
        "volume_weighted_price": vwp
    }


@bp.route("/gbce_index", methods=["GET"])
def gbce_index():
    return {
        "gbce_index": "hello world"
    }
