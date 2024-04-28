from cryptography.fernet import Fernet
from icecream import ic
from hashlib import sha256
import random as r
import pyperclip
import string
import sqlite3
import logging
import hashlib
import base64
import os

connection = sqlite3.connect('database.db', timeout=30)
cursor = connection.cursor()

def createList():
    # Simulando a geração da lista sem o módulo bson, usando string para ObjectId
    lista = []
    base_id = 0
    user = input("Username:")
    user_id = input('User id:')

    sites = [
    "youtube.com","en.wikipedia.org","facebook.com","instagram.com","twitter.com",
    "whatsapp.com","pornhub.com","pinterest.com","play.google.com","microsoft.com",
    "imdb.com","reddit.com","amazon.com","xnxx.com","apple.com",
    "tiktok.com","es.wikipedia.org","xvideos.com","nytimes.com","globo.com",
    "linkedin.com","de.wikipedia.org","fr.wikipedia.org","ja.wikipedia.org","quora.com",
    "yahoo.co.jp","espncricinfo.com","netflix.com","translate.google.com","uol.com.br",
    "openai.com","spboss.blog","fandom.com","canva.com","ru.wikipedia.org",
    "cricbuzz.com","detik.com","it.wikipedia.org","indiatimes.com","xhamster.com",
    "espn.com","satta-king-fixed-no.in","xosodaiphat.com","mayoclinic.org","sattaamatka.co.com",
    "pt.wikipedia.org","indeed.com","amazon.in","speedtest.net","nih.gov"
]
    
    names = [
    "olivia", "emma", "amelia", "sophia", "charlotte",
    "ava", "isabella", "mia", "luna", "aurora",
    "ellie", "harper", "evelyn", "lily", "aria",
    "mila", "gianna", "eliana", "camila", "nova",
    "sofia", "layla", "violet", "ella", "scarlett",
    "hazel", "willow", "chloe", "ivy", "avery",
    "eleanor", "penelope", "nora", "elena", "abigail",
    "isla", "delilah", "elizabeth", "paisley", "riley",
    "grace", "emily", "zoey", "maya", "leilani",
    "stella", "naomi", "athena", "emilia", "lainey",
    "noah", "liam", "oliver", "mateo", "elijah",
    "lucas", "ezra", "levi", "asher", "leo",
    "james", "luca", "muhammad", "ethan", "henry",
    "hudson", "maverick", "sebastian", "michael", "benjamin",
    "daniel", "jack", "elias", "grayson", "theo",
    "kai", "mason", "alexander", "jackson", "gabriel",
    "theodore", "samuel", "julian", "wyatt", "aiden",
    "josiah", "owen", "david", "waylon", "ezekiel",
    "luke", "jayden", "carter", "william", "isaiah",
    "logan", "santiago", "miles", "matthew", "john"
]


    for i in range(100):
        # Gerar detalhes aleatórios para cada item
        site = r.choice(sites)
        login = r.choice(names)
        login = login+"@gmail.com"
        password = ''.join(r.choices(string.ascii_letters + string.digits, k=20))
        key = keyGenerator(str(user))
        password = encryptSentence(password, key)

        cursor.execute("INSERT INTO Passwords (user_id, site, login, password) VALUES (?, ?, ?, ?)", (user_id, site, login, password))
        connection.commit()

    connection.close()

def keyGenerator(secret: str) -> bytes:
    hash_bytes = sha256(secret.encode('utf-8')).digest()
    base64_key = base64.urlsafe_b64encode(hash_bytes)
    return base64_key

def encryptSentence(message: str, key: bytes) -> str:
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode('utf-8'))
    return encrypted_message.decode('utf-8')

def main():
    addUser("Admin", "Admin")
    createList()
    
def addUser(login: str, password: str) -> bool:
        """
        Adds a new user to the 'Users' table with a hashed password.

        Args:
            login (str): User's login name.
            password (str): User's password.

        Returns:
            The inserted user ID on success, or an error message on failure.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = (login, hashed_password)
        try:
            cursor.execute("INSERT INTO Users (Login, Password) VALUES (?, ?)", user)
            connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            logging.error(f"Failed to add user: {e}")
            return str(e)

if __name__ == "__main__":
    main()