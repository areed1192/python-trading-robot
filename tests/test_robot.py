"""Unit test module for the Azure Session.

Will perform an instanc test to make sure it creates it.
"""

import os
import sys
import pyodbc
import unittest
from datetime import datetime
from datetime import timezone
from unittest import TestCase
from configparser import ConfigParser

# Add path to PyRobot.
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
    )
)

from pyrobot.robot import PyRobot
from pyrobot.portfolio import Portfolio
from configparser import ConfigParser


class PyRobotSession(TestCase):

    """Will perform a unit test for the Azure session."""

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

        right_now = datetime.now().replace(tzinfo = timezone.utc).timestamp()
        regular_market_start_time = datetime.now().replace(hour = 14, minute = 30, second = 00, tzinfo = timezone.utc).timestamp()
        regular_market_end_time = datetime.now().replace(hour = 21, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()

        if regular_market_end_time >= right_now >= regular_market_start_time:
            open =  True
        else:
            open = False

        self.assertEqual(open, self.robot.regular_market_open)

        """
        Pre
        09:00
        14:30

        Regular
        14:30
        21:00

        Post
        21:00
        01:00
        """

    def test_pre_market_open(self):
        """Tests whether US Pre-Market is Open"""

        right_now = datetime.now().replace(tzinfo = timezone.utc).timestamp()
        pre_market_start_time = datetime.now().replace(hour = 9, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()
        pre_market_end_time = datetime.now().replace(hour = 14, minute = 30, second = 00, tzinfo = timezone.utc).timestamp()

        if pre_market_end_time >= right_now >= pre_market_start_time:
            open =  True
        else:
            open = False

        self.assertEqual(open, self.robot.pre_market_open)

    def test_post_market_open(self):
        """Tests whether US Post-Market is Open"""

        right_now = datetime.now().replace(tzinfo = timezone.utc).timestamp()
        post_market_start_time = datetime.now().replace(hour = 21, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()
        post_market_end_time = datetime.now().replace(hour = 1, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()

        if post_market_end_time >= right_now >= post_market_start_time:
            open =  True
        else:
            open = False

        self.assertEqual(open, self.robot.post_market_open)

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.robot = None


if __name__ == '__main__':
    unittest.main()