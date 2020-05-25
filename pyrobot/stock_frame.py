import numpy as np
import pandas as pd

from datetime import time
from datetime import datetime
from datetime import timezone

from typing import List
from typing import Dict
from typing import Union

from pandas.core.groupby import DataFrameGroupBy
from pandas.core.window import RollingGroupby
from pandas.core.window import Window


class StockFrame():

    def __init__(self, data: List[Dict]) -> None:
        """Initalizes the Stock Data Frame Object.

        Arguments:
        ----
        data {List[Dict]} -- The data to convert to a frame. Normally, this is 
            returned from the historical prices endpoint.
        """        
        
        self._data = data
        self._frame: pd.DataFrame = self.create_frame()
        self._symbol_groups = None
        self._symbol_rolling_groups = None

    @property
    def frame(self) -> pd.DataFrame:
        """The frame object.

        Returns:
        ----
        pd.DataFrame -- A pandas data frame with the price data.
        """        
        return self._frame

    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        """Returns the Groups in the StockFrame.

        Overview:
        ----
        Often we will want to apply operations to a each symbol. The
        `symbols_groups` property will return the dataframe grouped by
        each symbol.

        Returns:
        ----
        {DataFrameGroupBy} -- A `pandas.core.groupby.GroupBy` object with each symbol.
        """  

        # Group by Symbol.   
        self._symbol_groups: DataFrameGroupBy = self._frame.groupby(
            by='symbol',
            as_index=False,
            sort=True
        )

        return self._symbol_groups

    def symbol_rolling_groups(self, size: int) -> RollingGroupby:
        """Grabs the windows for each group.

        Arguments:
        ----
        size {int} -- The size of the window.

        Returns:
        ----
        {RollingGroupby} -- A `pandas.core.window.RollingGroupby` object.
        """

        # If we don't a symbols group, then create it.
        if not self._symbol_groups:
            self.symbol_groups

        self._symbol_rolling_groups: RollingGroupby = self._symbol_groups.rolling(size)
        
        return self._symbol_rolling_groups


    def create_frame(self) -> pd.DataFrame:
        """Creates a new data frame with the data passed through.

        Returns:
        ----
        {pd.DataFrame} -- A pandas dataframe.
        """          
        
        # Make a data frame.
        price_df = pd.DataFrame(data=self._data)
        price_df = self._parse_datetime_column(price_df=price_df)
        price_df = self._set_multi_index(price_df=price_df)

        return price_df

    def _parse_datetime_column(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """Parses the datetime column passed through.

        Arguments:
        ----
        price_df {pd.DataFrame} -- The price data frame with a
            datetime column.

        Returns:
        ----
        {pd.DataFrame} -- A pandas dataframe.
        """        

        price_df['datetime'] = pd.to_datetime(price_df['datetime'], unit='ms', origin='unix')

        return price_df
    
    def _set_multi_index(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """Converts the dataframe to a multi-index data frame.

        Arguments:
        ----
        price_df {pd.DataFrame} -- The price data frame.

        Returns:
        ----
        pd.DataFrame -- A pandas dataframe.
        """        

        price_df = price_df.set_index(keys=['symbol','datetime'])

        return price_df

    def add_rows(self, data: Dict) -> None:
        """Adds a new row to our StockFrame.

        Arguments:
        ----
        data {Dict} -- A list of quotes.

        Usage:
        ----

        """        

        column_names = ['open', 'close', 'high', 'low', 'volume']

        for symbol in data:

            # Parse the Timestamp.
            time_stamp = pd.to_datetime(
                data[symbol]['quoteTimeInLong'],
                unit='ms',
                origin='unix'
            )

            # Define the Index Tuple.
            row_id = (symbol, time_stamp)

            # Define the values.
            row_values = [
                data[symbol]['openPrice'],
                data[symbol]['closePrice'],
                data[symbol]['highPrice'],
                data[symbol]['lowPrice'],
                data[symbol]['askSize'] + data[symbol]['bidSize']
            ]

            # Create a new row.
            new_row  = pd.Series(data=row_values)
            
            # Add the row.
            self.frame.loc[row_id, column_names] = new_row.values

            self.frame.sort_index(inplace=True)

    def do_indicator_exist(self, column_names: List[str]) -> bool:

        if set(column_names).issubset(self._frame.columns):
            return True
        else:
            raise KeyError("The following indicator columns are missing from the StockFrame: {missing_columns}".format(
                missing_columns=set(column_names).difference(self._frame.columns)
            )) 

    def _check_signals(self, indicators: dict) -> pd.DataFrame:

        # Grab the last rows.
        last_rows = self._symbol_groups.tail(1)

        conditions = []

        # Check to see if all the columns exist.
        if self.do_indicator_exist(column_names=indicators.keys()):

            for indicator in indicators:

                column = last_rows[indicator]
                buy_condition_target = indicators[indicator]['buy']
                sell_condition_target = indicators[indicator]['sell']

                condition_1 = column > buy_condition_target
                condition_2 = column > sell_condition_target

                conditions.append((condition_1 & condition_2))



        print(conditions)

            

