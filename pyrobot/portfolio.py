from typing import Tuple
from typing import List
from typing import Optional
from typing import Iterable

class Portfolio():

    def __init__(self, account_number: Optional[str] = None) -> None:
        """Initalizes a new instance of the Portfolio object.
        
        Keyword Arguments:
        ----
        account_number {str} -- An accout number to associate with the Portfolio. (default: {None})
        """
        
        self.positions = {}
        self.positions_count = 0
        self.market_value = 0.00
        self.profit_loss = 0.00
        self.risk_tolerance = 0.00
        self.account_number = account_number

    def add_positions(self, positions: List[dict]) -> dict:
        """Add Multiple positions to the portfolio at once.

        This method will take an iterable containing the values
        normally passed through in the `add_position` endpoint and
        then adds each position to the portfolio.
        
        Arguments:
        ----
        positions {list[dict]} -- Multiple positions with the required arguments to be added.

        Returns:
        ----
        {dict} -- The current positions in the portfolio.

        Usage:
        ----
            # Define mutliple positions to add.
            >>> multi_position = [
                {
                    'asset_type': 'equity',
                    'quantity': 2,
                    'purchase_price': 4.00,
                    'symbol': 'TSLA',
                    'purchase_date': '2020-01-31'
                },
                {
                    'asset_type': 'equity',
                    'quantity': 2,0
                    'purchase_price': 4.00,
                    'symbol': 'SQ',
                    'purchase_date': '2020-01-31'
                }
            ]
            >>> new_positions = trading_robot.portfolio.add_positions(positions=multi_position)
            {
                'SQ': {
                    'asset_type': 'equity',
                    'purchase_date': '2020-01-31',
                    'purchase_price': 4.00,
                    'quantity': 2,
                    'symbol': 'SQ'
                },
                'TSLA': {
                    'asset_type': 'equity',
                    'purchase_date': '2020-01-31',
                    'purchase_price': 4.00,
                    'quantity': 2,
                    'symbol': 'TSLA'
                }
            }
        """
        
        if isinstance(positions, list):

            # Loop through each position.
            for position in positions:
                
                # Add the position.
                self.add_position(
                    symbol=position['symbol'],
                    asset_type=position['asset_type'],
                    quantity=position.get('quantity',0),
                    purchase_price=position.get('purchase_price',0.0),
                    purchase_date=position.get('purchase_date',None)
                )

            return self.positions

        else:
            raise TypeError('Positions must be a list of dictionaries.')

    def add_position(self, symbol: str, asset_type: str, purchase_date: Optional[str] = None, quantity: int = 0, purchase_price: float = 0.0) -> dict:
        """Adds a single new position to the the portfolio.
        
        Arguments:
        ----
        symbol {str} -- The Symbol of the Financial Instrument. Example: 'AAPL' or '/ES'

        asset_type {str} -- The type of the financial instrument to be added. For example,
            'equity', 'forex', 'option', 'futures'

        Keyword Arguments:
        ----
        quantity {int} -- The number of shares or contracts you own. (default: {0})

        purchase_price {float} -- The price at which the position was purchased. (default: {0.00})

        purchase_date {str} -- The date which the asset was purchased. Must be ISO Format "YYYY-MM-DD"
            For example, "2020-04-01" (default: {None})

        Returns:
        ----
        {dict} -- A dictionary object that represents a position in the portfolio.

        Usage:
        ----
            >>> portfolio = Portfolio()
            >>> new_position = Portfolio.add_position(symbol='MSFT', 
                    asset_type='equity', 
                    quantity=2, 
                    purchase_price=4.00,
                    purchase_date="2020-01-31"
                )
            >>> new_position
            {
                'asset_type': 'equity', 
                'quantity': 2, 
                'purchase_price': 4.00,
                'symbol': 'MSFT',
                'purchase_date': '2020-01-31'
            }
        """
        
        self.positions[symbol] = {}
        self.positions[symbol]['symbol'] = symbol
        self.positions[symbol]['quantity'] = quantity
        self.positions[symbol]['purchase_price'] = purchase_price
        self.positions[symbol]['purchase_date'] = purchase_date
        self.positions[symbol]['asset_type'] = asset_type

        return self.positions[symbol]

    def remove_position(self, symbol: str) -> Tuple[bool,str]:
        """Deletes a single position from the portfolio.
        
        Arguments:
        ----
        symbol {str} -- The symbol of the instrument to be deleted. Example: 'AAPL' or '/ES'

        Returns:
        ----
        {Tuple[bool, str]} -- Returns `True` if successfully deleted, `False` otherwise 
            along with a message.

        Usage:
        ----
            >>> portfolio = Portfolio()

            >>> new_position = Portfolio.add_position(
                    symbol='MSFT', 
                    asset_type='equity', 
                    quantity=2, 
                    purchase_price=4.00,
                    purchase_date="2020-01-31"
                )
            >>> delete_status = Portfolio.delete_position(symbol='MSFT')
            >>> delete_status
            (True, 'MSFT was successfully removed.')

            >>> delete_status = Portfolio.delete_position(symbol='AAPL')
            >>> delete_status
            (False, 'AAPL did not exist in the porfolio.')
        """
        
        if symbol in self.positions:
            del self.positions[symbol]
            return (True, "{symbol} was successfully removed.".format(symbol=symbol))
        else:
            return (False, "{symbol} did not exist in the porfolio.".format(symbol=symbol))

    def total_allocation(self) -> dict:
        """Returns a summary of the portfolio by asset allocation.
        """        

        total_allocation = {
            'stocks':[],
            'fixed_income':[],
            'options':[],
            'futures':[],
            'furex':[]
        }
        
        if len(self.positions.keys()) > 0:
            for symbol in self.positions:
                total_allocation[self.positions[symbol]['asset_type']].append(self.positions[symbol])

    def risk_exposure(self):
        pass

    def portfolio_summary(self):
        pass
    
    def in_portfolio(self, symbol: str) -> bool:
        """checks if the symbol is in the portfolio.
        
        Arguments:
        ----
        symbol {str} -- The symbol of the instrument to be deleted. Example: 'AAPL' or '/ES'

        Returns:
        ----
        bool -- `True` if the position is in the portfolio, `False` otherwise.

        Usage:
        ----
            >>> portfolio = Portfolio()
            >>> new_position = Portfolio.add_position(
                symbol='MSFT', 
                asset_type='equity'
            )
            >>> in_position_flag = Portfolio.in_portfolio(symbol='MSFT')
            >>> in_position_flag
            True
        """

        if symbol in self.positions:
            return True
        else:
            return False

    def is_profitable(self, symbol: str, current_price: float) -> bool:
        """Specifies whether a position is profitable.
        
        Arguments:
        ----
        symbol {str} -- The symbol of the instrument, to check profitability.

        current_price {float} -- The current trading price of the instrument.
        
        Returns:
        ----
        {bool} -- Specifies whether the position is profitable or flat `True` or not
            profitable `False`.
        
        Raises:
        ----
        KeyError: If the Symbol does not exist it will return a key error.
        
        Usage:
        ----
            >>> portfolio = Portfolio()
            >>> new_position = Portfolio.add_position(
                symbol='MSFT', 
                asset_type='equity',
                purchase_price=4.00,
                purchase_date="2020-01-31"
            )
            >>> is_profitable_flag = Portfolio.is_profitable(
                symbol='MSFT',
                current_price=7.00
            )
            >>> is_profitable_flag
            True
        """

        # Grab the purchase price, if it exists.
        if self.in_portfolio(symbol=symbol):
            purchase_price = self.positions[symbol]['purchase_price']
        else:
            raise KeyError("The Symbol you tried to request does not exist.")
        
        if (purchase_price <= current_price):
            return True
        elif (purchase_price > current_price):
            return False

    def projected_market_value(self, current_prices: dict) -> dict:
        """Returns the Projected market value for all the positions in the portfolio.

        Arguments:
        ----
        current_prices {dict} -- A dictionary of current quotes for each of the symbols
            in the portfolio.

        Returns:
        ----
        dict -- A summarized version of the portfolio with each position, purchase price, current price,
            and projected values.
        
        Usage:
        ----
            >>> portfolio = Portfolio()
            >>> new_position = portfolio.add_position(
                symbol='MSFT', 
                asset_type='equity',
                purchase_price=4.00,
                purchase_date="2020-01-31"
            )
            >>> portfolio_summary = portfolio.projected_market_value(current_prices={'MSFT':{'lastPrice': 8.00, 'openPrice': 7.50}})        
        """

        projected_value = {}
        total_value = 0.0
        total_invested_capital = 0.0
        total_profit_or_loss = 0.0

        position_count_profitable = 0
        position_count_not_profitable = 0
        position_count_break_even = 0
        
        for symbol in current_prices:

            if self.in_portfolio(symbol=symbol):

                projected_value[symbol] = {}
                current_quantity = self.positions[symbol]['quantity']
                purchase_price = self.positions[symbol]['purchase_price']
                current_price = current_prices[symbol]['lastPrice']
                is_profitable = self.is_profitable(symbol=symbol, current_price=current_price)

                projected_value[symbol]['purchase_price'] = purchase_price
                projected_value[symbol]['current_price'] = current_prices[symbol]['lastPrice']
                projected_value[symbol]['quantity'] = current_quantity
                projected_value[symbol]['is_profitable'] = is_profitable
                projected_value[symbol]['total_market_value'] = (current_price * current_quantity)
                projected_value[symbol]['total_invested_capital'] = (current_quantity * purchase_price)
                projected_value[symbol]['total_loss_or_gain_$'] = (current_price - purchase_price) * current_quantity
                projected_value[symbol]['total_loss_or_gain_%'] = round(((current_price - purchase_price) / purchase_price),4)

                total_value += projected_value[symbol]['total_market_value']
                total_profit_or_loss += projected_value[symbol]['total_loss_or_gain_$']
                total_invested_capital += projected_value[symbol]['total_invested_capital']

                if projected_value[symbol]['total_loss_or_gain_$'] > 0:
                    position_count_profitable += 1
                elif projected_value[symbol]['total_loss_or_gain_$'] < 0:
                    position_count_not_profitable += 1
                else:
                    position_count_break_even += 1

        projected_value['total_positions'] = len(self.positions)
        projected_value['total_market_value'] = total_value
        projected_value['total_invested_capital'] = total_invested_capital
        projected_value['total_profit_or_loss'] = total_profit_or_loss
        projected_value['number_of_profitable_positions'] = position_count_profitable
        projected_value['number_of_non_profitable_positions'] = position_count_not_profitable
        projected_value['number_of_breakeven_positions'] = position_count_break_even

        return projected_value








