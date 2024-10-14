from sqlalchemy import create_engine, Column, String, Text, ForeignKey, UniqueConstraint, and_, or_
from sqlalchemy.orm import relationship, sessionmaker, declarative_base 
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from psycopg2.extras import RealDictCursor
from sqlalchemy.exc import SQLAlchemyError
from cryptography.fernet import Fernet
from sqlalchemy.sql import text
from dotenv import load_dotenv
from icecream import ic
 
import sqlalchemy as sa
import random as r
import pyperclip
import psycopg2
import hashlib
import logging
import bcrypt
import base64
import re
import os

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=sa.text("uuid_generate_v4()"))
    login = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    salt = Column(BYTEA, nullable=False)
    color = Column(Text, default='#1b1b1b', nullable=False)
    passwords = relationship('Passwords', back_populates='user', cascade='all, delete-orphan')


class Passwords(Base):
    __tablename__ = 'passwords'
    id = Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    site = Column(Text, nullable=False)
    login = Column(Text, nullable=False)
    password = Column(BYTEA, nullable=False)
    user = relationship('Users', back_populates='passwords')


class Model:
    def __init__(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        self.connect()
        self.session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        Base.metadata.create_all(self.engine)
        
    def connect(self):
        load_dotenv()
        
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        hostname = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')

        try:
            # Criar URL de conexão para o SQLAlchemy
            url = f"postgresql://{username}:{password}@{hostname}:{port}/{database}"
            # Criar engine
            self.engine = create_engine(url)
            # Criar uma sessão configurada
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            # Testar a conexão executando uma simples consulta
            result = self.session.execute(text("SELECT version()"))
            for row in result:
                print(f"Connected to: {row[0]}\n")
        
        except Exception as e:
            print(f"Failed to connect to Database: {e}")
        
        
    def createKey(self, user_id: str):
        query = sa.select(Users.login).where(Users.id == user_id)
        secret = self.session.execute(query).all()

        key = Cryptography.keyGenerator(secret[0][0])
    
        return key
    
    def darkColor(self, hex_color: str, darken_by: int) -> str:
        """
        Darkens the color chosen by the user for better visualization of the interface.
        
        Args:
            r, g, b = int: Converts Hex to RGB.
            r, g, b = max: Darkens the RGB components.
        Return:
           Defines the interface color chosen by the user, but darker.
        """
        hex_color = hex_color.strip('#')

        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        r, g, b = max(0, r - darken_by), max(0, g - darken_by), max(0, b - darken_by)

        return f'#{r:02x}{g:02x}{b:02x}'
    
    
    def addUser(self, login: str, password: str) -> str or None: # type: ignore
        # Generate a salt for this user
        salt = bcrypt.gensalt()  # This is already in bytes
        hashed_password = bcrypt.hashpw(password.encode(), salt).decode('utf-8')

        # Store both hashed password and salt in the database
        user_data = {'login': login, 'password': hashed_password, 'salt': salt}

        try:
            query = sa.insert(Users).values(**user_data).returning(Users.id)
            result = self.session.execute(query).fetchone()
            self.session.commit()

            if result:
                return str(result[0])
            else:
                print("No UUID returned.")
                return None
        except Exception as e:
            logging.error(f"Failed to add user: {e}")
            return None

        
        
    def isLoginValid(self, login: str, password: str) -> list:
        """
        Checks if the given login and password are valid by retrieving the stored salt
        and comparing the stored hashed password with the bcrypt hash of the provided password.
        """
        query = sa.select(Users.id, Users.password, Users.salt).where(Users.login == login)
        user_record = self.session.execute(query).fetchone()

        if user_record is not None:
            stored_password = user_record['password'].encode('utf-8')
            salt = user_record['salt']  # Salt is stored as bytes in the database
            
            # Hash the provided password using the stored salt
            hashed_input_password = bcrypt.hashpw(password.encode(), salt)
            
            # Compare the hashed input password with the stored hashed password
            if hashed_input_password == stored_password:
                return [True, str(user_record['id'])]
            else:
                return [False, 'Invalid Credentials']
        else:
            return [False, 'Invalid Credentials']

        
        
    def isCredentialValid(self, login: str, password: str, password_confirm: str) -> bool or str: # type: ignore
        """
        Validates if the password matches the confirmation password and checks for unique login.

        Args:
            login (str): The login name to validate.
            password (str): The password to check.
            password_confirm (str): The password confirmation to match against.

        Returns:
            True if credentials are valid, otherwise returns an error message.
        """
        try:
            if login == '':
                return "Login can't be empty."
            if password != password_confirm:
                return 'Password and confirmation do not match.'
            if password == '':
                return "Password can't be empty"
            
            query = sa.select(Users.id).where(Users.login == login)
            logins = self.session.execute(query).all()
            
            if len(logins) == 0:
                # If no existing user is found, the credentials are considered valid for new user creation.
                return True
            else:
                return 'Login already exists.'
        except Exception as e:
            print(f'An error occured:{e}')

            
            
    def updateUser(self, user_id: str, parameter: str, new_value: str) -> str:
        """
        Updates a specific user's information in the 'users' table.

        This method allows updating a user's information by specifying a parameter to update and 
        the new value for it. If updating the password, the new password is hashed before storage.

        Args:
            user_id (str): The unique identifier of the user to update.
            parameter (str): The column of the user's information to update (e.g., 'password').
            new_value (str): The new value to set for the specified parameter.

        Returns:
            str: A success message if the update was successful, or an error message if it failed.
        """
        if parameter.lower() == 'password':
            new_value = hashlib.sha256(new_value.encode()).hexdigest()

        try:
            if parameter.lower() == 'login':
                 if self.changeCryptography(user_id, new_value) == False:
                     return 'An error ocurred, please try again...'
            query = sa.update(Users).where(Users.id == user_id).values({parameter: new_value})
            itens = self.session.execute(query)
            
            self.session.commit()

            if itens.rowcount > 0:
                return f'{parameter} successfully updated.'
            else:
                return 'No update performed. User not found.'
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            return str(e)
        
    
    def changeCryptography(self, user_id: str, new_login: str):
        try:
            logs = self.findPasswords(user_id)
            key = Cryptography.keyGenerator(new_login)
            for log in logs:
                password_id = log[0]
                password = log[3]
                hashed_password = Cryptography.encryptSentence(password, key)
                self.session.execute(sa.update(Passwords).where(Passwords.id == password_id).values({'password': hashed_password}))
            self.session.commit()
            return True
        except Exception as e:
            print(f'An error occurred: {e}')
            self.session.rollback()
            return False
        
    def copy(self, userID: str, itemID: int) -> bool or str: # type: ignore
        """
        A function do copy login credentials stored in DB to clipboard.
        
        Attributes:
            item: Login of the user.
            password: Password of the user.
            Key: Create a key for get the Login of the user and encrypt the password.
            Copy: The Login and Password already copied to the clipboard.

        Returns:
            The login credentials copied to the clipboard if True, False otherwise.
        """
        try:
            query = sa.select(Passwords.login, Passwords.password).where(and_(Passwords.id == itemID, Passwords.user_id == userID))
            item = self.session.execute(query).all()
            if item:
                print(item)
                password = item[0][1]
                key = self.createKey(userID)
                password = Cryptography.decryptSentence(password, key)
                copy = f"Login: {item[0][0]} \nPassword: {password}"
                pyperclip.copy(copy)
                return "Login and Password copied to your clipboard"
            else:
                return "Cant find any matching item"
        except Exception as e: 
            print(f"An error ocurred: {e}")
            return False
        
    def findUserId(self, login: str, password: str) -> str:
        """
        Finds and returns the unique identifier (ID) of a user based on their login and password.

        This method attempts to find a user in the 'Logins' collection matching the provided login
        and password. If the password is not a special case ('EXISTS'), it will be hashed before 
        comparison. 

        Args:
            login (str): The login name of the user.
            password (str): The password of the user. If 'EXISTS', the password check is bypassed.

        Returns:
            str: The user's ID if a match is found, None otherwise.
        """

        if password == "EXISTS":
            query = sa.select(Users.id).where(Users.login == login)
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            query = sa.select(Users.id).where(and_(Users.login == login, Users.passwords == hashed_password))


        try:
            id = self.session.execute(query).all()
            if id:
                return id[0][0]
            else:
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return None
       
            
    def deleteUser(self, user_id: str) -> bool:
        """
        Deletes a user and their associated data based on the user ID.

        This method attempts to delete a user from the 'Logins' collection and any related data 
        from the 'Passwords' collection using the user's ID. 

        Args:
            user_id (in): The unique identifier of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        try:
            query = sa.delete(Users).where(Users.id == user_id)
            
            result = self.session.execute(query)
            self.session.commit()
            
            return result.rowcount > 0
        except Exception as e:
            logging.error(f"Failed to delete user: {e}")
            return False

            
    
    def findPasswords(self, user_id: str) -> list:
        """
        Retrieves a list of password information for a specific user.

        This method searches the 'passwords' collection for documents matching the specified user ID. It then extracts
        the first three login entries for each matching document, if available, and returns a list of these entries
        along with their document IDs.

        Args:
            user_id (int): The unique identifier of the user to retrieve passwords for.

        Returns:
            list: A list of lists, each containing the document ID and the first three logins for each matching document.
        """
        try:
            key = self.createKey(user_id)
            
            query = sa.select(Passwords.id, Passwords.site, Passwords.login, Passwords.password).where(Passwords.user_id == user_id)
            rows = self.session.execute(query).all()
            results = []
            for row in rows:
                if row:
                    results.append([row[0], row[1], row[2], row[3]])  # Append document ID and login details


            for i, item in enumerate(results):
                decrypted_password = Cryptography.decryptSentence(item[3], key)
                results[i][3] = decrypted_password
        except Exception as e:
            print(f"An error occured: {e}")
            
        
        return results
    
    
    def deleteItem(self, logged_user_id: str, item_id: int) -> tuple:
        """
        Attempts to delete a specified item for a logged-in user.

        This method first verifies that the logged-in user is the owner of the item by comparing user IDs.
        If the user is the owner, it then attempts to delete the item from the 'logins' collection.

        Args:
            logged_user_id (int): The ID of the logged-in user attempting the deletion.
            item_id (int): The ID of the item to be deleted.

        Returns:
            tuple: A tuple containing a boolean indicating success or failure, and a message describing the outcome.
        """
        try:
            self.connect()
            query = sa.delete(Passwords).where(and_(Passwords.id == item_id, Passwords.user_id == logged_user_id))
            result = self.session.execute(query)
            self.session.commit()
            if result.rowcount > 0:
                return "Item deleted successfully."
            else:
                return "Item not found."

        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            return f"Failed to delete item: {e}"

            

    def addNewLog(self, user_id: str, site: str, login: str, password: str) -> str:
        """
        Adds a new login entry for a specific user.

        This method creates a new document in the 'passwords' collection containing the user ID, site, login,
        and password information.

        Args:
            user_id (str): The ID of the user to add the log for.
            site (str): The website or application associated with the log.
            login (str): The login name or identifier.
            password (str): The password for the site/login.

        Returns:
            str: A message indicating the completion of the process or describing any errors encountered.
        """
        
        try:
            key = self.createKey(user_id)
            password = Cryptography.encryptSentence(password, key)
            query = sa.insert(Passwords).values({'user_id': user_id, 'site': site, 'login': login, 'password': password})
            result = self.session.execute(query)
            self.session.commit()
            if result.rowcount > 0:
                return 'Log added successfully.'
        except Exception as e:
            logging.error(f"Failed to add new log: {e}")
            return e          

            
            
    def validEditArgs(self, user_id: int, log_id: str):
        try:
            query = sa.select(Passwords.user_id).where(Passwords.id == log_id)
            log_entry = self.session.execute(query).all()
            if log_entry and str(log_entry[0][0]) == user_id:
                return True
            else:
                return False, "Cannot find matching log entry or user mismatch. Please try again."
        except Exception as e:
            return e

            
    
    def editLog(self, user_id: int, parameter: str, log_id: int, new_value: str) -> str:
        """
       Edits a specific field ('site', 'login', or 'password') of a log entry for a user.

        Args:
            parameter (str): The field of the log entry to update ('site', 'login', or 'password').
            log_id (int): The ID of the log entry to be edited.
            new_value (str): The new value to be set for the specified field.

        Returns:
            str: A message indicating the outcome of the operation, whether success or failure.

        Raises:
            Exception: If an error occurs during the find or update operations on the database.
        """
        if parameter == 'password':
            key = self.createKey(user_id)
            new_value = Cryptography.encryptSentence(new_value, key)

        try:
            # Attempt to find and update the log entry
            query = sa.update(Passwords).where(Passwords.id == log_id).values({parameter: new_value})
            results = self.session.execute(query)
            self.session.commit()
            # Check if the update was successful
            if results.rowcount > 0:
                return f"{parameter.capitalize()} updated successfully."
            else:
                return "Log entry not found or no update required."

        except Exception as e:
            logging.error(f"Failed to edit log: {e}")
            return f"Failed to edit log: {e}"


    def filterPasswords(self, filter: str, mode: str, user_id: str) -> list or None:  # type: ignore
        try:
            # Retrieve user key
            key = self.createKey(user_id)
            if mode.lower() == 'password':  
                passwords = self.findPasswords(user_id)
                filtered_passwords = []
                pattern = re.compile(re.escape(filter), re.IGNORECASE)  # Case insensitive regex pattern
                for password in passwords:
                    if pattern.search(password[3]):  # Use regex search to check if filter is in the password
                        filtered_passwords.append(password)
                return filtered_passwords      
            else:
                # Construct condition based on mode
                if mode.lower() == "site":
                    condition = Passwords.site.like(f"%{filter}%")
                elif mode.lower() == "login":
                    condition = Passwords.login.like(f"%{filter}%")
                else:
                    raise ValueError("Invalid mode. Choose 'site', 'login', or 'password'.")

                # Construct query based on mode
                query = (
                    sa.select(Passwords.id, Passwords.site, Passwords.login, Passwords.password)
                    .where(and_(Passwords.user_id == user_id, condition))
                )
                logs = self.session.execute(query).fetchall()

                # Process logs and decrypt passwords
                items = []
                for log in logs:
                    try:
                        decrypted_password = Cryptography.decryptSentence(log.password, key)
                        items.append([log.id, log.site, log.login, decrypted_password])
                    except Exception as e:
                        print(f"Error decrypting password for log {log.id}: {e}")
                return items

        except SQLAlchemyError as e:
            print(f"SQLAlchemy error occurred: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


    def changeColor(self, user_id, newColor):
        try:
            query = sa.update(Users).where(Users.id == user_id).values({'color': newColor})
            self.session.execute(query)
            self.session.commit()
            return True
        except Exception as e:
            print(f"An error ocorred: {e}")
         
    
    def findColor(self, user_id):
        try:
            query = sa.select(Users.color).where(Users.id == user_id)
            color = self.session.execute(query).all()

            return color[0][0]
        except Exception as e:
            print(f'An error occurred:{e}')

        
            
class PasswordGenerator:
    """A class for generating random passwords based on specified criteria.
    
    Attributes:
        let (list of str): Lowercase letters.
        may (list of str): Uppercase letters.
        sim (list of str): Special characters.
        numb (list of str): Digits from 0 to 9.
    """
    def __init__(self) -> None:
        """Initializes the PasswordGenerator with lists of characters used in password creation."""
        self.let = [chr(i) for i in range(97, 123)]  # a-z
        self.may = [chr(i) for i in range(65, 91)]  # A-Z
        self.sim = ['!', '@', '#', '$', '%', '¨', '&', '*', '(', ')', '+', '=', '|', '<', '>', ':', ';', '?']
        self.numb = [str(i) for i in range(10)]  # 0-9


    def generate_password(self, include_numbers: bool, include_lowercase: bool, include_symbols: bool, include_uppercase: bool, size: int) -> str:
        """Generates a random password based on the specified criteria.

        Args:
            include_numbers (bool): Whether to include numbers in the password.
            include_lowercase (bool): Whether to include lowercase letters in the password.
            include_symbols (bool): Whether to include symbols in the password.
            include_uppercase (bool): Whether to include uppercase letters in the password.
            size (int): The length of the password to generate.

        Returns:
            str: The generated password.
        """
        available_chars = []
        if include_numbers:
            available_chars.extend(self.numb)
        if include_lowercase:
            available_chars.extend(self.let)
        if include_symbols:
            available_chars.extend(self.sim)
        if include_uppercase:
            available_chars.extend(self.may)

        password = [r.choice(available_chars) for _ in range(size)]
        return ''.join(password)


class Cryptography:
    def __init__(self) -> None:
        pass
    

    @staticmethod
    def keyGenerator(secret: str) -> bytes:
        """Generates a secure key from a given secret using SHA-256 hashing and Base64 encoding.

        The function first hashes the secret using SHA-256 to ensure a fixed-length output. Then, it encodes the hash
        in Base64 format to create a suitable key for cryptographic operations, such as Fernet encryption.

        Args:
            secret (str): The secret string from which to generate the key.

        Returns:
            bytes: The generated secure key in Base64 format.
        """

        hash_bytes = hashlib.sha256(secret.encode('utf-8')).digest()
        base64_key = base64.urlsafe_b64encode(hash_bytes)
        
        return base64_key
    
    
    @staticmethod
    def encryptSentence(message: str, key: bytes) -> bytes:
        """Encrypts a message using Fernet symmetric encryption with the provided key.

        Args:
            message (str): The plaintext message to encrypt.
            key (bytes): The encryption key in Base64 format, typically generated by the `key_generator` function.

        Returns:
            bytes: The encrypted message.
        """
        cipher = Fernet(key)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))

        return encrypted_message
    
    
    @staticmethod
    def decryptSentence(encrypted_string: str, key: str) -> str:
        """Decrypts an encrypted message using Fernet symmetric decryption with the provided key.

        Args:
            encrypted_string (bytes): The encrypted message to decrypt.
            key (bytes): The decryption key in Base64 format, typically generated by the `key_generator` function.

        Returns:
            str: The decrypted plaintext message.
        """
        cipher = Fernet(key)
        decrypted_message = cipher.decrypt(bytes(encrypted_string)).decode('utf-8')

        return decrypted_message



if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    model = Model()
    print(model.filterPasswords('1','password', '119864e9-5f05-4659-8359-ed1a15dff34c'))









#  __                                  ______              __                                __           
# |  \                                /      \            |  \                              |  \          
# | $$       ______    ______        |  $$$$$$\  ______  _| $$_     ______    ______    ____| $$  ______  
# | $$      /      \  /      \       | $$ __\$$ /      \|   $$ \   |      \  /      \  /      $$ /      \ 
# | $$     |  $$$$$$\|  $$$$$$\      | $$|    \|  $$$$$$\\$$$$$$    \$$$$$$\|  $$$$$$\|  $$$$$$$|  $$$$$$\
# | $$     | $$    $$| $$  | $$      | $$ \$$$$| $$  | $$ | $$ __  /      $$| $$   \$$| $$  | $$| $$  | $$
# | $$_____| $$$$$$$$| $$__/ $$      | $$__| $$| $$__/ $$ | $$|  \|  $$$$$$$| $$      | $$__| $$| $$__/ $$
# | $$     \\$$     \ \$$    $$       \$$    $$ \$$    $$  \$$  $$ \$$    $$| $$       \$$    $$ \$$    $$
#  \$$$$$$$$ \$$$$$$$  \$$$$$$         \$$$$$$   \$$$$$$    \$$$$   \$$$$$$$ \$$        \$$$$$$$  \$$$$$$ 
#                                                                                                        
                                                                                                        
                                                                            
# /$$$$$$$           /$$       /$$                 /$$$$$$$                                                       
#| $$__  $$         | $$      | $$                | $$__  $$                                                      
#| $$  \ $$ /$$$$$$ | $$$$$$$ | $$  /$$$$$$       | $$  \ $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
#| $$$$$$$/|____  $$| $$__  $$| $$ /$$__  $$      | $$$$$$$/ /$$__  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$ /$$__  $$
#| $$____/  /$$$$$$$| $$  \ $$| $$| $$  \ $$      | $$__  $$| $$  \ $$| $$ \ $$ \ $$| $$$$$$$$| $$  \__/| $$  \ $$
#| $$      /$$__  $$| $$  | $$| $$| $$  | $$      | $$  \ $$| $$  | $$| $$ | $$ | $$| $$_____/| $$      | $$  | $$
#| $$     |  $$$$$$$| $$$$$$$/| $$|  $$$$$$/      | $$  | $$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$| $$      |  $$$$$$/
#|__/      \_______/|_______/ |__/ \______/       |__/  |__/ \______/ |__/ |__/ |__/ \_______/|__/       \______/ 
                                                                                                                 