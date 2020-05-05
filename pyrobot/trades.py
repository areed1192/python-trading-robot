import datetime
from typing import Union
from typing import List

class Trade():

    """
    Object Type:
    ----
    `pyrobot.Trade`

    Overview:
    ----
    Reprsents the Trade Object which is used to create new trades,
    add customizations to them, and easily modify existing content.
    """

    def __init__(self):
        """Initalizes a new order."""            
        
        self.order: dict = None
        self.side: str = ""
        self.enter_or_exit: str = ""
        self._triggered_added: bool = False

    def new_trade(self, order_type: str, side: str, enter_or_exit: str, price: float = 0.00, stop_limit_price: float = 0.00) -> dict:
        """Creates a new Trade object template.

        A trade object is a template that can be used to help build complex trades
        that normally are prone to errors when writing the JSON. Additionally, it
        will help the process of storing trades easier.
        
        Arguments:
        ----
        order_type {str} -- The type of order you would like to create. Can be
            one of the following: ['mkt', 'lmt', 'stop', 'stop_lmt', 'trailing_stop']

        side {str} -- The side the trade will take, can be one of the
            following: ['long', 'short']

        enter_or_exit {str} -- Specifices whether this trade will enter a new position
            or exit an existing position. If used to enter then specify, 'enter'. If
            used to exit a trade specify, 'exit'.
        
        Returns:
        ----
        dict -- [description]
        """

        self.order_types = {
            'mkt':'MARKET',
            'lmt':'LIMIT',
            'stop':'STOP',
            'stop_lmt':'STOP_LIMIT',
            'trailing_stop':'TRAILING_STOP'
        }

        self.order_instructions = {
            'enter':{
                'long':'BUY',
                'short':'SELL_SHORT'
            },
            'exit':{
                'long':'SELL',
                'short':'BUY_TO_COVER'                
            }
        }

        self.order = {
            "orderStrategyType": "SINGLE",
            "orderType": self.order_types[order_type],
            "session": "NORMAL",
            "duration": "DAY",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[enter_or_exit][side],
                    "quantity": 0,
                    "instrument": {
                        "symbol": None,
                        "assetType": None
                    }
                }
            ]
        }

        if self.order['orderType'] == 'STOP':
            self.order['stopPrice'] = price

        elif self.order['orderType'] == 'LIMIT':
            self.order['price'] = price

        elif self.order['orderType'] == 'STOP_LIMIT':
            self.order['price'] = stop_limit_price
            self.order['stopPrice'] = price

        elif self.order['orderType'] == 'TRAILING_STOP':
            self.order['stopPriceLinkBasis'] == ""
            self.order['stopPriceLinkType'] == ""
            self.order['stopPriceOffset'] == 0.00
            self.order['stopType'] == 'STANDARD'

        # Make a refrence to the side we take, useful when adding other components.
        self.enter_or_exit = enter_or_exit
        self.side = side
        self.order_type = order_type
        self.price = price

        if order_type == 'stop' or order_type == 'stop-lmt':
            self.stop_price = price
        else:
            self.stop_price = 0.0

        if self.enter_or_exit == 'enter':
            self.enter_or_exit_opposite = 'exit'
        if self.enter_or_exit == 'exit':
            self.enter_or_exit_opposite = 'enter'

    def instrument(self, symbol: str, quantity: int, asset_type: str, sub_asset_type: str = None) -> dict:
        """Adds an instrument to a trade.
        
        Arguments:
        ----
        symbol {str} -- [description]

        quantity {int} -- The quantity of shares to be purchased.
        
        asset_type {str} -- [description]
        
        Keyword Arguments:
        ----
        sub_asset_type {str} -- [description] (default: {None})
        
        Returns:
        ----
        dict -- [description]
        """

        self.order['orderLegCollection'][0]['instrument']['symbol'] = symbol
        self.order['orderLegCollection'][0]['instrument']['assetType'] = asset_type
        self.order['orderLegCollection'][0]['quantity'] = quantity

        self.order_size = quantity
        self.symbol = symbol
        self.asset_type = asset_type

        return self.order['orderLegCollection'][0]

    def good_till_cancel(self, cancel_time: datetime.datetime) -> None:
        """Converts an order to a `Good Till Cancel` order.
        
        Arguments:
        ----
        cancel_time {datetime.datetime} -- A datetime object representing the
            cancel time of the order.
        """

        self.order['duration'] = 'GOOD_TILL_CANCEL'
        self.order['cancelTime'] = cancel_time.isoformat()

    def modify_side(self):
        pass

    def add_box_range(self, profit_size: float = 0.00, percentage: bool = False, stop_limit: bool = False):  
        """Adds a Stop Loss(or  Stop-Limit order), and a limit Order

        Keyword Arguments:
        ----
        stop_limit {bool} -- If `True` makes the stop-loss a stop-limit. (default: {False})
        """        
        
        if not self._triggered_added:
            self._convert_to_trigger()

        # Add a take profit Limit order.
        self.add_take_profit(profit_size=profit_size, percentage=percentage)

        # Add a stop Loss Order.
        if not stop_limit:
            self.add_stop_loss(profit_size=profit_size, percentage=percentage)

    def add_stop_loss(self, stop_size: float, percentage: bool = False) -> bool:
        """Add's a stop loss order to exit the position when a certain loss is reached.

        Arguments:
        ----
        stop_size {float} -- The size of the stop from the current trading price. For example, `0.10`.

        Keyword Arguments:
        ----
        percentage {bool} -- Specifies whether the `stop_size` adjustment is a
            `percentage` or an `absolute dollar amount`. If `True` will calculate the
            stop size as a percentage of the current price. (default: {False})

        Returns:
        ----
        bool -- `True` if the order was added.
        """

        if not self._triggered_added:
            self._convert_to_trigger()
        
        if self.order_type == 'mkt':
            # Have to make a call to Get Quotes.
            pass
        elif self.order_type == 'lmt':
            price = self.price
        
        if percentage:
            adjustment = 1.0 - stop_size
            new_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -stop_size
            new_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        stop_loss_order = {
            "orderType": "STOP",
            "session": "NORMAL",
            "duration": "DAY",
            "stopPrice": new_price,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[self.enter_or_exit_opposite][self.side],
                    "quantity": self.order_size,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type
                    }
                }
            ]
        }

        self.stop_loss_order = stop_loss_order
        self.order['childOrderStrategies'].append(self.stop_loss_order)

        return True

    def add_stop_limit(self, stop_size: float, limit_size: float, stop_percentage: bool = False, limit_percentage: bool = False):
        """Add's a Stop Limit Order to exit a trade when a stop price is reached but does not exceed the limit.

        Arguments:
        ----
        stop_size {float} -- The size of the stop from the current trading price. For example, `0.10`.

        limit_size {float} -- The size of the limit from the current stop price. For example, `0.10`.

        Keyword Arguments:
        ----
        stop_percentage {bool} -- Specifies whether the `stop_size` adjustment is a
            `percentage` or an `absolute dollar amount`. If `True` will calculate the
            stop size as a percentage of the current price. (default: {False})

        limit_percentage {bool} -- Specifies whether the `limit_size` adjustment is a
            `percentage` or an `absolute dollar amount`. If `True` will calculate the
            limit size as a percentage of the current stop price. (default: {False})

        Returns:
        ----
        bool -- `True` if the order was added.
        """

        # Check to see if there is a trigger.
        if not self._triggered_added:
            self._convert_to_trigger()
        
        # Grab the price.
        if self.order_type == 'mkt':
            # Have to make a call to Get Quotes.
            pass
        elif self.order_type == 'lmt':
            price = self.price
        
        # Calculate the Stop Price.
        if stop_percentage:
            adjustment = 1.0 - stop_size
            stop_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -stop_size
            stop_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        # Calculate the Limit Price.
        if limit_percentage:
            adjustment = 1.0 - limit_size
            limit_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -limit_size
            limit_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        # Add the order.
        stop_limit_order = {
            "orderType": "STOP_LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "price":limit_price,
            "stopPrice": stop_price,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[self.enter_or_exit_opposite][self.side],
                    "quantity": self.order_size,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type
                    }
                }
            ]
        }

        self.stop_limit_order = stop_limit_order
        self.order['childOrderStrategies'].append(self.stop_limit_order)

        return True        

    def _calculate_new_price(self, price: float, adjustment: float, percentage: bool) -> float:
        """Calculates an adjusted price given an old price.

        Arguments:
        ----
        price {float} -- The original price.
        
        adjustment {float} -- The adjustment to be made to the new price.
            
        percentage {bool} -- Specifies whether the adjustment is a percentage adjustment `True` or
            an absolute dollar adjustment `False`.

        Returns:
        ----
        float -- The new price after the adjustment has been made.
        """        

        if percentage:
            new_price = price * adjustment
        else:
            new_price = price + adjustment

        # For orders below $1.00, can only have 4 decimal places.
        if new_price < 1:
            new_price = round(new_price,4)

        # For orders above $1.00, can only have 2 decimal places.
        else:
            new_price = round(new_price, 2)
        
        return new_price

    def add_take_profit(self, profit_size: float, percentage: bool = False) -> bool:
        """Add's a Limit Order to exit a trade when a profit threshold is reached.

        Arguments:
        ----
        profit_size {float} -- The size of the profit you want to make. For example, `0.10`.

        Keyword Arguments:
        ----
        percentage {bool} -- Specifies whether the `profit_size` passed through is a
            `percentage` or an `absolute dollar amount`. If `True` will calculate the
            profit as a percentage of the current price. (default: {False})

        Returns:
        ----
        bool -- `True` if the order was added.
        """        
        
        # Check to see if we have a trigger order.
        if not self._triggered_added:
            self._convert_to_trigger()

        # We need to basis to calculate off of. Use the price.
        if self.order_type == 'mkt':
            # Have to make a call to Get Quotes.
            pass
        elif self.order_type == 'lmt':
            price = self.price
        
        # Calculate the new price.
        if percentage:
            adjustment = 1.0 - profit_size
            new_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = profit_size
            new_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        # Build the order.
        take_profit_order = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": new_price,
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[self.enter_or_exit_opposite][self.side],
                    "quantity": self.order_size,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type
                    }
                }
            ]
        }

        # Add the order.
        self.take_profit_order = take_profit_order
        self.order['childOrderStrategies'].append(self.take_profit_order)

        return True

    def _convert_to_trigger(self):
        """Converts a regular order to a trigger order.

        Overview:
        ----
        Trigger orders can be used to have a stop loss orders, or take profit orders
        placed right after the main order has been placed. This helps protect the order
        when possible and take profit when thresholds are reached.    
        """        
        
        # Only convert to a trigger order, if it already isn't one.
        if self.order and self._triggered_added == False:
            self.order['orderStrategyType'] = 'TRIGGER'

            # Trigger orders will have child strategies, so initalize that list.
            self.order['childOrderStrategies'] = []

            # Update the state.
            self._triggered_added = True

    def modify_session(self, session: str) -> None:
        """Changes which session the order is for.

        Description
        ----
        Orders are able to be active during different trading sessions.
        If you would like the order to be active during a different session,
        then choose one of the following:

        1. 'am' - This is for pre-market hours.
        2. 'pm' - This is for post-market hours.
        3. 'normal' - This is for normal market hours.
        4. 'seamless' - This makes the order active all of the sessions.
        
        Arguments:
        ----
        session {str} -- The session you want the order to be active. Possible values
            are ['am', 'pm', 'normal', 'seamless']
        """

        if session in ['am', 'pm', 'normal', 'seamless']:
            self.order['session'] = session.upper()
        else:
            raise ValueError('Invalid session, choose either am, pm, normal, or seamless')
