from td.client import TDClient


class PyRobot():

    def __init__(self, account_username = None, account_password = None, consumer_id = None, redirect_uri = None, json_path = None):
        '''
            Initalizes a new instance of the robot and logs into the API platform specified.

            NAME: consumer_id
            DESC: The Consumer ID assigned to you during the App registration. This can
                  be found at the app registration portal.
            TYPE: String

            NAME: account_number
            DESC: This is the account number for your main TD Ameritrade Account.
            TYPE: String

            NAME: account_password
            DESC: This is the account password for your main TD Ameritrade Account.
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
        self.consumer_id = consumer_id
        self.account_username = account_username
        self.account_password = account_password
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
        td_client = TDClient(account_number = self.account_password, account_password = self.account_password, consumer_id = self.consumer_id, redirect_uri = self.redirect_uri, json_path = self.json_path)

        # log the client into the new session
        td_client.login()

        return td_client

    def create_portfolio(self, account_number = None):
        pass

    def create_trade(self):
        pass

    def delete_trade(self):
        pass
