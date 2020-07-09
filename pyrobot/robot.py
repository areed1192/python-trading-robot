import json
import time as time_true
import pprint
import pathlib
import pandas as pd

from datetime import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from typing import List
from typing import Dict
from typing import Union
from typing import Optional

from pyrobot.trades import Trade
from pyrobot.portfolio import Portfolio
from pyrobot.stock_frame import StockFrame

from td.client import TDClient
from td.utils import milliseconds_since_epoch


class PyRobot():

    def __init__(self, client_id: str, redirect_uri: str, paper_trading: bool = True, credentials_path: Optional[str] = None, trading_account: Optional[str] = None) -> None:
        """Initalizes a new instance of the robot and logs into the API platform specified.

        Arguments:
        ----
        client_id {str} -- The Consumer ID assigned to you during the App registration. 
            This can be found at the app registration portal.

        redirect_uri {str} -- This is the redirect URL that you specified when you created your
            TD Ameritrade Application.

        Keyword Arguments:
        ----
        credentials_path {str} -- The path to the session state file used to prevent a full 
            OAuth workflow. (default: {None})

        trading_account {str} -- Your TD Ameritrade account number. (default: {None})

        """

        # Set the attirbutes
        self.trading_account = trading_account
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.credentials_path = credentials_path
        self.session: TDClient = self._create_session()
        self.trades = {}
        self.historical_prices = {}
        self.stock_frame: StockFrame = None
        self.paper_trading = paper_trading

        self._bar_size = None
        self._bar_type = None

    def _create_session(self) -> TDClient:
        """Start a new session.

        Creates a new session with the TD Ameritrade API and logs the user into
        the new session.

        Returns:
        ----
        TDClient -- A TDClient object with an authenticated sessions.

        """

        # Create a new instance of the client
        td_client = TDClient(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            credentials_path=self.credentials_path
        )

        # log the client into the new session
        td_client.login()

        return td_client

    @property
    def pre_market_open(self) -> bool:
        """Checks if pre-market is open.

        Uses the datetime module to create US Pre-Market Equity hours in
        UTC time.

        Usage:
        ----
            >>> trading_robot = PyRobot(
            client_id=CLIENT_ID, 
            redirect_uri=REDIRECT_URI, 
            credentials_path=CREDENTIALS_PATH
            )
            >>> pre_market_open_flag = trading_robot.pre_market_open
            >>> pre_market_open_flag
            True

        Returns:
        ----
        bool -- True if pre-market is open, False otherwise.

        """

        pre_market_start_time = datetime.utcnow().replace(
            hour=12,
            minute=00,
            second=00
        ).timestamp()

        market_start_time = datetime.utcnow().replace(
            hour=13,
            minute=30,
            second=00
        ).timestamp()

        right_now = datetime.utcnow().timestamp()

        if market_start_time >= right_now >= pre_market_start_time:
            return True
        else:
            return False

    @property
    def post_market_open(self):
        """Checks if post-market is open.

        Uses the datetime module to create US Post-Market Equity hours in
        UTC time.

        Usage:
        ----
            >>> trading_robot = PyRobot(
            client_id=CLIENT_ID, 
            redirect_uri=REDIRECT_URI, 
            credentials_path=CREDENTIALS_PATH
            )
            >>> post_market_open_flag = trading_robot.post_market_open
            >>> post_market_open_flag
            True

        Returns:
        ----
        bool -- True if post-market is open, False otherwise.

        """

        post_market_end_time = datetime.utcnow().replace(
            hour=22,
            minute=30,
            second=00
        ).timestamp()

        market_end_time = datetime.utcnow().replace(
            hour=20,
            minute=00,
            second=00
        ).timestamp()

        right_now = datetime.utcnow().timestamp()

        if post_market_end_time >= right_now >= market_end_time:
            return True
        else:
            return False

    @property
    def regular_market_open(self):
        """Checks if regular market is open.

        Uses the datetime module to create US Regular Market Equity hours in
        UTC time.

        Usage:
        ----
            >>> trading_robot = PyRobot(
            client_id=CLIENT_ID, 
            redirect_uri=REDIRECT_URI, 
            credentials_path=CREDENTIALS_PATH
            )
            >>> market_open_flag = trading_robot.market_open
            >>> market_open_flag
            True

        Returns:
        ----
        bool -- True if post-market is open, False otherwise.

        """

        market_start_time = datetime.utcnow().replace(
                hour=13,
                minute=30,
                second=00
        ).timestamp()

        market_end_time = datetime.utcnow().replace(
            hour=20,
            minute=00,
            second=00
        ).timestamp()

        right_now = datetime.utcnow().timestamp()

        if market_end_time >= right_now >= market_start_time:
            return True
        else:
            return False

    def create_portfolio(self) -> Portfolio:
        """Create a new portfolio.

        Creates a Portfolio Object to help store and organize positions
        as they are added and removed during trading.

        Usage:
        ----
            >>> trading_robot = PyRobot(
            client_id=CLIENT_ID, 
            redirect_uri=REDIRECT_URI, 
            credentials_path=CREDENTIALS_PATH
            )
            >>> portfolio = trading_robot.create_portfolio()
            >>> portfolio
            <pyrobot.portfolio.Portfolio object at 0x0392BF88>

        Returns:
        ----
        Portfolio -- A pyrobot.Portfolio object with no positions.
        """

        # Initalize the portfolio.
        self.portfolio = Portfolio(account_number=self.trading_account)

        # Assign the Client
        self.portfolio.td_client = self.session

        return self.portfolio

    def create_trade(self, trade_id: str, enter_or_exit: str, long_or_short: str, order_type: str = 'mkt', price: float = 0.0, stop_limit_price=0.0) -> Trade:
        """Initalizes a new instance of a Trade Object.

        This helps simplify the process of building an order by using pre-built templates that can be
        easily modified to incorporate more complex strategies.

        Arguments:
        ----
        trade_id {str} -- The ID associated with the trade, this can then be used to access the trade during runtime.

        enter_or_exit {str} -- Defines whether this trade will be used to enter or exit a position.
            If used to enter, specify `enter`. If used to exit, speicfy `exit`.

        long_or_short {str} -- Defines whether this trade will be used to go long or short a position.
            If used to go long, specify `long`. If used to go short, speicfy `short`.

        Keyword Arguments:
        ----
        order_type {str} -- Defines the type of order to initalize. Possible values
            are `'mkt', 'lmt', 'stop', 'stop-lmt', 'trailign-stop'` (default: {'mkt'})

        price {float} -- The Price to be associate with the order. If the order type is `stop` or `stop-lmt` then 
            it is the stop price, if it is a `lmt` order then it is the limit price, and `mkt` is the market 
            price.(default: {0.0})

        stop_limit_price {float} -- Only used if the order is a `stop-lmt` and represents the limit price of
            the `stop-lmt` order. (default: {0.0})

        Usage:
        ----
            >>> trading_robot = PyRobot(
                client_id=CLIENT_ID, 
                redirect_uri=REDIRECT_URI, 
                credentials_path=CREDENTIALS_PATH
            )
            >>> new_trade = trading_robot_portfolio.create_trade(
                trade_id='long_1',
                enter_or_exit='enter',
                long_or_short='long',
                order_type='mkt'
            )
            >>> new_trade

            >>> new_market_trade = trading_robot_portfolio.create_trade(
                trade_id='long_2',
                enter_or_exit='enter',
                long_or_short='long',
                order_type='mkt',
                price=12.00
            )
            >>> new_market_trade

            >>> new_stop_trade = trading_robot_portfolio.create_trade(
                trade_id='long_3',
                enter_or_exit='enter',
                long_or_short='long',
                order_type='stop',
                price=2.00
            )
            >>> new_stop_trade

            >>> new_stop_limit_trade = trading_robot_portfolio.create_trade(
                trade_id='long_4',
                enter_or_exit='enter',
                long_or_short='long',
                order_type='stop-lmt',
                price=2.00,
                stop_limit_price=1.90
            )
            >>> new_stop_limit_trade

        Returns:
        ----
        Trade -- A pyrobot.Trade object with the specified template.
        """

        # Initalize a new trade object.
        trade = Trade()

        # Create a new trade.
        trade.new_trade(
            trade_id=trade_id,
            order_type=order_type,
            side=long_or_short,
            enter_or_exit=enter_or_exit,
            price=price,
            stop_limit_price=stop_limit_price
        )

        self.trades[trade_id] = trade

        return trade

    def delete_trade(self, index: int) -> None:
        """Deletes an exisiting trade from the `trades` collection.

        Arguments:
        ----
        index {int} -- The index of the order.

        Usage:
        ----
            >>> trading_robot = PyRobot(
                client_id=CLIENT_ID, 
                redirect_uri=REDIRECT_URI, 
                credentials_path=CREDENTIALS_PATH
            )
            >>> new_trade = trading_robot_portfolio.create_trade(
                enter_or_exit='enter',
                long_or_short='long',
                order_type='mkt'
            )
            >>> trading_robot.delete_trade(index=1)
        """

        if index in self.trades:
            del self.trades[index]

    def grab_current_quotes(self) -> dict:
        """Grabs the current quotes for all positions in the portfolio.

        Makes a call to the TD Ameritrade Get Quotes endpoint with all
        the positions in the portfolio. If only one position exist it will
        return a single dicitionary, otherwise a nested dictionary.

        Usage:
        ----
            >>> trading_robot = PyRobot(
                client_id=CLIENT_ID, 
                redirect_uri=REDIRECT_URI, 
                credentials_path=CREDENTIALS_PATH
            )
            >>> trading_robot_portfolio.add_position(
            symbol='MSFT',
            asset_type='equity'
            )
            >>> current_quote = trading_robot.grab_current_quotes()
            >>> current_quote
            {
                "MSFT": {
                    "assetType": "EQUITY",
                    "assetMainType": "EQUITY",
                    "cusip": "594918104",
                    ...
                    "regularMarketPercentChangeInDouble": 0,
                    "delayed": true
                }
            }

            >>> trading_robot = PyRobot(
            client_id=CLIENT_ID, 
            redirect_uri=REDIRECT_URI, 
            credentials_path=CREDENTIALS_PATH
            )
            >>> trading_robot_portfolio.add_position(
            symbol='MSFT',
            asset_type='equity'
            )
            >>> trading_robot_portfolio.add_position(
            symbol='AAPL',
            asset_type='equity'
            )
            >>> current_quote = trading_robot.grab_current_quotes()
            >>> current_quote

            {
                "MSFT": {
                    "assetType": "EQUITY",
                    "assetMainType": "EQUITY",
                    "cusip": "594918104",
                    ...
                    "regularMarketPercentChangeInDouble": 0,
                    "delayed": False
                },
                "AAPL": {
                    "assetType": "EQUITY",
                    "assetMainType": "EQUITY",
                    "cusip": "037833100",
                    ...
                    "regularMarketPercentChangeInDouble": 0,
                    "delayed": False
                }
            }

        Returns:
        ----
        dict -- A dictionary containing all the quotes for each position.

        """

        # First grab all the symbols.
        symbols = self.portfolio.positions.keys()

        # Grab the quotes.
        quotes = self.session.get_quotes(instruments=list(symbols))

        return quotes

    def grab_historical_prices(self, start: datetime, end: datetime, bar_size: int = 1,
                               bar_type: str = 'minute', symbols: Optional[List[str]] = None) -> List[dict]:
        """Grabs the historical prices for all the postions in a portfolio.

        Overview:
        ----
        Any of the historical price data returned will include extended hours
        price data by default.

        Arguments:
        ----
        start {datetime} -- Defines the start date for the historical prices.

        end {datetime} -- Defines the end date for the historical prices.

        Keyword Arguments:
        ----
        bar_size {int} -- Defines the size of each bar. (default: {1})

        bar_type {str} -- Defines the bar type, can be one of the following:
            `['minute', 'week', 'month', 'year']` (default: {'minute'})

        symbols {List[str]} -- A list of ticker symbols to pull. (default: None)

        Returns:
        ----
        {List[Dict]} -- The historical price candles.

        Usage:
        ----
            >>> trading_robot = PyRobot(
                client_id=CLIENT_ID,
                redirect_uri=REDIRECT_URI,
                credentials_path=CREDENTIALS_PATH
                )
            >>> start_date = datetime.today()
            >>> end_date = start_date - timedelta(days=30)
            >>> historical_prices = trading_robot.grab_historical_prices(
                    start=end_date,
                    end=start_date,
                    bar_size=1,
                    bar_type='minute'
                )
        """

        self._bar_size = bar_size
        self._bar_type = bar_type

        start = str(milliseconds_since_epoch(dt_object=start))
        end = str(milliseconds_since_epoch(dt_object=end))

        new_prices = []

        if not symbols:
            symbols = self.portfolio.positions

        for symbol in symbols:

            historical_prices_response = self.session.get_price_history(
                symbol=symbol,
                period_type='day',
                start_date=start,
                end_date=end,
                frequency_type=bar_type,
                frequency=bar_size,
                extended_hours=True
            )

            self.historical_prices[symbol] = {}
            self.historical_prices[symbol]['candles'] = historical_prices_response['candles']

            for candle in historical_prices_response['candles']:

                new_price_mini_dict = {}
                new_price_mini_dict['symbol'] = symbol
                new_price_mini_dict['open'] = candle['open']
                new_price_mini_dict['close'] = candle['close']
                new_price_mini_dict['high'] = candle['high']
                new_price_mini_dict['low'] = candle['low']
                new_price_mini_dict['volume'] = candle['volume']
                new_price_mini_dict['datetime'] = candle['datetime']
                new_prices.append(new_price_mini_dict)

        self.historical_prices['aggregated'] = new_prices

        return self.historical_prices

    def get_latest_bar(self) -> List[dict]:
        """Returns the latest bar for each symbol in the portfolio.

        Returns:
        ---
        {List[dict]} -- A simplified quote list.

        Usage:
        ----
            >>> trading_robot = PyRobot(
                client_id=CLIENT_ID,
                redirect_uri=REDIRECT_URI,
                credentials_path=CREDENTIALS_PATH
            )
            >>> latest_bars = trading_robot.get_latest_bar()
            >>> latest_bars

        """

        # Grab the info from the last quest.
        bar_size = self._bar_size
        bar_type = self._bar_type

        # Define the start and end date.
        start_date = datetime.today()
        end_date = start_date - timedelta(minutes=15)
        start = str(milliseconds_since_epoch(dt_object=start_date))
        end = str(milliseconds_since_epoch(dt_object=end_date))

        latest_prices = []

        # Loop through each symbol.
        for symbol in self.portfolio.positions:

            # Grab the request.
            historical_prices_response = self.session.get_price_history(
                symbol=symbol,
                period_type='day',
                start_date=start,
                end_date=end,
                frequency_type=bar_type,
                frequency=bar_size,
                extended_hours=True
            )

            # latest_prices.append(historical_prices_response['candles'][-1])

            if 'error' in historical_prices_response:
                
                time_true.sleep(2)

                # Grab the request.
                historical_prices_response = self.session.get_price_history(
                    symbol=symbol,
                    period_type='day',
                    start_date=start,
                    end_date=end,
                    frequency_type=bar_type,
                    frequency=bar_size,
                    extended_hours=True
                )               

            # parse the candles.
            for candle in historical_prices_response['candles'][-1:]:

                new_price_mini_dict = {}
                new_price_mini_dict['symbol'] = symbol
                new_price_mini_dict['open'] = candle['open']
                new_price_mini_dict['close'] = candle['close']
                new_price_mini_dict['high'] = candle['high']
                new_price_mini_dict['low'] = candle['low']
                new_price_mini_dict['volume'] = candle['volume']
                new_price_mini_dict['datetime'] = candle['datetime']
                latest_prices.append(new_price_mini_dict)

        return latest_prices

    def wait_till_next_bar(self, last_bar_timestamp: pd.DatetimeIndex) -> None:
        """Waits the number of seconds till the next bar is released.

        Arguments:
        ----
        last_bar_timestamp {pd.DatetimeIndex} -- The last bar's timestamp.
        """

        last_bar_time = last_bar_timestamp.to_pydatetime()[
            0].replace(tzinfo=timezone.utc)
        next_bar_time = last_bar_time + timedelta(seconds=60)
        curr_bar_time = datetime.now(tz=timezone.utc)

        last_bar_timestamp = int(last_bar_time.timestamp())
        next_bar_timestamp = int(next_bar_time.timestamp())
        curr_bar_timestamp = int(curr_bar_time.timestamp())

        _time_to_wait_bar = next_bar_timestamp - last_bar_timestamp
        time_to_wait_now = next_bar_timestamp - curr_bar_timestamp

        if time_to_wait_now < 0:
            time_to_wait_now = 0

        print("="*80)
        print("Pausing for the next bar")
        print("-"*80)
        print("Curr Time: {time_curr}".format(
                time_curr=curr_bar_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        print("Next Time: {time_next}".format(
                time_next=next_bar_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        print("Sleep Time: {seconds}".format(seconds=time_to_wait_now))
        print("-"*80)
        print('')

        time_true.sleep(time_to_wait_now)

    def create_stock_frame(self, data: List[dict]) -> StockFrame:
        """Generates a new StockFrame Object.

        Arguments:
        ----
        data {List[dict]} -- The data to add to the StockFrame object.

        Returns:
        ----
        StockFrame -- A multi-index pandas data frame built for trading.
        """

        # Create the Frame.
        self.stock_frame = StockFrame(data=data)

        return self.stock_frame

    def execute_signals(self, signals: List[pd.Series], trades_to_execute: dict) -> List[dict]:
        """Executes the specified trades for each signal.

        Arguments:
        ----
        signals {list} -- A pandas.Series object representing the buy signals and sell signals.
            Will check if series is empty before making any trades.

        Trades:
        ----
        trades_to_execute {dict} -- the trades you want to execute if signals are found.

        Returns:
        ----
        {List[dict]} -- Returns all order responses.

        Usage:
        ----
            >>> trades_dict = {
                    'MSFT': {
                        'trade_func': trading_robot.trades['long_msft'],
                        'trade_id': trading_robot.trades['long_msft'].trade_id
                    }
                }
            >>> signals = indicator_client.check_signals()
            >>> trading_robot.execute_signals(
                signals=signals,
                trades_to_execute=trades_dict
                )
        """

        buys: pd.Series = signals[0][1]
        sells: pd.Series = signals[1][1]

        order_responses = []

        # If we have buys or sells continue.
        if not buys.empty:

            # Grab the buy Symbols.
            symbols_list = buys.index.get_level_values(0).to_list()

            # Loop through each symbol.
            for symbol in symbols_list:

                # Check to see if there is a Trade object.
                if symbol in trades_to_execute:

                    if self.portfolio.in_portfolio(symbol=symbol):
                        self.portfolio.set_ownership_status(
                            symbol=symbol,
                            ownership=True
                        )

                    # Set the Execution Flag.
                    trades_to_execute[symbol]['has_executed'] = True
                    trade_obj: Trade = trades_to_execute[symbol]['trade_func']

                    if not self.paper_trading:

                        # Execute the order.
                        order_response = self.execute_orders(
                            trade_obj=trade_obj
                        )

                        order_response = {
                            'order_id': order_response['order_id'],
                            'request_body': order_response['request_body'],
                            'timestamp': datetime.now().isoformat()
                        }

                        order_responses.append(order_response)

                    else:

                        order_response = {
                            'order_id': trade_obj._generate_order_id(),
                            'request_body': trade_obj.order,
                            'timestamp': datetime.now().isoformat()
                        }

                        order_responses.append(order_response)

        elif not sells.empty:

            # Grab the buy Symbols.
            symbols_list = sells.index.get_level_values(0).to_list()

            # Loop through each symbol.
            for symbol in symbols_list:

                # Check to see if there is a Trade object.
                if symbol in trades_to_execute:

                    # Set the Execution Flag.
                    trades_to_execute[symbol]['has_executed'] = True

                    if self.portfolio.in_portfolio(symbol=symbol):
                        self.portfolio.set_ownership_status(
                            symbol=symbol,
                            ownership=False
                        )

                    trade_obj: Trade = trades_to_execute[symbol]['trade_func']

                    if not self.paper_trading:

                        # Execute the order.
                        order_response = self.execute_orders(
                            trade_obj=trade_obj
                        )

                        order_response = {
                            'order_id': order_response['order_id'],
                            'request_body': order_response['request_body'],
                            'timestamp': datetime.now().isoformat()
                        }

                        order_responses.append(order_response)

                    else:

                        order_response = {
                            'order_id': trade_obj._generate_order_id(),
                            'request_body': trade_obj.order,
                            'timestamp': datetime.now().isoformat()
                        }

                        order_responses.append(order_response)

        # Save the response.
        self.save_orders(order_response_dict=order_responses)

        return order_responses

    def execute_orders(self, trade_obj: Trade) -> dict:
        """Executes a Trade Object.

        Overview:
        ----
        The `execute_orders` method will execute trades as they're signaled. When executed,
        the `Trade` object will have the order response saved to it, and the order response will
        be saved to a JSON file for further analysis.

        Arguments:
        ----
        trade_obj {Trade} -- A trade object with the `order` property filled out.

        Returns:
        ----
        {dict} -- An order response dicitonary.
        """

        # Execute the order.
        order_dict = self.session.place_order(
            account=self.trading_account,
            order=trade_obj.order
        )

        return order_dict

    def save_orders(self, order_response_dict: dict) -> bool:
        """Saves the order to a JSON file for further review.

        Arguments:
        ----
        order_response {dict} -- A single order response.

        Returns:
        ----
        {bool} -- `True` if the orders were successfully saved.
        """

        # Define the folder.
        folder: pathlib.PurePath = pathlib.Path(
            __file__).parents[1].joinpath("data")

        # See if it exist, if not create it.
        if not folder.exists():
            folder.mkdir()

        # Define the file path.
        file_path = folder.joinpath('orders.json')

        # First check if the file alread exists.
        if file_path.exists():

            with open('data/orders.json', 'r') as order_json:
                orders_list = json.load(order_json)

        else:

            orders_list = []

        # Combine both lists.
        orders_list = orders_list + order_response_dict

        # Write the new data back.
        with open(file='data/orders.json', mode='w+') as order_json:
            json.dump(obj=orders_list, fp=order_json, indent=4)

        return True
