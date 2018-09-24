
# from addressing import addresses
import accounts_pb2
import addresses

class MarketplaceState(object):

    # def __init__(self, context, timeout=2):
    def __init__(self,context):   
        self._context = context
        # self._state_entries = []
        # self._timeout = timeout
        
        

    def set_account(self, public_key, email,phone_number):
        address = addresses.make_account_address(account_id=public_key)
        # print(address)
        # container = _get_account_container(self._state_entries, address)
        current_entry = self._context.get_state([address])
        # print(current_entry)
        if current_entry == []:
            # print("accounts does not exist, need to create one")
            details= {}
            details["email"] = email
            details["phone_number"] = phone_number
        else:
            print("account exist")

        state_data = str(details).encode('utf-8')
        # print(state_data)
        final_state = self._context.set_state({address: state_data})
        print(final_state)
        if len(final_state) < 1:
            raise InternalError("State Error")



            



        # try:
        #     account = _get_account_from_container(
        #         container,
        #         public_key)
        # except KeyError:
        #     account = container.entries.add()
        # # print("shit")            
        # # account.public_key = public_key
        # account.email = email
        # account.phone_number = phone_number
        # # for holding in holdings:
        #     account.holdings.append(holding)
        # print(account)
        # state_entries_send = {}
        # state_entries_send[address] = container.SerializeToString()
        # print(state_entries_send)
        # print(container)
        # return self._context.set_state(
        #     state_entries_send)
        #     # self._timeout)


    # def get_account(self, public_key):
    #     address = addresses.make_account_address(account_id=public_key)
    #     # print("the address is {}".format(address))
    #     # print(self._context.get_state(
    #         # addresses=[address]))
    #     self._state_entries.extend(self._context.get_state(
    #         [address]))
    #     # print(self._state_entries)    
    #         # timeout=self._timeout))
    #     # print(self._state_entries)
    #     container = _get_account_container(self._state_entries, address)
    #     account = None
    #     try:
    #         account = _get_account_from_container(
    #             container,
    #             identifier=public_key)
    #         # print(account)
    #     except KeyError:
    #         # We are fine with returning None for an account that doesn't
    #         # exist in state.
    #         pass
    #     # print(account)    
    #     return account



# def _get_account_container(state_entries, address):
#     try:
#         entry = _find_in_state(state_entries, address)
#         container = accounts_pb2.AccountContainer()
#         container.ParseFromString(entry.data)
#     except KeyError:
#         container = accounts_pb2.AccountContainer()
#     print(container)
#     return container


# def _get_account_from_container(container, identifier):
#     for account in container.entries:
#         if account.public_key == identifier:
#             return account
#     raise KeyError(
#         "Account with identifier {} is not in container.".format(identifier))


# def _find_in_state(state_entries, address):
#     for entry in state_entries:
#         if entry.address == address:
#             return entry
#     raise KeyError("Address {} not found in state".format(address))