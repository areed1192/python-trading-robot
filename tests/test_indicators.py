"""Unit test module for the Indicator Object.

Will perform an instance test to make sure it creates it. Additionally,
it will test different properties and methods of the object.
"""
import unittest
import pandas as pd

from datetime import datetime
from datetime import timedelta
from unittest import TestCase
from configparser import ConfigParser


from pyrobot.robot import PyRobot
from pyrobot.stock_frame import StockFrame


class PyRobotIndicatorTest(TestCase):

    """Will perform a unit test for the Indicator Object."""

    def setUp(self) -> None:
        """Set up the Indicator Client."""

        # Grab configuration values.
        config = ConfigParser()
        config.read('configs/config.ini')       

        CLIENT_ID = config.get('main', 'CLIENT_ID')
        REDIRECT_URI = config.get('main', 'REDIRECT_URI')
        CREDENTIALS_PATH = config.get('main', 'JSON_PATH')

        # Create a robot.
        self.robot = PyRobot(
            client_id = CLIENT_ID, 
            redirect_uri = REDIRECT_URI, 
            credentials_path = CREDENTIALS_PATH
        )

        # Grab historical prices, first define the start date and end date.
        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        # Grab the historical prices.
        historical_prices = self.robot.grab_historical_prices(
            start=end_date,
            end=start_date,
            bar_size=1,
            bar_type='minute',
            symbols=['AAPL','MSFT']
        )

        # Convert data to a Data Frame.
        self.stock_frame = self.robot.create_stock_frame(data=historical_prices['aggregated'])

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a StockFrame."""

        self.assertIsInstance(self.stock_frame, StockFrame)