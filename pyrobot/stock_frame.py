import pandas as pd
from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import Window

from datetime import datetime
from datetime import time
from datetime import timezone

from typing import List
from typing import Dict
from typing import Union


class StockFrame():

    def __init__(self, data: List[Dict]) -> None:
        
        self._data = data
        self._frame: pd.DataFrame = self.create_frame()


    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    # @frame.setter
    # def frame(self, data) -> pd.DataFrame:
    #     self._data = data
    #     self._frame = self.create_frame()


    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        self._symbol_groups: DataFrameGroupBy = self._frame.groupby(by='symbol')
        return self._symbol_groups

    def symbol_groups_windows(self, size: int) -> Window:
        self._symbol_groups_windows: Window = self._symbol_groups.rolling(size)
        return self._symbol_groups_windows


    def create_frame(self) -> pd.DataFrame:      
        
        # Make a data frame.
        price_df = pd.DataFrame(data=self._data)
        price_df = self._parse_datetime_column(price_df=price_df)
        price_df = self._set_multi_index(price_df=price_df)

        return price_df

    def _parse_datetime_column(self, price_df: pd.DataFrame):

        price_df['datetime'] = pd.to_datetime(price_df['datetime'], unit='ms', origin='unix')

        return price_df
    
    def _set_multi_index(self, price_df: pd.DataFrame):

        price_df = price_df.set_index(keys=['symbol','datetime'])

        return price_df
