"""Unit test module for the Portfolio Object.

Will perform an instance test to make sure it creates it. Additionally,
it will test different properties and methods of the object.
"""

import unittest
from unittest import TestCase
from configparser import ConfigParser

from pyrobot.portfolio import Portfolio
from td.client import TDClient


class PyRobotPortfolioTest(TestCase):

    """Will perform a unit test for the Portfolio object."""

    def setUp(self) -> None:
        """Set up the Portfolio."""

        self.portfolio = Portfolio()
        self.maxDiff = None

                # Grab configuration values.
        config = ConfigParser()
        config.read('configs/config.ini')       

        CLIENT_ID = config.get('main', 'CLIENT_ID')
        REDIRECT_URI = config.get('main', 'REDIRECT_URI')
        CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
        self.ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

        self.td_client = TDClient(
            client_id=CLIENT_ID,
            redirect_uri=REDIRECT_URI,
            credentials_path=CREDENTIALS_PATH
        )

        self.td_client.login()

    def test_create_portofolio(self):
        """Make sure it's a Portfolio."""

        self.assertIsInstance(self.portfolio, Portfolio)

    def test_td_client_property(self):
        """Test the TD Client property."""

        # Should be None if wasn't initalized from the PyRobot.
        self.assertIsNone(self.portfolio.td_client)
    
    def test_stock_frame_property(self):
        """Test the Stock Frame property."""

        # Should be None if wasn't initalized from the PyRobot.
        self.assertIsNone(self.portfolio.stock_frame)        

    def test_historical_prices_property(self):
        """Test the Historical Prices property."""

        # Should be False if wasn't initalized from the PyRobot.
        self.assertFalse(self.portfolio.historical_prices)  

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
            'ownership_status': True, 
            'quantity': 10, 
            'purchase_price': 3.00,
            'purchase_date': '2020-01-31'
        }

        self.assertDictEqual(new_position, correct_position)

    def test_add_position_default_arguments(self):
        """Test adding a single position to the portfolio, no date."""

        new_position = self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity'
        )

        correct_position = {
            'symbol': 'MSFT',
            'asset_type': 'equity',
            'ownership_status': False, 
            'quantity': 0, 
            'purchase_price': 0.00,
            'purchase_date': None
        }

        self.assertDictEqual(new_position, correct_position)

    def test_delete_existing_position(self):
        """Test deleting an exisiting position."""

        self.portfolio.add_position(
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

        self.portfolio.add_position(
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

    def test_is_profitable(self):
        """Checks to see if a position is profitable."""

        # Add a position.
        self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        # Test for being Profitable.
        is_profitable = self.portfolio.is_profitable(
            symbol='MSFT',
            current_price=5.00
        
        )

        # Test for not being profitable.
        is_not_profitable = self.portfolio.is_profitable(
            symbol='MSFT',
            current_price=1.00
        )
        
        self.assertTrue(is_profitable)
        self.assertFalse(is_not_profitable)

    def test_projected_market_value(self):
        """Tests the generation of a market value summary, for all of the positions."""

        # Add a position.
        self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        correct_dict = {
            'MSFT': {
                'current_price': 5.0,
                'is_profitable': True,
                'purchase_price': 3.0,
                'quantity': 10,
                'total_invested_capital': 30.0,
                'total_loss_or_gain_$': 20.0,
                'total_loss_or_gain_%': 0.6667,
                'total_market_value': 50.0
            },
            'total': {
                'number_of_breakeven_positions': 0,
                'number_of_non_profitable_positions': 0,
                'number_of_profitable_positions': 1,
                'total_invested_capital': 30.0,
                'total_market_value': 50.0,
                'total_positions': 1,
                'total_profit_or_loss': 20.0
            }
        }

        portfolio_summary = self.portfolio.projected_market_value(current_prices={'MSFT':{'lastPrice':5.0}})
        self.assertDictEqual(correct_dict, portfolio_summary)

    def test_grab_historical_prices(self):
        pass

    def test_portfolio_summary(self):
        """Tests the generation of a portfolio summary, for all of the positions."""

        # Add a position.
        self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        self.portfolio.td_client = self.td_client

        correct_dict = [
            'projected_market_value',
            'portfolio_weights',
            'portfolio_risk'
        ]

        correct_dict = set(correct_dict)

        summary_dict = self.portfolio.portfolio_summary()

        self.assertTrue(correct_dict.issubset(summary_dict))    

    def test_ownership_status(self):
        """Tests getting and setting the ownership status."""

        # Add a position.
        self.portfolio.add_position(
            symbol='MSFT',
            asset_type='equity',
            quantity=10,
            purchase_price=3.00,
            purchase_date='2020-01-31'
        )

        # Should be True, since `purchase_date` was set.
        self.assertTrue(self.portfolio.get_ownership_status(symbol='MSFT'))

        # Reassign it.
        self.portfolio.set_ownership_status(symbol='MSFT', ownership=False)

        # Should be False.
        self.assertFalse(self.portfolio.get_ownership_status(symbol='MSFT'))


    def tearDown(self) -> None:
        """Teardown the Portfolio object."""

        self.portfolio = None


if __name__ == '__main__':
    unittest.main()