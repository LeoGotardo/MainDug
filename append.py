from psycopg2.extras import RealDictCursor
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from hashlib import sha256
from icecream import ic
import random as r
import psycopg2
import string
import logging
import hashlib
import base64
import os

os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()

hostname = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port = os.getenv('DB_PORT')

try:
    connection = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=password,
        port=port
    )
    
    cursor = connection.cursor()
    
except (Exception, psycopg2.DatabaseError) as e:
    print(f"Failed to connect to Database: {e}")

def close():
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()

def setupTables():
        cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                Login TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL,
                Color TEXT DEFAULT '#1b1b1b'
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Passwords (
                id SERIAL PRIMARY KEY,
                user_id UUID NOT NULL,
                Site TEXT NOT NULL,
                Login TEXT NOT NULL,
                Password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (id)
            )
        ''')

        connection.commit()

def appendList(user, user_id):
    sites = [
        "youtube.com", "en.wikipedia.org", "facebook.com", "instagram.com", "twitter.com",
        "whatsapp.com", "pornhub.com", "pinterest.com", "play.google.com", "microsoft.com",
        "imdb.com", "reddit.com", "amazon.com", "xnxx.com", "apple.com",
        "tiktok.com", "es.wikipedia.org", "xvideos.com", "nytimes.com", "globo.com",
        "linkedin.com", "de.wikipedia.org", "fr.wikipedia.org", "ja.wikipedia.org", "quora.com",
        "yahoo.co.jp", "espncricinfo.com", "netflix.com", "translate.google.com", "uol.com.br",
        "openai.com", "spboss.blog", "fandom.com", "canva.com", "ru.wikipedia.org",
        "cricbuzz.com", "detik.com", "it.wikipedia.org", "indiatimes.com", "xhamster.com",
        "espn.com", "satta-king-fixed-no.in", "xosodaiphat.com", "mayoclinic.org", "sattaamatka.co.com",
        "pt.wikipedia.org", "indeed.com", "amazon.in", "speedtest.net", "nih.gov"
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
        # Generate random details for each item
        site = r.choice(sites)
        login = r.choice(names) + "@gmail.com"
        password = ''.join(r.choices(string.ascii_letters + string.digits, k=20))
        key = keyGenerator(str(user))
        password = encryptSentence(password, key)

        cursor.execute("INSERT INTO Passwords (user_id, Site, Login, Password) VALUES (%s, %s, %s, %s)", (user_id, site, login, password))
        connection.commit()

def keyGenerator(secret: str) -> bytes:
    hash_bytes = sha256(secret.encode('utf-8')).digest()
    base64_key = base64.urlsafe_b64encode(hash_bytes)
    return base64_key

def encryptSentence(message: str, key: bytes) -> str:
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode('utf-8'))
    return encrypted_message.decode('utf-8')

def addUser(login: str, password: str) -> str:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = (login, hashed_password)
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("INSERT INTO Users (id, Login, Password) VALUES (uuid_generate_v4(), %s, %s) RETURNING id", user)
            result = cursor.fetchone()
            connection.commit()
            if result:
                return result['id']
            else:
                print("No UUID returned.")
                return None
    except psycopg2.IntegrityError as e:
        logging.error(f"Failed to add user: {e}")
        return None

def main():
    setupTables()

    login = input('Enter the login to add:')
    if login:
        password = input('Enter the password:')
        user_id = addUser(login, password)
        ic(user_id)
        if user_id:
            appendList(login, user_id)
    else:
        user_id = input('UserID:')
        appendList(login, user_id)

if __name__ == "__main__":
    main()
