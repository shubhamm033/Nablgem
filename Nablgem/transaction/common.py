import hashlib
from uuid import uuid4

from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import transaction_pb2

# from sawtooth_rest_api.protobuf import batch_pb2
# from sawtooth_rest_api.protobuf import transaction_pb2



from addressing import addresses

from sawtooth_sdk.protobuf.batch_pb2 import BatchList
# print(BatchList)

def wrap_payload_in_txn_batch(txn_key, payload, header, batch_key):
    """Takes the serialized RBACPayload and creates a batch_list, batch
    signature tuple.
    Args:
        txn_key (sawtooth_signing.Signer): The txn signer's key pair.
        payload (bytes): The serialized RBACPayload.
        header (bytes): The serialized TransactionHeader.
        batch_key (sawtooth_signing.Signer): The batch signer's key pair.
    Returns:
        tuple
            The zeroth element is a BatchList, and the first element is
            the batch header_signature.
    """

    transaction = transaction_pb2.Transaction(
        payload=payload,
        header=header,
        header_signature=txn_key.sign(header))
    print(txn_key.sign(header))
    batch_header = batch_pb2.BatchHeader(
        signer_public_key=batch_key.get_public_key().as_hex(),
        transaction_ids=[transaction.header_signature]).SerializeToString()

    batch = batch_pb2.Batch(
        header=batch_header,
        header_signature=batch_key.sign(batch_header),
        transactions=[transaction])

    batch_list_bytes = BatchList(batches=[batch]).SerializeToString()
       
    return [batch], batch.header_signature, batch_list_bytes
      

def make_header_and_batch(payload, inputs, outputs, txn_key, batch_key):

    header = make_header(
        inputs=inputs,
        outputs=outputs,
        payload_sha512=hashlib.sha512(
            payload.SerializeToString()).hexdigest(),
        signer_pubkey=txn_key.get_public_key().as_hex(),
        batcher_pubkey=batch_key.get_public_key().as_hex())

    return wrap_payload_in_txn_batch(
        txn_key=txn_key,
        payload=payload.SerializeToString(),
        header=header.SerializeToString(),
        batch_key=batch_key)


def make_header(inputs,
                outputs,
                payload_sha512,
                signer_pubkey,
                batcher_pubkey):
    header = transaction_pb2.TransactionHeader(
        inputs=inputs,
        outputs=outputs,
        batcher_public_key=batcher_pubkey,
        dependencies=[],
        family_name=addresses.FAMILY_NAME,
        family_version='1.0',
        nonce=uuid4().hex,
        signer_public_key=signer_pubkey,
        payload_sha512=payload_sha512)
    return header
