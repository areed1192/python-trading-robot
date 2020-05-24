"""Unit test module for the StockFrame Object.

Will perform an instance test to make sure it creates it. Additionally,
it will test different properties and methods of the object.
"""

import unittest
import pandas as pd
from unittest import TestCase
from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

from pyrobot.robot import PyRobot
from pyrobot.stock_frame import StockFrame


class PyRobotStockFrameTest(TestCase):

    """Will perform a unit test for the StockFrame Object."""

    def setUp(self) -> None:
        """Set up the Stock Frame."""

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

    def test_frame_property(self):
        """Test that the `frame` property returns a Pandas DataFrame object."""

        self.assertIsInstance(self.stock_frame.frame, pd.DataFrame)
        self.assertIsInstance(self.stock_frame.frame.index, pd.MultiIndex)

    def test_frame_symbols(self):
        """Test that the `frame.index` property contains the specified symbols."""

        self.assertIn('AAPL', self.stock_frame.frame.index)
        self.assertIn('MSFT', self.stock_frame.frame.index)

    def test_symbol_groups_property(self):
        """Test that the `symbol_groups` property returns a Pandas DataFrameGroupBy object."""

        self.assertIsInstance(self.stock_frame.symbol_groups, pd.core.groupby.DataFrameGroupBy)
    
    def test_symbol_rolling_groups_property(self):
        """Test that the `symbol_rolling_groups` property returns a Pandas RollingGroupBy object."""

        self.assertIsInstance(self.stock_frame.symbol_rolling_groups(size=15), pd.core.window.RollingGroupby)

    def test_add_row(self):
        """Test adding a new row to our data frame."""

        # Define a new row.
        new_row_dict = {
            'AAPL':{
                'openPrice':100.00,
                'closePrice':100.00,
                'highPrice':100.00,
                'lowPrice':100.00,
                'askSize':100,
                'bidSize':100,
                'quoteTimeInLong':1586390399572
            }

        }

        # Add the row.
        self.stock_frame.add_rows(data=new_row_dict)

        # Create a timestamp.
        time_stamp_parsed = pd.to_datetime(1586390399572, unit='ms', origin='unix')
        index_tuple = ('AAPL', time_stamp_parsed)

        # Check to see if the Tuple is in the Index.
        self.assertIn(index_tuple, self.stock_frame.frame.index)

    def tearDown(self) -> None:
        """Teardown the StockFrame."""

        self.stock_frame = None


if __name__ == '__main__':
    unittest.main()