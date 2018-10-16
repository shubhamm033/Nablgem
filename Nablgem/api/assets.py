import bcrypt
import requests
from itsdangerous import BadSignature

import json
from sanic import Blueprint,request
from sanic import response

from sanic.response import json
import rethinkdb as r
import base64
import binascii

from sawtooth_signing import CryptoFactory

from db import accounts_query
from db import auth_query
from db import asset_query

from sawtooth_signing import CryptoFactory
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from transaction import transaction_creation
from sawtooth_signing import create_context

from api import encryption 
from api import remote_api
from api.authorization import authorized
from api import common
from api import messaging
from api.errors import ApiBadRequest
from api.errors import ApiInternalError
from api import common
from api import accounts_utils
from api import amazon_s3


ASSETS_BP = Blueprint('assets',url_prefix='/assets')

@ASSETS_BP.route("/",methods=["POST"])
async def generate_asset_address(request):
    
    required_fields = ["user_id","password"]

    common.validate_fields(required_fields,request.json)

    mnemonic, address, account = await accounts_utils.get_account_details(request)
    # print(type(account))
    childkey_index = common.gen_childkey_index()
    
    if "keys" in account.keys():
        while childkey_index in account["keys"]:
            childkey_index = common.gen_childkey_index()
        
    else:
        childkey_index = common.gen_childkey_index()

    child_private_key,child_public_key = await remote_api.get_child_key(mnemonic,childkey_index)
    
    private_hex_key,public_hex_key = await remote_api.get_child_key(mnemonic,request.app.config.ROOT_KEY_INDEX) 



    private_key = Secp256k1PrivateKey.from_hex(private_hex_key)
    # private_key = request.app.config.CONTEXT.new_random_private_key()
    signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    public_key = signer.get_public_key().as_hex()

    batches, batch_id,batch_list_bytes = transaction_creation.create_empty_asset(
        txn_key=signer,
        batch_key=request.app.config.SIGNER,
        key_index =  childkey_index,
        child_public_key = child_public_key,
        is_empty_asset = True
        )
    
    # print(batch_list_bytes)

    
    data = await messaging.send(batch_list_bytes,request)
    

    try:
        await messaging.wait_for_status(batch_id,300,request)
    except (ApiBadRequest, ApiInternalError) as err:
        raise err


    token = common.generate_auth_token(
        request.app.config.SECRET_KEY,
        child_private_key,
        public_key)
    # print(token)
    return response.json(
        {
            'authorization': token,
            'key_index': childkey_index
        })


@ASSETS_BP.route("/create",methods=["POST"])
async def create_asset(request):
    
    required_fields = ["user_id","password","file_name","file_hash","base64_file_bytes"]

    common.validate_fields(required_fields,request.json)

    file_exist = await asset_query.fetch_info_by_filehash(request.app.config.DB_CONN,request.json["file_hash"])
    
    if file_exist:
        raise ApiInternalError("file already exist. Try again later")


    file_bytes = base64.b64decode(request.json["base64_file_bytes"])

    mnemonic, address, account = await accounts_utils.get_account_details(request)

    childkey_index =common.gen_childkey_index()



    child_private_key,child_public_key = await remote_api.get_child_key(mnemonic,childkey_index)
    
    private_hex_key,public_hex_key = await remote_api.get_child_key(mnemonic,request.app.config.ROOT_KEY_INDEX) 

    private_key = Secp256k1PrivateKey.from_hex(private_hex_key)
    
    signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    public_key = signer.get_public_key().as_hex()

    
    aes_key = encryption.generate_aes_key(16)

    ciphertext,tag,nonce = encryption.aes_encrypt(aes_key,file_bytes)

    ciphertext = b"".join([tag,ciphertext,nonce])
    
    secrets = binascii.hexlify(ciphertext)
    
    struct ={
        "file_hash": request.json["file_hash"],
        "file_name": request.json["file_name"],
        "file_cipher_hex": secrets.decode()
        
    }

    s3_key = amazon_s3.generate_s3_key(request.json["user_id"],request.json["file_name"])
    s3_url = amazon_s3.store_s3(request,s3_key,request.json["user_id"],struct)
    
    

    





































    


    
    
    





    








    # batches, batch_id,batch_list_bytes =  transaction_creation.create_account(

    



def _create_asset_dict(body,s3_url,s3_key,childkey_index):

    keys = ["user_id","password","file_name","file_hash","base64_file_bytes"]

    account = {k: body[k] for k in keys if body.get(k) is not None}

    account["s3_url"] = s3_url
    account["s3_key"] = s3_key
    account["childkey_index"] = [childkey_index]
     
    return account 
     






    
 










    




        
    


    


    