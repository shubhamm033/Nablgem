import requests
import json
import binascii
from SSSA import sssa
from faker import Faker
from Crypto.Cipher import AES



ip_port= "52.66.22.183"

faker = Faker()

email, phone_number = faker.email(), faker.phone_number()

print ("Trying to register user with email {} and phone_number {}".format(email, phone_number))

r = requests.post("http://%s/registration"%ip_port,  data=json.dumps({"email": email, "phone_number": phone_number, "junkone": faker.paragraph(), "junk_two": faker.paragraph()}))
user_id = r.json()["data"]["user_id"]
password = r.json()["data"]["password"]

print ("User with user id {} has been created, password is {}".format(user_id, password))


r = requests.post("http://%s/getkeys"%ip_port,  data=json.dumps({"email": email, "phone_number": phone_number}))


print ("Hex ecndoed secrets which are received\n")
print ("Secret One")
print (r.json()["data"]["secret_one"], "\n")
print ("Secret Two")
print (r.json()["data"]["secret_two"], "\n")
print ("Secret Three")
print (r.json()["data"]["secret_three"], "\n")


shares = []



##hex decoding the password
key = binascii.unhexlify(password)
for secret in r.json()["data"].keys():
    data = binascii.unhexlify(r.json()["data"][secret])
    nonce, tag = data[:12], data[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    shares.append(cipher.decrypt_and_verify(data[12:-16], tag))


print (shares)
sss = sssa()
mnemonic = sss.combine(shares)

print (mnemonic)

