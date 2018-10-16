import binascii
from SSSA import sssa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



def recover_mnemonic(password,secrets):
    shares = []
    # type(secrets)
    key = binascii.unhexlify(password)
    for secret in secrets:
        data = binascii.unhexlify(secret)
        nonce, tag = data[:12], data[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        shares.append(cipher.decrypt_and_verify(data[12:-16], tag))
    sss = sssa()
    mnemonic = sss.combine(shares)
    return mnemonic


def generate_aes_key(number_of_bytes):
    return get_random_bytes(number_of_bytes)

def aes_encrypt(key, file_bytes):
    ##The nonce and the tag generated will be exactly 16 bytes
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(file_bytes)
    nonce = cipher.nonce
    return ciphertext, tag, nonce


def aes_decrypt(key, ciphertext):
    tag, nonce = ciphertext[:16], ciphertext[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    decrypted_text = cipher.decrypt_and_verify(ciphertext[16:-16], tag)
    return decrypted_text




