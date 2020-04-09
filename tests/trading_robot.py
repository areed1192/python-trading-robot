
import pprint
from pyrobot.robot import PyRobot
from tests.config import CONSUMER_ID, REDIRECT_URI, JSON_PATH, ACCOUNT_TRADING

# Initalize the robot
trading_robot = PyRobot(consumer_id = CONSUMER_ID, redirect_uri = REDIRECT_URI, json_path = JSON_PATH)

# Create a Portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

# Add a single position
trading_robot_portfolio.add_position(
    symbol = 'MSFT', 
    quantity = 10, 
    purchase_price = 10, 
    asset_type = 'equity',
    purchase_date = '2020-04-01'
)

# Add another single position
trading_robot_portfolio.add_position(
    symbol = 'AAPL', 
    quantity = 10, 
    purchase_price = 10, 
    asset_type = 'equity', 
    purchase_date = '2020-04-01'
)

# Print the Positions
pprint.pprint(trading_robot_portfolio.positions)

# If the Market is open, print some quotes.
if trading_robot.regular_market_open:
    pprint.pprint(trading_robot.grab_current_quotes())

# If the Post Market is Open, do something.
elif trading_robot.post_market_open:
    pprint.pprint(trading_robot.grab_current_quotes())

# If the Pre Market is Open, do something.
elif trading_robot.pre_market_open:
    pprint.pprint(trading_robot.grab_current_quotes())
