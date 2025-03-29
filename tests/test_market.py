import pytest
import datetime
from math import isclose
from app import create_app
from app.stocks.models import Stock, StockMarket, available_stocks


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def stock_market():
    test_available_stocks = {
        "PLANETEXPRESS": Stock("PLANETEXPRESS", "Common", 0, 0, 10),
        "MOMCORP": Stock("MOMCORP", "Common", 10, 0, 100),
        "PANUCCI": Stock("PANUCCI", "Preferred", 4, 0.1, 500),
    }
    return StockMarket([], test_available_stocks)


# Test Routes
# TODO seed the StockMarket though config as currently the route tests
# are reading the StockMarket initiated at models.py instead of the fixture.
def test_route_dividend_yield(client):
    # all good
    response = client.get(
        f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=1"
    )
    assert response.status_code == 200
    # missing stock
    response = client.get("/stocks/dividend_yield?symbol=ACME&price=1")
    assert response.status_code == 404
    # price is float type
    response = client.get(
        f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=1.1"
    )
    assert response.status_code == 400
    # price is negative
    response = client.get(
        f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=-1"
    )
    assert response.status_code == 400
    # price is string type
    response = client.get(
        f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=ArtificialRock"
    )
    assert response.status_code == 400


def test_route_pe_ratio(client):
    # all good
    response = client.get(
        f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=1"
    )
    assert response.status_code == 200
    # missing stock
    response = client.get("/stocks/pe_ratio?symbol=ACME&price=1")
    assert response.status_code == 404
    # price is float type
    response = client.get(
        f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=1.1"
    )
    assert response.status_code == 400
    # price is negative
    response = client.get(
        f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=-1"
    )
    assert response.status_code == 400
    # price is string type
    response = client.get(
        f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=ArtificialRock"
    )
    assert response.status_code == 400


def test_route_trade(client):
    # TODO remove hardcodes symbol
    response = client.post(
        "/stocks/trade",
        json={"symbol": "GIN", "quantity": 10, "price": 100, "type": "buy"},
    )
    assert response.status_code == 200


def test_route_volume_weighted_price(client):
    response = client.get(
        f"/stocks/volume_weighted_price?symbol={[*available_stocks.keys()][0]}"
    )
    assert response.status_code == 200


def test_route_gbce_index(client):
    response = client.get("/stocks/gbce_index")
    assert response.status_code == 200


def test_route_list_stocks(client):
    response = client.get("/stocks/list_stocks")
    assert response.status_code == 200


def test_route_list_trades(client):
    response = client.get("/stocks/list_trades")
    assert response.status_code == 200


# Test Model Methods
def test_model_method_stock_methods():
    stock = Stock(
        symbol="TEST", type="Common", last_dividend=10, fixed_dividend=0, par_value=100
    )
    assert stock.calculate_dividend_yield(100) == 0.1  # last_dividend / price
    assert stock.calculate_pe_ratio(100) == 10

    pstock = Stock(symbol="TEST", type="Preferred", last_dividend=10, fixed_dividend=0.02, par_value=100)
    price = 50
    pexpected_yield = (0.02 * 100) / 50  # (fixed_dividend * par_value) / price
    assert pstock.calculate_dividend_yield(price) == pexpected_yield


def test_model_method_trade(stock_market):
    assert len(stock_market.trades) == 0
    stock_market.trade("TEST", 10, 100, "buy")
    assert len(stock_market.trades) == 1


def test_model_method_gbce_index(stock_market):
    stock_market.trade("TEST", 10, 27, "buy")
    stock_market.trade("TEST", 10, 125, "buy")
    stock_market.trade("TEST", 10, 8, "buy")
    gbce_idx = stock_market.calculate_gbce_all_share_index()
    assert gbce_idx > 0
    assert isclose(gbce_idx, 30.0)


def test_model_method_add_stock():
    stock_market = StockMarket()
    stock = Stock(
        symbol="TEST", type="Common", last_dividend=10, fixed_dividend=0, par_value=100
    )
    stock_market.add_stock(stock)
    assert stock_market.get_stock("TEST") is not None
    assert len(stock_market.list_stocks()) == 1


def test_model_method_volume_weighted_stock_price(stock_market):
    stock_market.trade("TEST", 8, 100, "buy")
    stock_market.trade("TEST", 2, 50, "buy")
    assert isclose(stock_market.calculate_volume_weighted_stock_price("TEST"), 90.0)


def test_model_method_volume_weighted_stock_price_time_filter(stock_market):
    stock_market.trade("NOTTEST", 10, 42, "buy")
    stock_market.trade("TEST", 10, 100, "buy")
    old_trade = stock_market.trades[-1]
    old_trade.timestamp -= datetime.timedelta(minutes=16)  # Make it older than 15 mins
    stock_market.trade("TEST", 5, 200, "buy")

    vwp = stock_market.calculate_volume_weighted_stock_price("TEST")
    assert vwp == 200  # Only the recent trade should be considered
