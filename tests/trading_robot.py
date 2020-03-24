from pyrobot.robot import PyRobot
from config import ACCOUNT_USERNAME, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, JSON_PATH

trading_robot = PyRobot(account_username = ACCOUNT_USERNAME, account_password = ACCOUNT_PASSWORD, consumer_id = CONSUMER_ID, redirect_uri = REDIRECT_URI, json_path = JSON_PATH)

print(trading_robot.session)