from addressing import addresses

from transaction.common import make_header_and_batch
from proto import payload_pb2 


def create_account(txn_key, batch_key,email,phone_number,adhaar,pancard,first_name,last_name,user_type,user_id,keys):


# def create_account(txn_key, batch_key):
    """Create a CreateAccount txn and wrap it in a batch and list.
    Args:
        txn_key (sawtooth_signing.Signer): The Txn signer key pair.
        batch_key (sawtooth_signing.Signer): The Batch signer key pair.
        label (str): The account's label.
        description (str): The description of the account.
    Returns:
        tuple: List of Batch, signature tuple
    """

    inputs = [addresses.make_account_address(
        account_id=txn_key.get_public_key().as_hex())]

    outputs = [addresses.make_account_address(
        account_id=txn_key.get_public_key().as_hex())]

    account = payload_pb2.CreateAccount(
        email=email,
        phone_number=phone_number,
        user_type = user_type,
        pan_card_number=pancard,
        user_id = user_id,
        first_name= first_name,
        last_name= last_name,
        key_indexes=keys,
        adhaar = adhaar
        
        )
    # print(account)
    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_ACCOUNT,
        create_account=account)
    # print(payload)
    return make_header_and_batch(
        payload=payload,
        inputs=inputs,
        outputs=outputs,
        txn_key=txn_key,
        batch_key=batch_key)




def create_empty_asset(txn_key, batch_key,key_index,child_public_key,is_empty_asset):

    inputs = [addresses.make_asset_address(
        asset_id=child_public_key),
        addresses.make_account_address(account_id=txn_key.get_public_key().as_hex())]

    outputs = [addresses.make_asset_address(
        asset_id= child_public_key),
        addresses.make_account_address(account_id=txn_key.get_public_key().as_hex())]

    asset = payload_pb2.CreateAsset(
        child_public_key = child_public_key,
        child_key_index =key_index,
        is_empty_asset =True 
        )
    
    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_ASSET,
        create_asset=asset)
    # print(payload)
    return make_header_and_batch(
        payload=payload,
        inputs=inputs,
        outputs=outputs,
        txn_key=txn_key,
        batch_key=batch_key)


