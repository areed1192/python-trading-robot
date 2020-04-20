
class Trade():

    def __init__(self):
        pass

    def new_trade(self, order_type: str, side: str, enter_or_exit: str) -> dict:
        """[summary]
        
        Arguments:
            order_type {str} -- [description]
            side {str} -- [description]
            enter_or_exit {str} -- [description]
        
        Returns:
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

        order_template = {
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

        if order_template['orderType'] == 'STOP':
            order_template['stopPrice'] = 0.00
        elif order_template['orderType'] == 'LIMIT':
            order_template['price'] = 0.00
        elif order_template['orderType'] == 'STOP_LIMIT':
            order_template['price'] = 0.00
            order_template['stopPrice'] = 0.00
        elif order_template['orderType'] == 'TRAILING_STOP':
            order_template['stopPriceLinkBasis'] == ""
            order_template['stopPriceLinkType'] == ""
            order_template['stopPriceOffset'] == 0.00
            order_template['stopType'] == 'STANDARD'

    def instrument(self, symbol = None):
        pass

    def order_type(self, order_type = None):
        pass

    def good_till_cancel(self, cancel_time = None):
        pass

    def side(self):
        pass

    def add_stop_loss(self):
        pass

    def add_stop_profit(self):
        pass

    def session(self):
        pass

    

