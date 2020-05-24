"""Unit test module for the Trade Object.

Will perform an instance test to make sure it creates it. Additionally,
it will test different properties and methods of the object.
"""

import unittest
from unittest import TestCase
from configparser import ConfigParser

from pyrobot.robot import PyRobot
from pyrobot.trades import Trade


class PyRobotTradeTest(TestCase):

    """Will perform a unit test for the Trade object."""

    def setUp(self) -> None:
        """Set up the Trade Object."""

        # Grab configuration values.
        config = ConfigParser()
        config.read('configs/config.ini')       

        CLIENT_ID = config.get('main', 'CLIENT_ID')
        REDIRECT_URI = config.get('main', 'REDIRECT_URI')
        CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
        self.ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

        # Create a new instance of a robot.
        self.robot = PyRobot(
            client_id = CLIENT_ID, 
            redirect_uri = REDIRECT_URI, 
            credentials_path = CREDENTIALS_PATH
        )

    def test_create_new_market_order(self):
        """Create a new market order."""

        # Create a new Trade Object.
        new_trade = self.robot.create_trade(enter_or_exit='enter', long_or_short='short',order_type='mkt')

        self.assertIsInstance(new_trade, Trade)
        self.assertEqual(new_trade.order_type, 'mkt')

    def test_create_new_limit_order(self):
        """Create a new limit order."""

        # Create a new Trade Object.
        new_trade = self.robot.create_trade(enter_or_exit='enter', long_or_short='short',order_type='lmt')

        self.assertIsInstance(new_trade, Trade)
        self.assertEqual(new_trade.order_type, 'lmt')

    def test_create_new_stop_order(self):
        """Create a new stop order."""

        # Create a new Trade Object.
        new_trade = self.robot.create_trade(enter_or_exit='enter', long_or_short='short',order_type='stop')

        self.assertIsInstance(new_trade, Trade)
        self.assertEqual(new_trade.order_type, 'stop')
    
    def test_add_instrument(self):
        """Tests adding an instrument to an order after creating it."""

        # Create a new Trade Object.
        new_trade = self.robot.create_trade(
            enter_or_exit='enter',
            long_or_short='long',
            order_type='lmt',
            price=12.00
        )

        # Define the Order Leg it should be.
        order_leg = {
            "instruction": 'BUY',
            "quantity": 2,
            "instrument": {
                "symbol": 'MSFT',
                "assetType": 'EQUITY'
            }
        }
        
        # Add an instrument to the Trade.
        new_trade.instrument(symbol='MSFT',quantity=2, asset_type='EQUITY')
        self.assertDictEqual(new_trade.order['orderLegCollection'][0], order_leg)

    def test_add_stop_loss_percentage(self):
        """Tests adding a stop Loss Order to an exisiting Limit Order."""
        
        # Create a new Trade Object.
        new_trade = self.robot.create_trade(
            enter_or_exit='enter',
            long_or_short='long',
            order_type='lmt',
            price=12.00
        )

        # Add a new instrument.
        new_trade.instrument(symbol='MSFT',quantity=2, asset_type='EQUITY')

        # Add a new percentage Stop Loss.
        new_trade.add_stop_loss(stop_size=.10, percentage=True)

        stop_loss_order = {
            "orderType": "STOP",
            "session": "NORMAL",
            "duration": "DAY",
            "stopPrice": 10.8,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": 'SELL',
                    "quantity": 2,
                    "instrument": {
                        "symbol": 'MSFT',
                        "assetType": 'EQUITY'
                    }
                }
            ]
        }

        self.assertEqual(new_trade.order_type, 'lmt')
        self.assertIn('childOrderStrategies', new_trade.order)
        self.assertDictEqual(new_trade.stop_loss_order, stop_loss_order)

    def test_add_stop_loss_dollar(self):
        """Tests adding a stop Loss Order to an exisiting Limit Order."""
        
        # Create a new Trade Object.
        new_trade = self.robot.create_trade(
            enter_or_exit='enter',
            long_or_short='long',
            order_type='lmt',
            price=12.00
        )

        # Add a new instrument.
        new_trade.instrument(symbol='MSFT',quantity=2, asset_type='EQUITY')

        # Add a new stop Loss.
        new_trade.add_stop_loss(stop_size=.10, percentage=False)

        stop_loss_order = {
            "orderType": "STOP",
            "session": "NORMAL",
            "duration": "DAY",
            "stopPrice": 11.90,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": 'SELL',
                    "quantity": 2,
                    "instrument": {
                        "symbol": 'MSFT',
                        "assetType": 'EQUITY'
                    }
                }
            ]
        }

        self.assertEqual(new_trade.order_type, 'lmt')
        self.assertIn('childOrderStrategies', new_trade.order)
        self.assertDictEqual(new_trade.stop_loss_order, stop_loss_order)

    # def test_price_calculation(self):
    #     """Tests calculating the new price for Stop Orders."""

    #     new_price = Trade()._calculate_new_price(price=12.00,adjustment=.1, percentage=True)

    def tearDown(self) -> None:
        """Teardown the Robot."""

        self.robot = None

if __name__ == '__main__':
    unittest.main()