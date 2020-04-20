import datetime

class Trade():

    def __init__(self):        
        self.order = None

    def new_trade(self, order_type: str, side: str, enter_or_exit: str) -> dict:
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

        order_types = {
            'mkt':'MARKET',
            'lmt':'LIMIT',
            'stop':'STOP',
            'stop_lmt':'STOP_LIMIT',
            'trailing_stop':'TRAILING_STOP'
        }

        order_instructions = {
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
            "orderType": order_types[order_type],
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": order_instructions[enter_or_exit][side],
                    "quantity": 0,
                    "instrument": {
                        "symbol": None,
                        "assetType": None
                    }
                }
            ]
        }

        if self.order['orderType'] == 'STOP':
            self.order['stopPrice'] = 0.00
        elif self.order['orderType'] == 'LIMIT':
            self.order['price'] = 0.00
        elif self.order['orderType'] == 'STOP_LIMIT':
            self.order['price'] = 0.00
            self.order['stopPrice'] = 0.00
        elif self.order['orderType'] == 'TRAILING_STOP':
            self.order['stopPriceLinkBasis'] == ""
            self.order['stopPriceLinkType'] == ""
            self.order['stopPriceOffset'] == 0.00
            self.order['stopType'] == 'STANDARD'

    def instrument(self, symbol: str, asset_type: str, sub_asset_type: str = None) -> dict:
        """[summary]
        
        Arguments:
            symbol {str} -- [description]
            asset_type {str} -- [description]
        
        Keyword Arguments:
            sub_asset_type {str} -- [description] (default: {None})
        
        Returns:
            dict -- [description]
        """

        self.order['orderLegCollection'][0]['instrument']['symbol'] = symbol
        self.order['orderLegCollection'][0]['instrument']['assetType'] = asset_type

        return order['orderLegCollection'][0]

    def good_till_cancel(self, cancel_time: datetime.datetime) -> None:
        """Converts an order to a `Good Till Cancel` order.
        
        Arguments:
            cancel_time {datetime.datetime} -- A datetime object representing the
                cancel time of the order.
        """


        self.order['duration'] = 'GOOD_TILL_CANCEL'
        self.order['cancelTime'] = cancel_time.isoformat()


    def modify_side(self):
        pass

    def add_stop_loss(self):
        pass

    def add_profit_lock(self):
        pass

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
        

    

