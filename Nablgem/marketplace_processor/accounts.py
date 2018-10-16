from sawtooth_sdk.processor.exceptions import InvalidTransaction


def handle_account_creation(create_account, header, state):
    """Handles creating an Account.
    Args:
        create_account (CreateAccount): The transaction.
        header (TransactionHeader): The header of the Transaction.
        state (MarketplaceState): The wrapper around the Context.
    Raises:
        InvalidTransaction
            - The public key already exists for an Account.
    """

    # if state.get_account(public_key=header.signer_public_key):
        
    #     raise InvalidTransaction("Account with public key {} already "
    #                              "exists".format(header.signer_public_key))
    

    state.set_account(
        public_key=header.signer_public_key,
        email=create_account.email,
        phone_number=create_account.phone_number,
        user_type =create_account.user_type,
        pan_card_number =create_account.pan_card_number,
        user_id= create_account.user_id,
        first_name = create_account.first_name,
        last_name = create_account.last_name,
        adhaar=create_account.adhaar
        )


