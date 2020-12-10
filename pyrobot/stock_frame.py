import pandas as pd

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

        self._symbol_rolling_groups: RollingGroupby = self._symbol_groups.rolling(
            size
        )

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

        price_df['datetime'] = pd.to_datetime(
            price_df['datetime'],
            unit='ms', 
            origin='unix'
        )

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

        price_df = price_df.set_index(keys=['symbol', 'datetime'])

        return price_df

    def add_rows(self, data: Dict) -> None:
        """Adds a new row to our StockFrame.

        Arguments:
        ----
        data {Dict} -- A list of quotes.

        Usage:
        ----
            >>> # Create a StockFrame object.
            >>> stock_frame = trading_robot.create_stock_frame(
                data=historical_prices['aggregated']
            )
            >>> fake_data = {
                "datetime": 1586390396750,
                "symbol": "MSFT",
                "close": 165.7,
                "open": 165.67,
                "high": 166.67,
                "low": 163.5,
                "volume": 48318234
            }
            >>> # Add to the Stock Frame.
            >>> stock_frame.add_rows(data=fake_data)
        """

        column_names = ['open', 'close', 'high', 'low', 'volume']

        for quote in data:

            # Parse the Timestamp.
            time_stamp = pd.to_datetime(
                quote['datetime'],
                unit='ms',
                origin='unix'
            )

            # Define the Index Tuple.
            row_id = (quote['symbol'], time_stamp)

            # Define the values.
            row_values = [
                quote['open'],
                quote['close'],
                quote['high'],
                quote['low'],
                quote['volume']
            ]

            # Create a new row.
            new_row = pd.Series(data=row_values)

            # Add the row.
            self.frame.loc[row_id, column_names] = new_row.values

            self.frame.sort_index(inplace=True)

    def do_indicator_exist(self, column_names: List[str]) -> bool:
        """Checks to see if the indicator columns specified exist.

        Overview:
        ----
        The user can add multiple indicator columns to their StockFrame object
        and in some cases we will need to modify those columns before making trades.
        In those situations, this method, will help us check if those columns exist
        before proceeding on in the code.

        Arguments:
        ----
        column_names {List[str]} -- A list of column names that will be checked.

        Raises:
        ----
        KeyError: If a column is not found in the StockFrame, a KeyError will be raised.

        Returns:
        ----
        bool -- `True` if all the columns exist.
        """

        if set(column_names).issubset(self._frame.columns):
            return True
        else:
            raise KeyError("The following indicator columns are missing from the StockFrame: {missing_columns}".format(
                missing_columns=set(column_names).difference(
                    self._frame.columns)
            ))

    def _check_signals(self, indicators: dict, indciators_comp_key: List[str], indicators_key: List[str]) -> Union[pd.DataFrame, None]:
        """Returns the last row of the StockFrame if conditions are met.

        Overview:
        ----
        Before a trade is executed, we must check to make sure if the
        conditions that warrant a `buy` or `sell` signal are met. This
        method will take last row for each symbol in the StockFrame and
        compare the indicator column values with the conditions specified
        by the user.

        If the conditions are met the row will be returned back to the user.

        Arguments:
        ----
        indicators {dict} -- A dictionary containing all the indicators to be checked
            along with their buy and sell criteria.

        indicators_comp_key List[str] -- A list of the indicators where we are comparing
            one indicator to another indicator.

        indicators_key List[str] -- A list of the indicators where we are comparing
            one indicator to a numerical value.

        Returns:
        ----
        {Union[pd.DataFrame, None]} -- If signals are generated then, a pandas.DataFrame object
            will be returned. If no signals are found then nothing will be returned.
        """

        # Grab the last rows.
        last_rows = self._symbol_groups.tail(1)

        # Define a list of conditions.
        conditions = []

        # Check to see if all the columns exist.
        if self.do_indicator_exist(column_names=indicators_key):

            for indicator in indicators_key:

                column = last_rows[indicator]

                # Grab the Buy & Sell Condition.
                buy_condition_target = indicators[indicator]['buy']
                sell_condition_target = indicators[indicator]['sell']

                buy_condition_operator = indicators[indicator]['buy_operator']
                sell_condition_operator = indicators[indicator]['sell_operator']

                condition_1: pd.Series = buy_condition_operator(
                    column, buy_condition_target
                )
                condition_2: pd.Series = sell_condition_operator(
                    column, sell_condition_target
                )

                condition_1 = condition_1.where(lambda x: x == True).dropna()
                condition_2 = condition_2.where(lambda x: x == True).dropna()

                conditions.append(('buys', condition_1))
                conditions.append(('sells', condition_2))
        
        # Store the indicators in a list.
        check_indicators = []
        
        # Split the name so we can check if the indicator exist.
        for indicator in indciators_comp_key:
            parts = indicator.split('_comp_')
            check_indicators += parts

        if self.do_indicator_exist(column_names=check_indicators):

            for indicator in indciators_comp_key:
                
                # Split the indicators.
                parts = indicator.split('_comp_')

                # Grab the indicators that need to be compared.
                indicator_1 = last_rows[parts[0]]
                indicator_2 = last_rows[parts[1]]

                # If we have a buy operator, grab it.
                if indicators[indicator]['buy_operator']:

                    # Grab the Buy Operator.
                    buy_condition_operator = indicators[indicator]['buy_operator']

                    # Grab the Condition.
                    condition_1: pd.Series = buy_condition_operator(
                        indicator_1, indicator_2
                    )

                    # Keep the one's that aren't null.
                    condition_1 = condition_1.where(lambda x: x == True).dropna()

                    # Add it as a buy signal.
                    conditions.append(('buys', condition_1))

                # If we have a sell operator, grab it.
                if indicators[indicator]['sell_operator']:

                    # Grab the Sell Operator.
                    sell_condition_operator = indicators[indicator]['sell_operator']

                    # Store it in a Pd.Series.
                    condition_2: pd.Series = sell_condition_operator(
                        indicator_1, indicator_2
                    )

                    # keep the one's that aren't null.
                    condition_2 = condition_2.where(lambda x: x == True).dropna()

                    # Add it as a sell signal.
                    conditions.append(('sells', condition_2))

        return conditions
