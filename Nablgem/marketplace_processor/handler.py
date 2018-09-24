# # from marketplace_processor.account import account_creation
# # from marketplace_processor.asset import asset_creation
# # from marketplace_processor.holding import holding_creation
# # from marketplace_processor.offer import offer_acceptance
# # from marketplace_processor.offer import offer_closure
# # from marketplace_processor.offer import offer_creation
# # from marketplace_processor.marketplace_payload import MarketplacePayload
# # from marketplace_processor.marketplace_state import MarketplaceState

# from sawtooth_sdk.processor.handler import TransactionHandler

# class MarketplaceTransactionHandler(TransactionHandler):
#     '''                                                       
#     Transaction Processor class for the simplewallet transaction family.       
                                                              
#     This with the validator using the accept/get/set functions.
#     It implements functions to deposit, withdraw, and transfer money.
#     '''

#     def __init__(self, namespace_prefix):
#         self._namespace_prefix = namespace_prefix

#     @property
#     def family_name(self):
#         return FAMILY_NAME

#     @property
#     def family_versions(self):
#         return ['1.0']

#     @property
#     def namespaces(self):
#         return [self._namespace_prefix]

#     def apply(self, transaction, context):
#         '''This implements the apply function for this transaction handler.
                                                              
#            This function does most of the work for this class by processing
#            a single transaction for the simplewallet transaction family.   
#         '''                                                   
        
#         # Get the payload and extract simplewallet-specific information.
#         header = transaction.header
#         payload_list = transaction.payload.decode().split(",")
#         operation = payload_list[0]
#         amount = payload_list[1]

#         # Get the public key sent from the client.
#         from_key = header.signer_public_key

#         # Perform the operation.
#         # LOGGER.info("Operation = "+ operation)

#         # if operation == "deposit":
#         #     self._make_deposit(context, amount, from_key)
#         # elif operation == "withdraw":
#         #     self._make_withdraw(context, amount, from_key)
#         # elif operation == "transfer":
#         #     if len(payload_list) == 3:
#         #         to_key = payload_list[2]
#         #     self._make_transfer(context, amount, to_key, from_key)
#         # else:
#         #     LOGGER.info("Unhandled action. " +
#         #         "Operation should be deposit, withdraw or transfer")
