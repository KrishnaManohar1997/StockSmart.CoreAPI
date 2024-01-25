from common.constants.base_enum import BaseEnum


class TransactionIntent(BaseEnum):
    # To create a transactionId for single stock or basket orders
    TRANSACTION = "TRANSACTION"
    # Used for Connecting/LOGIN
    CONNECT = "CONNECT"
    # Import the Holdings of the User
    HOLDINGS_IMPORT = "HOLDINGS_IMPORT"
