"""Unit test module for the PyRobot Object.

Will perform an instance test to make sure it creates it. Additionally,
it will test different properties and methods of the object.
"""

import unittest
import pprint

from unittest import TestCase
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from configparser import ConfigParser

from pyrobot.trades import Trade
from pyrobot.robot import PyRobot
from pyrobot.portfolio import Portfolio
from pyrobot.stock_frame import StockFrame


class PyRobotTest(TestCase):

    """Will perform a unit test for the PyRobot Object."""

    def setUp(self) -> None:
        """Set up the Robot."""

        # Grab configuration values.
        config = ConfigParser()
        config.read('configs/config.ini')       

        CLIENT_ID = config.get('main', 'CLIENT_ID')
        REDIRECT_URI = config.get('main', 'REDIRECT_URI')
        CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
        self.ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

        self.robot = PyRobot(
            client_id = CLIENT_ID, 
            redirect_uri = REDIRECT_URI, 
            credentials_path = CREDENTIALS_PATH
        )

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a robot."""

        self.assertIsInstance(self.robot, PyRobot)

    def test_create_portofolio(self):
        """Call `create_portfolio` and make sure it's a Portfolio."""

        new_portfolio = self.robot.create_portfolio()

        self.assertIsInstance(new_portfolio, Portfolio)


    def test_regular_market_open(self):
        """Tests whether Market is Open"""

        # Define right now.
        right_now = datetime.utcnow().timestamp()

        # Define the start time.
        regular_market_start_time = datetime.utcnow().replace(
            hour=14,
            minute=30,
            second=00
        ).timestamp()

        # Define the end time.
        regular_market_end_time = datetime.utcnow().replace(
            hour=21,
            minute=00,
            second=00
        ).timestamp()

        if regular_market_end_time >= right_now >= regular_market_start_time:
            open =  True
        else:
            open = False

        self.assertEqual(open, self.robot.regular_market_open)


    def test_pre_market_open(self):
        """Tests whether US Pre-Market is Open"""

        # Define right now.
        right_now = datetime.utcnow().timestamp()

        # Define the start time.
        pre_market_start_time = datetime.utcnow().replace(
            hour=9,
            minute=00,
            second=00
        ).timestamp()

        # Define the end time.
        pre_market_end_time = datetime.utcnow().replace(
            hour=14,
            minute=30,
            second=00
        ).timestamp()

        if pre_market_end_time >= right_now >= pre_market_start_time:
            open =  True
        else:
            open = False

        self.assertEqual(open, self.robot.pre_market_open)

    def test_post_market_open(self):
        """Tests whether US Post-Market is Open"""

        # Define right now.
        right_now = datetime.utcnow().timestamp()

        # Define the start time.
        post_market_start_time = datetime.utcnow().replace(
            hour=21,
            minute=00,
            second=00
        ).timestamp()

        # Define the end time.
        post_market_end_time = datetime.utcnow().replace(
            hour=1,
            minute=30,
            second=00
        ).timestamp()

        if post_market_end_time >= right_now >= post_market_start_time:
            open = True
        else:
            open = False

        self.assertEqual(open, self.robot.post_market_open)

    def test_historical_prices(self):
        """Tests Grabbing historical prices."""

        # Grab historical prices, first define the start date and end date.
        start_date = datetime.today()
        end_date = start_date - timedelta(days=30)

        # Grab the historical prices.
        self.robot.grab_historical_prices(
            start=end_date,
            end=start_date,
            bar_size=1,
            bar_type='minute',
            symbols=['AAPL']
        )

        self.assertIn('aggregated', self.robot.historical_prices)

    def test_build_portfolio(self):
        """Test building a Portfolio object."""

        # Create a Portfolio
        porfolio_obj = self.robot.create_portfolio()

        self.assertIsInstance(porfolio_obj, Portfolio)

    def test_build_trade(self):
        """Test building a Trade object."""

        # Create a Trade
        trade_obj = self.robot.create_trade(
            trade_id='long_msft',
            enter_or_exit='enter',
            long_or_short='short',
            order_type='lmt',
            price=150.00
        )

        self.assertIsInstance(trade_obj, Trade)

    def test_grab_accounts(self):
        """Test grabbing accounts using the robot."""

        accounts = self.robot.get_accounts(all_accounts=True)

        pprint.pprint(accounts)

        self.assertIsInstance(accounts, list)

    def test_grab_positions(self):
        """Test grabbing positions using the robot."""

        positions = self.robot.get_positions(all_accounts=True)

        pprint.pprint(positions)

        self.assertIsInstance(positions, list)

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.robot = None


if __name__ == '__main__':
    unittest.main()