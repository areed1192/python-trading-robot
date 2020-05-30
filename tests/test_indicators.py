"""Unit test module for the Indicator Object.

Will perform an instance test to make sure it creates it. Additionally,
it will test different properties and methods of the object.
"""
import unittest
import operator
import pandas as pd

from unittest import TestCase
from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser


from pyrobot.robot import PyRobot
from pyrobot.indicators import Indicators
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

        # Create the indicator client.
        self.indicator_client = Indicators(price_data_frame=self.stock_frame)

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a StockFrame."""

        self.assertIsInstance(self.stock_frame, StockFrame)
        self.assertIsInstance(self.indicator_client, Indicators)
    
    def test_price_frame_data_property(self):
        """Test getting the Price Data Frame."""

        self.assertIsNotNone(self.indicator_client.price_data_frame)

    def test_is_multi_index_property(self):
        """Test getting the Price Data Frame."""

        self.assertTrue(self.indicator_client.is_multi_index)

    def test_change_in_price(self):
        """Test adding the Change in Price."""
        
        # Create the Change in Price indicator.
        self.indicator_client.change_in_price()

        # Check if we have the column.
        self.assertIn('change_in_price', self.stock_frame.frame.columns)

        # And that it's not empty.
        self.assertFalse(self.stock_frame.frame['change_in_price'].empty)

    def test_rsi(self):
        """Test adding the Relative Strength Index."""
        
        # Create the RSI indicator.
        self.indicator_client.rsi(period=14)

        # Check if we have the column.
        self.assertIn('rsi', self.stock_frame.frame.columns)

        # And that it's not empty.
        self.assertFalse(self.stock_frame.frame['rsi'].empty)

    def test_sma(self):
        """Test adding the Simple Moving Average."""
        
        # Create the SMA indicator.
        self.indicator_client.sma(period=200)

        # Check if we have the column.
        self.assertIn('sma', self.stock_frame.frame.columns)

        # And that it's not empty.
        self.assertFalse(self.stock_frame.frame['sma'].empty)

    def test_ema(self):
        """Test adding the Exponential Moving Average."""
        
        # Create the EMA indicator.
        self.indicator_client.ema(period=50)

        # Check if we have the column.
        self.assertIn('ema', self.stock_frame.frame.columns)

        # And that it's not empty.
        self.assertFalse(self.stock_frame.frame['ema'].empty)

    def test_indicator_exist(self):
        """Test checkinf if an indicator column exist."""
        
        # Create the EMA indicator.
        self.indicator_client.ema(period=50)

        # Check if we have the column.
        self.assertIn('ema', self.stock_frame.frame.columns)

        # And that it's not empty.
        self.assertTrue(self.stock_frame.do_indicator_exist(column_names=['ema']))

    def test_indicator_signal(self):
        """Test checkinf if an indicator column exist."""
        
        # Create the EMA indicator.
        self.indicator_client.ema(period=50)

        self.indicator_client.set_indicator_signal(
            indicator='sma',
            buy=50.0,
            sell=30.0,
            condition_buy=operator.ge,
            condition_sell=operator.le
        )

        func_1 = operator.ge
        func_2 = operator.le

        correct_dict = {
            'buy': 50.0,
            'sell': 30.0,
            'buy_operator': func_1,
            'sell_operator': func_2
        }

        correct_dict_all = {
            'sma':{
                'buy': 50.0,
                'sell': 30.0,
                'buy_operator': func_1,
                'sell_operator': func_2
            }
        }


        # And that it's not empty.
        self.assertDictEqual(
            self.indicator_client.get_indicator_signal(indicator='sma'),
            correct_dict
        )

        # And that it's not empty.
        self.assertDictEqual(
            self.indicator_client.get_indicator_signal(),
            correct_dict_all
        )

    def tearDown(self) -> None:
        """Teardown the Indicator object."""

        self.stock_frame = None
        self.indicator_client = None


if __name__ == '__main__':
    unittest.main()