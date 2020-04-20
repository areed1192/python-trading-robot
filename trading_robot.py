
import pprint
from datetime import datetime
from configparser import ConfigParser
from pyrobot.robot import PyRobot

# Grab configuration values.
config = ConfigParser()
config.read('configs/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

# Initalize the robot
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

# Create a new Trade Object.
new_trade = trading_robot.create_trade(enter_or_exit='enter', long_or_short='short',order_type='stop')

# Make it Good Till Cancel.
new_trade.good_till_cancel(cancel_time=datetime.now())

# Change the session
new_trade.modify_session(session='am')
pprint.pprint(new_trade.order)