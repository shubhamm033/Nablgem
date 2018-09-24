import requests
import os
import json
import hashlib
import binascii
from SSSA import sssa
from Crypto.Cipher import AES
from os.path import expanduser


from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory





FAMILY_NAME = "User registration"
ip ="52.66.22.183"

HOME_DIRECTORY = expanduser("~")
PATH = "%s/.sawtooth/keys"%HOME_DIRECTORY
if not os.path.exists(PATH):
    os.makedirs(PATH)




def _hash(data):
    return hashlib.sha512(data).hexdigest()

def registration(email,phone_number):
    
    try:
        r = requests.post("http://%s/registration"%ip,  data=json.dumps({"email": email, "phone_number": phone_number}))
        
        
        with open("%s/user_id.txt"%PATH ,"w+") as f:
            user_id = r.json()["data"]["user_id"]  
            f.write(user_id)    
        return r.json()["data"]["user_id"], r.json()["data"]["password"]

    except Exception as e:
        return json.dumps({"success":False,"error":str(e)})




def mnemonic(email,phone_number,password):        
    
    
    r = requests.post("http://%s/getkeys"%ip,  data=json.dumps({"email": email, "phone_number": phone_number}))
    shares=[]
    
    try:
        key = binascii.unhexlify(password)
        for secret in r.json()["data"].keys():
            data = binascii.unhexlify(r.json()["data"][secret])
            nonce, tag = data[:12], data[-16:]
            cipher = AES.new(key, AES.MODE_GCM, nonce)
            shares.append(cipher.decrypt_and_verify(data[12:-16], tag))

    except Exception as e:
        return json.dumps({"success":False,"error":str(e)})
        
    sss = sssa()
    mnemonic = sss.combine(shares)
    
    return mnemonic
        
    

# p = registration("paper10@gmail.com","9198013772")
# q = Mnemonic("paper10@gmail.com","9198013772","5427a238806999da39fb1173afc02e324eb5092905df61a312c7657da363f210")
# print(q)

def recover_master_keys(mnemonic):
    r = requests.post("http://%s/master_mnemonic_keys"%ip,  data=json.dumps({"mnemonic": mnemonic}))
    return r.json()["data"]["master_private_key"], r.json()["data"]["master_public_key"]



def recover_child_keys(mnemonic, index):
    r = requests.post("http://%s/child_mnemonic_keys"%ip,  data=json.dumps({"mnemonic": mnemonic, "child_key_index": index}))
    

    with open("%s/user_id.txt"%PATH, 'r+') as f:
        user_id = f.read()
    print ("THis is the user id %s"%user_id)

    with open("%s/%s.priv"%(PATH, user_id), 'w+') as f:
        f.write(r.json()["data"]["child_private_key"])

    with open("%s/%s.pub"%(PATH, user_id), 'w+') as f:
        f.write(r.json()["data"]["child_public_key"])


    with open("%s/%s.key_child_index"%(PATH, user_id), 'w+') as f:
        f.write(str(index))

    return r.json()["data"]["child_private_key"], r.json()["data"]["child_public_key"]




# class UserRegistration(object):

#     def __init__(self, baseUrl, keyFile=None):
#         '''Initialize the client class.

#            This is mainly getting the key pair and computing the address.
#         '''

#         self._baseUrl = baseUrl

#         if keyFile is None:
#             self._signer = None
#             return

#         try:
#             with open(keyFile) as fd:
#                 privateKeyStr = fd.read().strip()
#         except OSError as err:
#             raise Exception('Failed to read private key {}: {}'.format(
#                 keyFile, str(err)))

        
        
        








            










# UserRegistration("art distance random latin ranch canal mouse mirror whisper broom rotate door wheat toddler mirror recipe friend hill life early staff betray fit fit",1)






























