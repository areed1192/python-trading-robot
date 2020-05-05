"""Unit test module for the Azure Session.

Will perform an instanc test to make sure it creates it.
"""

import os
import sys
import pyodbc
import unittest
from unittest import TestCase
from configparser import ConfigParser

from pyrobot.robot import PyRobot
from pyrobot.portfolio import Portfolio
from configparser import ConfigParser


class PyRobotSession(TestCase):

    """Will perform a unit test for the Azure session."""

    def setUp(self) -> None:
        """Set up the Robot."""

        self.portfolio = Portfolio()

    def test_create_portofolio(self):
        """Make sure it's a Portfolio."""

        self.assertIsInstance(self.portfolio, Portfolio)

    def test_add_position(self):
        """Test adding a single position to the portfolio."""

        new_position = self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        correct_position = {
            'symbol': 'MSFT',
            'asset_type': 'equity', 
            'quantity': 10, 
            'purchase_price': 3.00,
            'purchase_date': '2020-01-31'
        }

        self.assertDictEqual(new_position, correct_position)

    def test_add_position_default_arguments(self):
        """Test adding a single position to the portfolio, no date."""

        new_position = self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
        )

        correct_position = {
            'symbol': 'MSFT',
            'asset_type': 'equity', 
            'quantity': 0, 
            'purchase_price': 0.00,
            'purchase_date': None
        }

        self.assertDictEqual(new_position, correct_position)

    def test_delete_existing_position(self):
        """Test deleting an exisiting position."""

        new_position = self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        delete_status = self.portfolio.remove_position(symbol='MSFT')
        correct_status = (True, 'MSFT was successfully removed.')

        self.assertTupleEqual(delete_status, correct_status)

    def test_delete_non_existing_position(self):
        """Test deleting a non-exisiting position."""

        delete_status = self.portfolio.remove_position(symbol='AAPL')
        correct_status = (False, 'AAPL did not exist in the porfolio.')

        self.assertTupleEqual(delete_status, correct_status)
    
    def test_in_portfolio_exisitng(self):
        """Checks to see if an exisiting position exists."""

        new_position = self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        in_portfolio_flag = self.portfolio.in_portfolio(symbol='MSFT')
        self.assertTrue(in_portfolio_flag)
    
    def test_in_portfolio_non_exisitng(self):
        """Checks to see if a non exisiting position exists."""

        in_portfolio_flag = self.portfolio.in_portfolio(symbol='AAPL')
        self.assertFalse(in_portfolio_flag)

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.robot = None


if __name__ == '__main__':
    unittest.main()