
import time as time_lib
import pprint
import pathlib
import operator
import pandas as pd

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
    credentials_path=CREDENTIALS_PATH
)

# Create a Portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Define mutliple positions to add.
multi_position = [
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2020-01-31'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'SQ',
        'purchase_date': '2020-01-31'
    }
]

# Grab the New positions
new_positions = trading_robot.portfolio.add_positions(positions=multi_position)
pprint.pprint(new_positions)

# Add a single position
trading_robot_portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10,
    asset_type='equity',
    purchase_date='2020-04-01'
)

# Add another single position
trading_robot_portfolio.add_position(
    symbol='AAPL',
    quantity=10,
    purchase_price=10,
    asset_type='equity',
    purchase_date='2020-04-01'
)

# If the Market is open, print some quotes.
if trading_robot.regular_market_open:
    pprint.pprint(trading_robot.grab_current_quotes())

# If the Post Market is Open, do something.
elif trading_robot.post_market_open:
    pprint.pprint(trading_robot.grab_current_quotes())

# If the Pre Market is Open, do something.
elif trading_robot.pre_market_open:
    pprint.pprint(trading_robot.grab_current_quotes())

# Print the Positions
pprint.pprint(trading_robot_portfolio.positions)

# Grab the current quotes, for all of our positions.
current_quotes = trading_robot.grab_current_quotes()

# Print the Quotes.
pprint.pprint(current_quotes)

# Let's see if our Microsoft Position is profitable.
is_msft_porfitable = trading_robot.portfolio.is_profitable(
    symbol="MSFT",
    current_price=current_quotes['MSFT']['lastPrice']
)
print("Is Microsoft Profitable: {answer}".format(answer=is_msft_porfitable))

# Let's get the projected Market Value.
portfolio_summary = trading_robot.portfolio.projected_market_value(current_prices=current_quotes)
pprint.pprint(portfolio_summary)

# Create a new Trade Object.
new_trade = trading_robot.create_trade(
    trade_id='long_msft',
    enter_or_exit='enter',
    long_or_short='short',
    order_type='lmt',
    price=150.00
)

# Make it Good Till Cancel.
new_trade.good_till_cancel(cancel_time=datetime.now())

# Change the session
new_trade.modify_session(session='am')

# Add an Order Leg.
new_trade.instrument(symbol='MSFT', quantity=2, asset_type='EQUITY')

# Add a Stop Loss Order with the Main Order.
new_trade.add_stop_loss(stop_size=.10, percentage=False)

# Print out the order.
pprint.pprint(new_trade.order)

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
stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'])

# Create an indicator Object.
indicator_client = Indicators(price_data_frame=stock_frame)

# Add the RSI Indicator.
indicator_client.rsi(period=14)

# Add the 200 day simple moving average.
indicator_client.sma(period=200)

# Add the 50 day exponentials moving average.
indicator_client.ema(period=50)

# Add a signal to check for.
indicator_client.set_indicator_signal(
    indicator='rsi',
    buy=40.0,
    sell=20.0,
    condition_buy=operator.ge,
    condition_sell=operator.le
)

# print the frame.
print(stock_frame.frame)

keep_trading = True

while keep_trading:
    
    # Grab a new quote.
    current_quotes = trading_robot.grab_current_quotes()

    # Add to the Stock Frame.
    stock_frame.add_rows(data=current_quotes)

    print(stock_frame.frame)

    # Refresh the Indicators.
    indicator_client.refresh()

    # Check for signals.
    signals = indicator_client.check_signals()

    # Execute Trades.
    trading_robot.execute_signals()

    # Sleep 5 seconds.
    time_lib.sleep(5)
