from cryptography.fernet import Fernet

from PIL import Image
 
import random as r
import pyperclip
import sqlite3
import logging
import hashlib
import base64
import os

class Model:
    def __init__(self) -> None:
        """Initializes the Model class and sets up SQLite connection."""
        # Clear screen in a cross-platform way
        os.system('cls' if os.name == 'nt' else 'clear')

        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.setup_tables()

    def setup_tables(self):
        """Set up SQLite tables if they do not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Login TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL,
                Color TEXT DEFAULT '#1b1b1b'
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                site TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (id)
            )
        ''')
        self.connection.commit()
        
        
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
    
    
    def addUser(self, login: str, password: str) -> bool:
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
            self.cursor.execute("INSERT INTO Users (Login, Password) VALUES (?, ?)", user)
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            logging.error(f"Failed to add user: {e}")
            return str(e)
        
    
    def isLoginValid(self, login: str, password: str) -> list:
        """
        Checks if the given login and password are valid.

        Args:
            login (str): The login to check.
            password (str): The password to check, will be hashed.

        Returns:
            A list containing a boolean of validity and either the user's ID or an error message.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        query = "SELECT id FROM Users WHERE Login = ? AND Password = ?"
        id = self.cursor.execute(query, (login, hashed_password))
        valid = self.cursor.fetchone()
        
        if valid is not None:
            return [True, id]
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
        if login == '':
            return "Login can't be empty."
        if password != password_confirm:
            return 'Password and confirmation do not match.'
        if password == '':
            return "Password can't be empty"
        
        query = "SELECT id FROM Users WHERE Login = ?"
        self.cursor.execute(query, (login,))
        if self.cursor.fetchone() is None:
            # If no existing user is found, the credentials are considered valid for new user creation.
            return True
        else:
            return 'Login already exists.'
        

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
        if parameter == 'password':
            new_value = hashlib.sha256(new_value.encode()).hexdigest()  # Corrected the hashing syntax

        try:
            # Assuming 'conn' is your SQLite database connection object
            # Safely constructing the SQL query to prevent SQL injection
            query = f"UPDATE Users SET {parameter} = ? WHERE id = ?"
            self.cursor.execute(query, (new_value, user_id))
            self.connection.commit()  # Commit the changes
            if self.cursor.rowcount > 0:
                return f'{parameter} successfully updated.'
            else:
                return 'No update performed. User not found.'
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            return str(e)



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

    def keyGenerator(secret: str) -> bytes:
        """Generates a secure key from a given secret using SHA-256 hashing and Base64 encoding.

        The function first hashes the secret using SHA-256 to ensure a fixed-length output. Then, it encodes the hash
        in Base64 format to create a suitable key for cryptographic operations, such as Fernet encryption.

        Args:
            secret (str): The secret string from which to generate the key.

        Returns:
            bytes: The generated secure key in Base64 format.
        """
        # Step 1: Hash the string using SHA-256 to ensure 32 bytes
        hash_bytes = hashlib.sha256(secret.encode('utf-8')).digest()
        
        # Step 2: Encode the hash result in base64 to be used as a Fernet key
        base64_key = base64.urlsafe_b64encode(hash_bytes)
        
        return base64_key
    
    
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
    

    def decryptSentence(encrypted_string: bytes, key: bytes) -> str:
        """Decrypts an encrypted message using Fernet symmetric decryption with the provided key.

        Args:
            encrypted_string (bytes): The encrypted message to decrypt.
            key (bytes): The decryption key in Base64 format, typically generated by the `key_generator` function.

        Returns:
            str: The decrypted plaintext message.
        """
        cipher = Fernet(key)
        decrypted_message = cipher.decrypt(encrypted_string).decode('utf-8')

        return decrypted_message



if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    generator = PasswordGenerator()
    model = Model()










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
                                                                                                                 