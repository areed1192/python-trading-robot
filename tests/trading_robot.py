
import time as t

from datetime import datetime, time, timezone
from pyrobot.robot import PyRobot
from tests.config import CONSUMER_ID, REDIRECT_URI, JSON_PATH, ACCOUNT_TRADING

# Initalize the robot
trading_robot = PyRobot(consumer_id = CONSUMER_ID, redirect_uri = REDIRECT_URI, json_path = JSON_PATH)

# Create a Portfolio
trading_robot_portfolio = trading_robot.create_portfolio()

postions = [('MSFT', 10), ('AAPL',20), ('AA',10)]

trading_robot_portfolio.add_position(symbol = 'MSFT', quantity = 10, purchase_price = 10, asset_type = 'equity', purchase_date = '2020-04-01')
trading_robot_portfolio.add_position(symbol = 'AAPL', quantity = 10, purchase_price = 10, asset_type = 'equity', purchase_date = '2020-04-01')

print(trading_robot_portfolio.positions)

print(trading_robot.grab_current_quotes())

# print(trading_robot.session)
# print(trading_robot.pre_market_open)
# print(trading_robot.post_market_open)