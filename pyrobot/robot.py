from td.client import TDClient
from datetime import datetime, time, timezone
from pyrobot.portfolio import Portfolio

class PyRobot():

    def __init__(self, trading_account = None, consumer_id = None, redirect_uri = None, json_path = None):
        '''
            Initalizes a new instance of the robot and logs into the API platform specified.

            NAME: trading_account
            DESC: This is the account number for your main TD Ameritrade Account.
            TYPE: String

            NAME: consumer_id
            DESC: The Consumer ID assigned to you during the App registration. This can
                  be found at the app registration portal.
            TYPE: String

            NAME: redirect_uri
            DESC: This is the redirect URL that you specified when you created your
                  TD Ameritrade Application.    
            TYPE: String

            NAME: json_path
            DESC: The path to the session state file used to prevent a full 
                  OAuth workflow.   
            TYPE: String
        '''

        # Set the attirbutes
        self.trading_account = trading_account
        self.consumer_id = consumer_id
        self.redirect_uri = redirect_uri
        self.json_path = json_path
        self.session = self._create_session()
        self.trades = {}

    def _create_session(self):
        '''
            Creates a new session with the TD Ameritrade API and logs the user into
            the new session.

            RTYPE: td.TDClient
        '''

        # Create a new instance of the client
        td_client = TDClient(account_number = self.trading_account, consumer_id = self.consumer_id, redirect_uri = self.redirect_uri, json_path = self.json_path)

        # log the client into the new session
        td_client.login()

        return td_client
    
    @property
    def pre_market_open(self):
        '''
            Returns whether we are in pre-market trading or not.

            RTYPE: Boolean
        '''

        pre_market_start_time = datetime.now().replace(hour = 12, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()
        market_start_time = datetime.now().replace(hour = 13, minute = 30, second = 00, tzinfo = timezone.utc).timestamp()
        right_now = datetime.now().replace(tzinfo = timezone.utc).timestamp()

        if market_start_time >= right_now >= pre_market_start_time:
            return True
        else:
            return False


    @property
    def post_market_open(self):
        '''
            Returns whether we are in after-hours trading or not.

            RTYPE: Boolean
        '''

        post_market_end_time = datetime.now().replace(hour = 22, minute = 30, second = 00, tzinfo = timezone.utc).timestamp()
        market_end_time = datetime.now().replace(hour = 20, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()
        right_now = datetime.now().replace(tzinfo = timezone.utc).timestamp()

        if post_market_end_time >= right_now >= market_end_time:
            return True
        else:
            return False

    @property
    def regular_market_open(self):
        '''
            Returns whether we are in after-hours trading or not.

            RTYPE: Boolean
        '''

        market_start_time = datetime.now().replace(hour = 13, minute = 30, second = 00, tzinfo = timezone.utc).timestamp()
        market_end_time = datetime.now().replace(hour = 20, minute = 00, second = 00, tzinfo = timezone.utc).timestamp()
        right_now = datetime.now().replace(tzinfo = timezone.utc).timestamp()

        if market_end_time >= right_now >= market_start_time:
            return True
        else:
            return False

    def create_portfolio(self):
        '''
            Creates a Portfolio Object to help store and organize positions
            as they are added and removed during trading.

            RTYPE: pyrobot.Portfolio
        '''        

        # Initalize the portfolio.
        self.portfolio = Portfolio(account_number = self.trading_account)

        return self.portfolio

    def create_trade(self):
        pass

    def delete_trade(self):
        pass

    def grab_current_quotes(self):
        '''
            Grabs current quotes for all the positions in the portfolios.

            RTYPE: Dictionary
        '''

        # First grab all the symbols.
        symbols = self.portfolio.positions.keys()

        # Grab the quotes.
        quotes = self.session.get_quotes(instruments = list(symbols))

        return quotes
