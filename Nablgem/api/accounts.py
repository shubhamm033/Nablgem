import bcrypt
import requests
from itsdangerous import BadSignature

import json
from sanic import Blueprint,request
from sanic import response

from sanic.response import json
import rethinkdb as r

from sawtooth_signing import CryptoFactory

from db import accounts_query
from db import auth_query

from sawtooth_signing import CryptoFactory
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from transaction import transaction_creation
from sawtooth_signing import create_context



from api.authorization import authorized
from api import common
from api import messaging
from api.errors import ApiBadRequest
from api.errors import ApiInternalError

ACCOUNTS_BP = Blueprint('accounts',url_prefix='/accounts')

# @ACCOUNTS_BP.route("/accounts")
# async def create_account(request):
#     print(request.body)
#     print(request.headers)

#     return json({"ok":1})

# @ACCOUNTS_BP.get("accounts/shit")
# async def create_account(request):
    
#     return json({"name":"shabana"})
@ACCOUNTS_BP.route("/",methods=["GET"])
async def create_account(request):
    
    return json({"name":"shabanana"})



@ACCOUNTS_BP.route("/",methods=["POST"])
async def create_account(request):
    
    # print(request.app.config)
    # print(request.json)
    required_fields = ['email', 'phone_number']
    common.validate_fields(required_fields, request.json)
    #   
    # privateKey = Secp256k1PrivateKey.from_hex(privateKeyStr)
    private_key = request.app.config.CONTEXT.new_random_private_key()
    signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    public_key = signer.get_public_key().as_hex()
    # print(public_key)
    
    # return json({"main":1})    
    auth_entry =  _create_auth_dict(
        request, public_key, private_key.as_hex())
    # print(auth_entry)
    # print(request.app.config.DB_CONN)
    await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)
    
    
    account =  _create_account_dict(request.json, public_key)
    # print(account)
    batches, batch_id,batch_list_bytes =  transaction_creation.create_account(
        txn_key=signer,
        batch_key=request.app.config.SIGNER,
        email=account['email'],
        phone_number=account["phone_number"])
    # print(batch_list_bytes)
    # print(batches)
    # print(type(batch_list_bytes))
    # print(type(batch_id))
    # print(batches)
    # await messaging.send(
    #     request.app.config.VAL_CONN,
    #     request.app.config.TIMEOUT,
    #     batches)
    
    data = await messaging.send(batch_list_bytes,request)
    # print(data)
    # try:
    #     await messaging.check_batch_status(
    #         request.app.config.VAL_CONN, batch_id)
    # except (ApiBadRequest, ApiInternalError) as err:
    #     await auth_query.remove_auth_entry(
    #         request.app.config.DB_CONN, request.json.get('email'))
    #     raise err
    try:
        await messaging.wait_for_status(batch_id,300,request)
    except (ApiBadRequest, ApiInternalError) as err:
        raise err
    


    token = common.generate_auth_token(
        request.app.config.SECRET_KEY,
        account.get('email'),
        public_key)
    # print(token)
    return response.json(
        {
            'authorization': token,
            'account': account
        })




def _create_account_dict(body, public_key):
    keys = ['email',"phone_number"]

    account = {k: body[k] for k in keys if body.get(k) is not None}

    account['publicKey'] = public_key
    # account['holdings'] = []

    return account


def _create_auth_dict(request, public_key, private_key):
    auth_entry = {
        'public_key': public_key,
        'email': request.json['email']
    }

    # auth_entry['encrypted_private_key'] = common.encrypt_private_key(
    #     request.app.config.AES_KEY, public_key, private_key)
    # auth_entry['hashed_password'] = bcrypt.hashpw(
    #     bytes(request.json.get('password'), 'utf-8'), bcrypt.gensalt())

    return auth_entry








