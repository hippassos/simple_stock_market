from . import stocks


@stocks.route('/list_stocks', methods=['GET'])
def list_stocks():
    return {
        "stocks": ["hello world"]
    }

@stocks.route('/dividend_yield', methods=['GET'])
def dividend_yield():
    return {
        "dividend_yield": "hello world"
    }


@stocks.route('/pe_ratio', methods=['GET'])
def pe_ratio():
    return {
        "pe_ratio": "hello world"
    }

@stocks.route('/trade', methods=['POST'])
def trade():
    return {
        "trade": "hello world"
    }

@stocks.route('/volume_weighted_price', methods=['GET'])
def volume_weighted_price():
    return {
        "volume_weighted_price": "hello world"
    }

@stocks.route('/gbce_index', methods=['GET'])
def gbce_index():
    return {
        "gbce_index": "hello world"
    }
