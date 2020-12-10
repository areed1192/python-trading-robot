from pyrobot.trades import Trade
from td.client import TDClient

class OrderStatus():

    def __init__(self, trade_obj: Trade) -> None:

        self.trade_obj = trade_obj
        self.order_status = self.trade_obj.order_status

    @property
    def is_cancelled(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order was filled or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `FILLED`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'FILLED':
            return True
        else:
            return False

    @property
    def is_rejected(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order was rejected or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `REJECTED`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'REJECTED':
            return True
        else:
            return False

    @property
    def is_expired(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order has expired or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `EXPIRED`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'EXPIRED':
            return True
        else:
            return False

    @property
    def is_replaced(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order has been replaced or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `REPLACED`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'REPLACED':
            return True
        else:
            return False

    @property
    def is_working(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is working or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `WORKING`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'WORKING':
            return True
        else:
            return False

    @property
    def is_pending_activation(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is pending activation or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `PENDING_ACTIVATION`, 
            `False` otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'PENDING_ACTIVATION':
            return True
        else:
            return False

    @property
    def is_pending_cancel(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is pending cancellation or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `PENDING_CANCEL`, 
            `False` otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'PENDING_CANCEL':
            return True
        else:
            return False

    @property
    def is_pending_replace(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is pending replacement or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `PENDING_REPLACE`, 
            `False` otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'PENDING_REPLACE':
            return True
        else:
            return False

    @property
    def is_queued(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is in the queue or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `QUEUED`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'QUEUED':
            return True
        else:
            return False

    @property
    def is_accepted(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order was accepted or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `ACCEPTED`, `False`
            otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'ACCEPTED':
            return True
        else:
            return False

    @property
    def is_awaiting_parent_order(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is waiting for the parent order
        to execute or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `AWAITING_PARENT_ORDER`,
            `False` otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'AWAITING_PARENT_ORDER':
            return True
        else:
            return False

    @property
    def is_awaiting_condition(self, refresh_order_info: bool = True) -> bool:
        """Specifies whether the order is waiting for the condition
        to execute or not.

        Arguments:
        ----
        refresh_order_info {bool} -- Specifies whether you want
            to refresh the order data from the TD API before 
            checking. If `True` a request will be made to the
            TD API to grab the latest Order Info.

        Returns
        -------
        bool
            `True` if the order status is `AWAITING_CONDITION`,
            `False` otherwise.
        """

        if refresh_order_info:
            self.trade_obj._update_order_status()

        if self.order_status == 'AWAITING_CONDITION':
            return True
        else:
            return False