from cryptography.fernet import Fernet
import base64
from hashlib import sha256
from icecream import ic 

def keyGenerator(s):
    # Passo 1: Hash da string usando SHA-256 para garantir 32 bytes
    hash_bytes = sha256(s.encode('utf-8')).digest()
    
    # Passo 2: Codifica o resultado do hash em base64 para ser usado como chave Fernet
    base64_key = base64.urlsafe_b64encode(hash_bytes)
    
    return base64_key


def encryptSentence(massege, key):
    cypher = Fernet(key)
    encryptedMessege = cypher.encrypt(massege.encode('utf-8'))

    return encryptedMessege

def decryptSentence(encriptedString, key):
    cypher = Fernet(key)
    decriptedMessege = cypher.decrypt(encriptedString).decode('utf-8')

    return decriptedMessege


textToEncrypt = input("text:")
keySeed = input("keyseed:")

key = keyGenerator(keySeed)
encryptedText = encryptSentence(textToEncrypt, key)
decryptedText = decryptSentence(encryptedText, key)

ic(textToEncrypt)
ic(keySeed)
ic(key)
ic(encryptedText)
ic(decryptedText)