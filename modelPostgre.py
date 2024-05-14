from dotenv import load_dotenv

import psycopg2
import os


class Model:
    def __init__(self) -> None:
        self.setupTables()
        
    
    def connect(self):
        load_dotenv()
        
        hostname = os.getenv('DB_HOST')
        database = os.getenv('DB_NAME')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')

        try:
            self.connection = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = password,
                port = port
            )
            
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.DatabaseError) as e:
            print(f"Failed to connect to Database: {e}")


    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()

            
    def setupTables(self):
        self.connect()
        
        self.cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id UUID PRIMARY KEY,
                Login TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL,
                Color TEXT DEFAULT '#1b1b1b'
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Passwords (
                id SERIAL PRIMARY KEY,
                user_id UUID NOT NULL,
                Site TEXT NOT NULL,
                Login TEXT NOT NULL,
                Password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (id)
            )
        ''')
        
        self.connection.commit()
        self.close()
            

if __name__ == "__main__":
    model = Model()