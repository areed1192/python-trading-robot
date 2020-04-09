
class Portfolio():

    def __init__(self, account_number = None):
        
        self.positions = {}
        self.positions_count = 0
        self.market_value = 0
        self.profit_loss = 0
        self.risk_tolerance = 0
        self.account_number = account_number

    def add_positions(self, positions = None):
        pass

    def add_position(self, symbol = None, quantity = None, purchase_price = None, asset_type = None, purchase_date = None):
        '''
            Adds a single position to the portfolio

            NAME: symbol
            DESC: The Symbol of the Financial Instrument. Example: ['AAPL', '/ES']
            TYPE: String

            NAME: quantity
            DESC: The quantity of the position you own.
            TYPE: Integer

            NAME: purchase_price
            DESC: The price at which the position was purchased.
            TYPE: Float

            NAME: purchase_date
            DESC: The date which the asset was purchased. Must be ISO Format "YYYY-MM-DD"
            TYPE: String

            NAME: asset_type
            DESC: The Asset type of the financial instrument.
            TYPE: String
        '''
        
        self.positions[symbol] = {}
        self.positions[symbol]['quantity'] = quantity
        self.positions[symbol]['purchase_price'] = purchase_price
        self.positions[symbol]['purchase_date'] = purchase_date
        self.positions[symbol]['asset_type'] = asset_type

    def remove_position(self, symbol = None):
        '''
            Deletes a single position from the portfolio
            using the symbol.

            NAME: symbol
            DESC: The Symbol of the Financial Instrument. Example: ['AAPL', '/ES']
            TYPE: String
        '''
        
        if symbol in self.positions:
            del self.positions[symbol]

    def total_allocation(self):

        total_allocation = {
            'stocks':[],
            'fixed_income':[],
            'options':[],
            'futures':[],
            'furex':[]
        }
        
        if len(self.positions.keys()) > 0:
            for symbol in self.positions:
                total_allocation[self.positions[symbol]['asset_type']]

    def risk_exposure(self):
        pass

    def portfolio_summary(self):
        pass
    
    def own_position(self, symbol = None):

        if symbol in self.positions:
            return True
        else:
            return False

    def is_porfitable(self, symbol = None, current_price = None):
        
        if symbol in self.positions and self.positions[symbol]['purchase_price'] < current_price:
            return True
        elif symbol in self.positions and self.positions[symbol]['purchase_price'] > current_price:
            return False
        elif symbol in self.positions and self.positions[symbol]['purchase_price'] == current_price:
            return True
        else:
            return None

    def projected_market_value(self):
        pass


