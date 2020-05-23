import numpy as np
import pandas as pd

from typing import Tuple
from typing import List
from typing import Iterable

from pyrobot.stock_frame import StockFrame


class Indicators():
    

    def __init__(self, price_data_frame: StockFrame) -> None:
        """Initalizes the Indicator Client.

        Arguments:
        ----
        price_data_frame {pyrobot.StockFrame} -- The price data frame which is used to add indicators to.
            At a minimum this data frame must have the following columns: `['timestamp','close','open','high','low']`.
        
        Usage:
        ----
            >>> historical_prices_df = trading_robot.grab_historical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
            )
            >>> price_data_frame = pd.DataFrame(data=historical_prices)
            >>> indicator_client = Indicators(price_data_frame=price_data_frame)
            >>> price_data_frame_indicators = indicator_client.price_data_frame
        """

        self._price_data_frame: StockFrame = price_data_frame
        self._price_groups = self._price_data_frame.symbol_groups
        
        if self.is_multi_index:
            True

    @property
    def price_data_frame(self) -> pd.DataFrame:
        return self._price_data_frame.frame

    @price_data_frame.setter
    def price_data_frame(self, price_data_frame):
        self._price_data_frame = price_data_frame

    @price_data_frame.deleter
    def price_data_frame(self):
        del self._price_data_frame

    @property
    def is_multi_index(self):
        if isinstance(self._price_data_frame.frame.index, pd.MultiIndex):
            return True
        else:
            return False

    def change_in_price(self) -> pd.DataFrame:
        """Calculates the Change in Price.

        Returns:
        ----
        pd.DataFrame -- A data frame with the Change in Price.
        """        

        self._price_data_frame.frame['change_in_price'] = self._price_data_frame.frame.groupby(
            by='symbol',
            as_index=False
        )['close'].transform(
            lambda x: x.diff()
        )

    def rsi(self, period: int, method: str = 'wilders') -> pd.DataFrame:
        """Calculates the Relative Strength Index (RSI).

        Arguments:
        ----
        period {int} -- The number of periods to use to calculate the RSI.

        Keyword Arguments:
        ----
        method {str} -- The calculation methodology. (default: {'wilders'})

        Returns:
        ----
        pd.DataFrame -- A Pandas data frame with the RSI indicator included.

        Usage:
        ----
            >>> historical_prices_df = trading_robot.grab_historical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
            )
            >>> price_data_frame = pd.DataFrame(data=historical_prices)
            >>> indicator_client = Indicators(price_data_frame=price_data_frame)
            >>> indicator_client.rsi(period=14)
            >>> price_data_frame = inidcator_client.price_data_frame
        """

        # Define the price data frame.
        price_frame = self._price_data_frame.frame

        # First calculate the Change in Price.
        if 'change_in_price' not in price_frame.columns:
            self.change_in_price()

        # Define the up days.
        price_frame['up_day'] = price_frame.groupby(
            by='symbol',
            as_index=False
        )['change_in_price'].transform(lambda x : np.where(x >= 0, x, 0))

        # Define the down days.
        price_frame['down_day'] = price_frame.groupby(
            by='symbol',
            as_index=False
        )['change_in_price'].transform(lambda x : np.where(x < 0, x.abs(), 0))

        # Calculate the EWMA (Exponential Weighted Moving Average), meaning older values are given less weight compared to newer values.
        price_frame['ewma_up'] = price_frame.groupby('symbol')['up_day'].transform(lambda x: x.ewm(span = period).mean())
        price_frame['ewma_down'] = price_frame.groupby('symbol')['down_day'].transform(lambda x: x.ewm(span = period).mean())

        # Calculate the Relative Strength
        relative_strength = price_frame['ewma_up'] / price_frame['ewma_down']

        # Calculate the Relative Strength Index
        relative_strength_index = 100.0 - (100.0 / (1.0 + relative_strength))

        # Add the info to the data frame.
        price_frame['rsi'] = np.where(relative_strength_index == 0, 100, 100 - (100 / (1 + relative_strength_index)))

        # Clean up before sending back.
        price_frame.drop(labels=['ewma_up', 'ewma_down', 'down_day', 'up_day', 'change_in_price'], axis=1, inplace=True)

        # Reassign?
        # self.price_data_frame(price_frame)

        return price_frame

    def sma(self, period: int) -> pd.DataFrame:
        """Calculates the Simple Moving Average (SMA).

        Arguments:
        ----
        period {int} -- The number of periods to use when calculating the SMA.

        Returns:
        ----
        pd.DataFrame -- A Pandas data frame with the SMA indicator included.

        Usage:
        ----
            >>> historical_prices_df = trading_robot.grab_historical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
            )
            >>> price_data_frame = pd.DataFrame(data=historical_prices)
            >>> indicator_client = Indicators(price_data_frame=price_data_frame)
            >>> indicator_client.sma(period=100)
            >>> price_data_frame = inidcator_client.price_data_frame
        """
        
        # Grab the Price Frame.
        price_frame = self._price_data_frame.frame

        # Add the SMA
        price_frame['sma'] = price_frame.groupby('symbol')['close'].transform(lambda x: x.rolling(window=period).mean())

        return price_frame

    def ema(self, period: int, alpha: float = 0.0) -> pd.DataFrame:
        """Calculates the Exponential Moving Average (EMA).

        Arguments:
        ----
        period {int} -- The number of periods to use when calculating the EMA.

        Returns:
        ----
        pd.DataFrame -- A Pandas data frame with the EMA indicator included.

        Usage:
        ----
            >>> historical_prices_df = trading_robot.grab_historical_prices(
                start=start_date,
                end=end_date,
                bar_size=1,
                bar_type='minute'
            )
            >>> price_data_frame = pd.DataFrame(data=historical_prices)
            >>> indicator_client = Indicators(price_data_frame=price_data_frame)
            >>> indicator_client.ema(period=50)
            >>> price_data_frame = inidcator_client.price_data_frame
        """

        # Grab the Price Frame.
        price_frame = self._price_data_frame.frame

        # Add the EMA
        price_frame['ema'] = price_frame.groupby('symbol', sort=True)['close'].transform(
            lambda x: x.ewm(span=period).mean()
        )

        return price_frame
