import asyncio
from api import messaging

# import requests
# from sanic import Blueprint,request
# from sanic import response
from proto import accounts_pb2
from proto import payload_pb2
from proto import newaccount_pb2
# from sanic.response import json
from api import messaging
from db import auth_query
from api import encryption
from api import addresses
from google.protobuf.json_format import MessageToDict
# print(MessageToDict)
from ast import literal_eval

async def get_account_details(request):

    details = await auth_query.fetch_info_by_email(request.app.config.DB_CONN,request.json["user_id"])
    
    secrets = details[0]["secrets"]
    email=details[0]["email"]
    public_key = details[0]["public_key"]
    password=request.json["password"]
    address = addresses.make_account_address(account_id=public_key)
    
    mnemonic = encryption.recover_mnemonic(password,secrets)

    account = await messaging.get_account_state(address,request)
    print(account)
    account =  account_deserialization(account)

    return mnemonic, address, account




def account_deserialization(state_data):
    """
    COnverts data from json data fetched from sawtooth rest api to
    account dict.
    """

    # account = accounts_pb2.Account()
    # # print(type(account))
    # account.ParseFromString(state_data)
    # return  MessageToDict(account, preserving_proto_field_name=True)
    state_data = state_data.decode("utf-8")
    state_data =literal_eval(state_data)

    return state_data