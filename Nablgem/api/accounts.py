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


from api import accounts_utils
from api import encryption 
from api import remote_api
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



@ACCOUNTS_BP.route('/login',methods = ["POST"])
async def login_account(request):

    required_fields =["user_id","password"]

    # common.validate_fields(required_fields,request.json)
    # user_id= request.json["user_id"]
    # password= request.json["password"]
    # print(request.json)
    mnemonic, address, account = await accounts_utils.get_account_details(request)
    print(account)

    return  response.json({"account":account})

@ACCOUNTS_BP.route("/",methods=["POST"])
async def create_account(request):
    
    # print(request.app.config)
    # print(request.json)
    required_fields = ['email','phone_number',"adhaar","pancard","first_name","last_name","user_type"]
    # print(request.json)

    common.validate_fields(required_fields, request.json)
       
    user_id, password, secrets = await remote_api.registration(request)
    # print(secrets)
    print(user_id)
    print(password)
    mnemonic = encryption.recover_mnemonic(password,secrets)
    
    # print(mnemonic)

    private_hex_key,public_hex_key = await remote_api.get_child_key(mnemonic,request.app.config.ROOT_KEY_INDEX) 

    






    private_key = Secp256k1PrivateKey.from_hex(private_hex_key)
    # private_key = request.app.config.CONTEXT.new_random_private_key()
    signer = CryptoFactory(request.app.config.CONTEXT).new_signer(private_key)
    public_key = signer.get_public_key().as_hex()
    # print(public_key)
    
    # return json({"main":1})    
    auth_entry  =  _create_auth_dict(
        request, public_key, private_key.as_hex(),secrets,user_id)
    # print(auth_entry)
    # print(request.app.config.DB_CONN)
    database_entry = await auth_query.create_auth_entry(request.app.config.DB_CONN, auth_entry)
    # details = await auth_query.fetch_info_by_email(request.app.config.DB_CONN,user_id)
    # print(request.app.config.DB_CONN)
    # print(details)
    
    # type(email_details)
    account =  _create_account_dict(request.json, public_key,user_id)
    
    # print(account)
    batches, batch_id,batch_list_bytes =  transaction_creation.create_account(
        txn_key=signer,
        batch_key=request.app.config.SIGNER,
        email=account['email'],
        phone_number=account["phone_number"],
        adhaar= account["adhaar"],
        pancard=account["pancard"],
        first_name= account["first_name"],
        last_name=account["last_name"],
        user_type=account["user_type"],
        user_id=account["user_id"],
        keys= []
        )
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




def _create_account_dict(body, public_key,user_id):
    keys = ['email',"phone_number","adhaar","pancard","first_name","last_name","user_type"]

    account = {k: body[k] for k in keys if body.get(k) is not None}

    account['publicKey'] = public_key
    account["user_id"] = user_id
     # account['holdings'] = []

    return account


def _create_auth_dict(request, public_key, private_key,secrets,user_id):
    auth_entry = {
        'public_key': public_key,
        'email': request.json['email'],
        "secrets": secrets,
        "user_id":user_id
    }

    # auth_entry['encrypted_private_key'] = common.encrypt_private_key(
    #     request.app.config.AES_KEY, public_key, private_key)
    # auth_entry['hashed_password'] = bcrypt.hashpw(
    #     bytes(request.json.get('password'), 'utf-8'), bcrypt.gensalt())

    return auth_entry








