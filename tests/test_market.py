import pytest
from app import create_app
from app.stocks.models import Stock, StockMarket, available_stocks
import datetime


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# Test Routes
def test_route_dividend_yield(client):
    # all good
    response = client.get(f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=1")
    assert response.status_code == 200
    # missing stock
    response = client.get("/stocks/dividend_yield?symbol=ACME&price=1")
    assert response.status_code == 404
    # price is float type
    response = client.get(f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=1.1")
    assert response.status_code == 400
    # price is negative
    response = client.get(f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=-1")
    assert response.status_code == 400
    # price is string type
    response = client.get(f"/stocks/dividend_yield?symbol={[*available_stocks.keys()][0]}&price=ArtificialRock")
    assert response.status_code == 400


def test_route_pe_ratio(client):
    # all good
    response = client.get(f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=1")
    assert response.status_code == 200
    # missing stock
    response = client.get("/stocks/pe_ratio?symbol=ACME&price=1")
    assert response.status_code == 404
    # price is float type
    response = client.get(f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=1.1")
    assert response.status_code == 400
    # price is negative
    response = client.get(f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=-1")
    assert response.status_code == 400
    # price is string type
    response = client.get(f"/stocks/pe_ratio?symbol={[*available_stocks.keys()][0]}&price=ArtificialRock")
    assert response.status_code == 400


def test_route_record_trade(client):
    response = client.post("/stocks/trade", json={"symbol": "GIN", "quantity": 10, "price": 100, "type": "buy"})
    assert response.status_code == 200


def test_route_volume_weighted_price(client):
    response = client.get("/stocks/volume_weighted_price?symbol=TEST")
    assert response.status_code == 200


def test_route_gbce_index(client):
    response = client.get("/stocks/gbce_index")
    assert response.status_code == 200


def test_route_list_stocks(client):
    response = client.get("/stocks/list_stocks")
    assert response.status_code == 200


# Test Model Methods
def test_model_method_stock_methods():
    stock = Stock(symbol="TEST", type="Common", last_dividend=10, fixed_dividend=0, par_value=100)
    assert stock.calculate_dividend_yield(100) == 0.1
    assert stock.calculate_pe_ratio(100) == 10


def test_model_method_trade_recording():
    trades = Trades()
    trades.record_trade("TEST", 10, 100, "buy")
    assert len(trades.trades) == 1


def test_model_method_volume_weighted_stock_price():
    trades = Trades()
    trades.record_trade("TEST", 10, 100, "buy")
    assert trades.calculate_volume_weighted_stock_price("TEST") == 100


def test_model_method_gbce_index():
    trades = Trades()
    trades.record_trade("TEST", 10, 100, "buy")
    assert trades.calculate_gbce_all_share_index() > 0


def test_model_method_stock_market():
    stock_market = StockMarket()
    stock = Stock(symbol="TEST", type="Common", last_dividend=10, fixed_dividend=0, par_value=100)
    stock_market.add_stock(stock)
    assert stock_market.get_stock("TEST") is not None
    assert len(stock_market.list_stocks()) == 1


def test_model_method_volume_weighted_stock_price_time_filter():
    trades = Trades()
    trades.record_trade("TEST", 10, 100, "buy")
    old_trade = trades.trades[-1]
    old_trade.timestamp -= datetime.timedelta(minutes=16)  # Make it older than 15 mins
    trades.record_trade("TEST", 5, 200, "buy")

    vwp = trades.calculate_volume_weighted_stock_price("TEST")
    assert vwp == 200  # Only the recent trade should be considered
