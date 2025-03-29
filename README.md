# Flask Stock Trading Application

This is a Flask-based stock trading application that follows the application factory pattern and uses blueprints. It includes:

- **Unit tests** with `pytest`
- **Linting & formatting** using `flake8` and `black`
- **Logging**
- **Docker support**
- **Input validations**

## Features

- **Calculate Dividend Yield**: For a given stock and price, computes the dividend yield.
- **Calculate P/E Ratio**: For a given stock and price, computes the Price-to-Earnings Ratio.
- **Trade stocks**: Records trades with timestamp, quantity, type (buy/sell), and price.
- **Volume Weighted Stock Price**: For a given stock, calculates the VWAP for trades in the past 15 minutes.
- **GBCE All Share Index**: Computes the geometric mean of all stock prices in the ledger.

## Installation & Setup

### Prerequisites
- Python 3.8+
- Docker (optional)
- Tested only with Ubuntu 20.04/22.04 and WSL2, windows should work since there are no obvious operations invoking os.fork() but it is not tested

### Setup & Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/simple_stock_market.git
   cd simple_stock_market
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements/dev.txt
   ```
4. Run the application:
   ```bash
   flask run
   ```

### Run with Docker
1. Build the Docker image:
   ```bash
   docker build -t simple-stock-market .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 simple-stock-market
   ```

## Running Tests & Coverage reporting
To get the coverage report and execute tests using `pytest`:
```bash
coverage run -m pytest tests -v && coverage report -m
```
### Test with Docker
1. Build the Docker image:
    ```bash
    docker build -t simple-stock-market-test -f Dockerfile.test .
    ```
2. Run the container:
    ```bash
    docker run --rm simple-stock-market-test
    ```

## Linting & Code Formatting
- Run `flake8` for linting:
  ```bash
  flake8 .
  ```
- Run `black` for formatting:
  ```bash
  black .
  ```

## Default Base URL
```
http://localhost:5000
```

## API Endpoints

### List all stocks
#### Endpoint:
```
GET /stocks/list_stocks
```
#### **Description:**
Returns a list of all available stocks in the market.

#### Response:
```json
{
    "stocks": [
        {
            "fixed_dividend": 0,
            "last_dividend": 0,
            "par_value": 100,
            "symbol": "TEA",
            "type": "Common"
        },
        ...
    ]
}
```

### List all trades
#### Endpoint:
```
GET /stocks/list_trades
```
#### **Description:**
Returns a list of all recorded trades.

#### Response:
```json
{
    "trades": [
        {
            "price": 41,
            "quantity": 2,
            "symbol": "ALE",
            "timestamp": "Sat, 29 Mar 2025 22:01:58 GMT",
            "trade_type": "buy"
        },
        ...
    ]
}
```

### Calculate Dividend Yield
#### Endpoint:
```
GET /stocks/dividend_yield?symbol=<symbol>&price=<price>
```
#### **Description:**
Calculates the dividend yield for a given stock and price.
#### **Parameters:**
- `symbol` (string, required): Stock symbol.
- `price` (integer, required): Stock price in pennies.

#### Response:
```json
{
    "dividend_yield": 0.05
}
```

### Calculate PE Ration
#### Endpoint:
```
GET /stocks/pe_ratio?symbol=<symbol>&price=<price>
```
#### **Description:**
Calculates the Price-to-Earnings (P/E) Ratio for a given stock and price.
#### **Parameters:**
- `symbol` (string, required): Stock symbol.
- `price` (integer, required): Stock price in pennies.

#### Response:
```json
{
    "pe_ratio": 30
}
```

### Trade
#### Endpoint:
```
POST /stocks//trade
```
#### **Description:**
Records a new trade with details.
#### **Request Body:**
```json
{
    "symbol": "ALE",
    "quantity": 2,
    "price": 41,
    "type": "buy"
}
```

#### Response:
```json
{
    "message": "Traded for ALE: 2 shares at 41, type: buy"
}
```

### Calculate Volume Weighted Stock Price
#### Endpoint:
```
GET /stocks/volume_weighted_price?symbol=<symbol>
```
#### **Description:**
Calculates the volume-weighted stock price based on trades in the past 15 minutes.
#### **Parameters:**
- `symbol` (string, required): Stock symbol.

#### Response:
```json
{
    "volume_weighted_price": 152.3
}
```

### Calculate GBCE All Share Index
#### Endpoint:
```
GET /stocks/gbce_index
```
#### **Description:**
Calculates the GBCE All Share Index using the geometric mean of all stock prices.

#### Response:
```json
{
    "gbce_index": 140.2
}
```

## Error Handling
The following format of responses are generated when it is required
```json
{
    "code": 404,
    "error": "Not Found",
    "message": "Stock requested is not available"
}
```

## License
This project is licensed under the MIT License.
