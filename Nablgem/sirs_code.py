# import hashlib
# import base64
# import random
# import requests
# import binascii
# import yaml
# import json
# from SSSA import sssa

# from sawtooth_signing import create_context
# from Crypto.Cipher import AES
# from sawtooth_signing import CryptoFactory
# from sawtooth_signing import ParseError
# from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

# from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
# from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
# from sawtooth_sdk.protobuf.batch_pb2 import BatchList
# from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
# from sawtooth_sdk.protobuf.batch_pb2 import Batch

# # The Transaction Family Name
# FAMILY_NAME = 'simplewallet'
# API_ADDRESS = "52.66.22.183"

# def _hash(data):
#     return hashlib.sha512(data).hexdigest()


# def registration(email, phone_number):
#     r = requests.post("http://%s/registration"%API_ADDRESS,
#                             data=json.dumps({"email": email,
#                             "phone_number": phone_number}))
#     if r.json()["success"]:
#         print(r.json()["data"]["password"])
#         return r.json()["data"]["password"], r.json()["data"]["user_id"]

#     else:
#         return False, False

# def mnemonic(email, phone_number, password):
#     r = requests.post("http://%s/getkeys"%API_ADDRESS,  data=json.dumps({"email": email, "phone_number": phone_number}))
#     shares = []
#     ##hex decoding the password
#     try:
#         key = binascii.unhexlify(password)
#         # key =password
#     except Exception:
#         return "Wrong Password: Please ensure you are providing the right password"
#     for secret in r.json()["data"].keys():
#         data = binascii.unhexlify(r.json()["data"][secret])
#         nonce, tag = data[:12], data[-16:]
#         try:
#             cipher = AES.new(key, AES.MODE_GCM, nonce)
#             shares.append(cipher.decrypt_and_verify(data[12:-16], tag))
#         except Exception:
#             return "Wrong Password: Please ensure you are providing the right password"
#     sss = sssa()
#     _mnemonic = sss.combine(shares)
#     return _mnemonic


# # q=registration("paper9@gmail.com","9198013772")
# p = mnemonic("paper9@gmail.com","9198013772","874b8d1e272e5007565e7c1f29b6ca1621f33d185fffba49796aa92861b377e6")
# print(p)


# import os 


# config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"config.py")


# print(config_file_path)

from sanic import Sanic, Blueprint
from sanic.response import text, json

app = Sanic()

failing_bp = Blueprint('failing_blueprint', url_prefix='/api/failing')

# @failing_bp.get("/")
# async def get_data(request):
#     return json({
#         "hello": "world",
#         "I am working if": "you see me",
#         "from": "the failing blueprint"
#     })

@failing_bp.post("/")
async def post_data(request):
    # print(request.body)
    # print(request.headers)
    return json("POST [FAILING] - {}\n\n{}".format(
        request.headers,
        request.body
    ))

if __name__ == "__main__":
    app.blueprint(failing_bp)

    app.run(debug=True, host="0.0.0.0", port=7000)

