"""Unit test module for the Azure Session.

Will perform an instanc test to make sure it creates it.
"""

import os
import sys
import pyodbc
import unittest
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

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.robot = None


if __name__ == '__main__':
    unittest.main()