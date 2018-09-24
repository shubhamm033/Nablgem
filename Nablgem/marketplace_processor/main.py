import hashlib
import logging

import handler
from marketplace_payload import MarketplacePayload
from marketplace_state import MarketplaceState
import accounts

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

LOGGER = logging.getLogger(__name__)

FAMILY_NAME = "marketplace"

def _hash(data):
    '''Compute the SHA-512 hash and return the result as hex characters.'''
    return hashlib.sha512(data).hexdigest()

sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

class MarketplaceTransactionHandler(TransactionHandler):
    '''                                                       
    Transaction P\rocessor class for the simplewallet transaction family.       
                                                              
    This with the validator using the accept/get/set functions.
    It implements functions to deposit, withdraw, and transfer money.
    '''

    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        '''This implements the apply function for this transaction handler.
                                                              
           This function does most of the work for this class by processing
           a single transaction for the simplewallet transaction family.   
        '''                                                   
        # print(transaction.header)
        # print(transaction.payload)
        state = MarketplaceState(context=context)
        payload = MarketplacePayload(payload=transaction.payload)

        # print(payload.create_account())

        # if payload.is_create_account():
        accounts.handle_account_creation(
            payload.create_account(),
            header=transaction.header,
            state=state)
    # Get the payload and extract simplewallet-specific information.
    
        # header = transaction.header
        # payload_list = transaction.payload.decode().split(",")
        
        # o~peration = payload_list[0]
        # amount = payload_list[1]

        # Get the public key sent from the client.
        # from_key = header.signer_public_key




def setup_loggers():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

def main():
    '''Entry-point function for the simplewallet transaction processor.'''
    setup_loggers()
    try:
        # Register the transaction handler and start it.
        processor = TransactionProcessor(url='tcp://localhost:4004')

        handler = MarketplaceTransactionHandler(sw_namespace)

        processor.add_handler(handler)

        processor.start()

    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    # except BaseException as err:
    #     traceback.print_exc(file=sys.stderr)
    #     sys.exit(1)

if __name__ =="__main__":
    main()