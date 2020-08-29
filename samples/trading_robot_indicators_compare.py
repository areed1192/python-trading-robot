import pprint
import operator

from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators

# Grab configuration values.
config = ConfigParser()
config.read('configs/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

# Initalize the robot.
trading_robot = PyRobot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH,
    paper_trading=True
)

# Create a Portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Add a single position
trading_robot_portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10,
    asset_type='equity',
    purchase_date='2020-04-01'
)

# Grab historical prices, first define the start date and end date.
start_date = datetime.today()
end_date = start_date - timedelta(days=30)

# Grab the historical prices.
historical_prices = trading_robot.grab_historical_prices(
    start=end_date,
    end=start_date,
    bar_size=1,
    bar_type='minute'
)

# Convert data to a Data Frame.
stock_frame = trading_robot.create_stock_frame(
    data=historical_prices['aggregated']
)

# We can also add the stock frame to the Portfolio object.
trading_robot.portfolio.stock_frame = stock_frame

# Additionally the historical prices can be set as well.
trading_robot.portfolio.historical_prices = historical_prices

# Create an indicator Object.
indicator_client = Indicators(price_data_frame=stock_frame)

# Add the RSI Indicator.
indicator_client.rsi(period=14)

# Add the 200 day simple moving average.
indicator_client.sma(period=200)

# Add the 50 day exponentials moving average.
indicator_client.ema(period=50)

# Add the Bollinger Bands.
indicator_client.bollinger_bands(period=20)

# Add the Rate of Change.
indicator_client.rate_of_change(period=1)

# Add the Average True Range.
indicator_client.average_true_range(period=14)

# Add the Stochastic Oscillator.
indicator_client.stochastic_oscillator()

# Add the MACD.
indicator_client.macd(fast_period=12, slow_period=26)

# Add the Mass Index.
indicator_client.mass_index(period=9)

# Add a signal to check for.
indicator_client.set_indicator_signal_compare(
    indicator_1='sma',
    indicator_2='ema',
    condition_buy=operator.ge,
    condition_sell=None
)

# Check for signals.
signals = indicator_client.check_signals()

# Print the Head.
print(trading_robot.stock_frame.frame.head())

# Print the Signals.
pprint.pprint(signals)
