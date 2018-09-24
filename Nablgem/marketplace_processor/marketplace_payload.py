

import payload_pb2


class MarketplacePayload(object):

    def __init__(self, payload):
        self._transaction = payload_pb2.TransactionPayload()
        # print(self._transaction)
        self._transaction.ParseFromString(payload)
        # print(self._transaction)

    def create_account(self):
        """Returns the value set in the create_account.
        Returns:
            payload_pb2.CreateAccount
        """

        return self._transaction.create_account

    def is_create_account(self):

        create_account = payload_pb2.TransactionPayload.CREATE_ACCOUNT
        # print(self._transaction.payload_type)
        # print(create_account)
        return self._transaction.payload_type == create_account
