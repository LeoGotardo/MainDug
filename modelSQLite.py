from cryptography.fernet import Fernet
 
import random as r
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

        self.connection = sqlite3.connect('database.db', timeout=30)
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
                Site TEXT NOT NULL,
                Login TEXT NOT NULL,
                Password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (id)
            )
        ''')
        self.connection.commit()
        
        
    def createKey(self, user_id: str):
        self.cursor.execute("SELECT Login FROM Users WHERE id = ?", (user_id))
        secret = self.cursor.fetchone()

        key = Cryptography.keyGenerator(secret[0])
    
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
        valid = self.cursor.execute(query, (login, hashed_password))
        valid = self.cursor.fetchone()
        
        if valid is not None:
            return [True, str(valid[0])]
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
        

    def updateUser(self, user_id: int, parameter: str, new_value: str) -> str:
        """
        Updates a specific user's information in the 'users' table.

        This method allows updating a user's information by specifying a parameter to update and 
        the new value for it. If updating the password, the new password is hashed before storage.

        Args:
            user_id (int): The unique identifier of the user to update.
            parameter (str): The column of the user's information to update (e.g., 'password').
            new_value (str): The new value to set for the specified parameter.

        Returns:
            str: A success message if the update was successful, or an error message if it failed.
        """
        if parameter == 'Password':
            print(new_value)
            new_value = hashlib.sha256(new_value.encode()).hexdigest()

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
        
        
    def findUserId(self, login: str, password: str) -> str:
        """
        Finds and returns the unique identifier (ID) of a user based on their login and password.

        This method attempts to find a user in the 'Logins' collection matching the provided login
        and password. If the password is not a special case ('EXISTS'), it will be hashed before 
        comparison. 

        Args:
            login (str): The login name of the user.
            password (str): The password of the user. If '$exists', the password check is bypassed.

        Returns:
            str: The user's ID if a match is found, None otherwise.
        """
        query = "SELECT id FROM Users WHERE Login = ? AND Password = ?"
        
        if password != "EXISTS":
            password = hashlib.sha256(password.encode()).hexdigest()
            user = self.cursor.execute(query, (login, password))
        else:
            user = self.cursor.execute(query, (login, password))
            
        user = self.cursor.fetchone()

        if user:
            return user[0]
        return None


    def deleteUser(self, user_id: int) -> bool:
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
            self.cursor.execute("DELETE FROM Users WHERE id = ?", (user_id))
            self.cursor.execute("DELETE FROM Passwords WHERE user_id = ?", (user_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
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
        key = self.createKey(user_id)
        
        self.cursor.execute("SELECT id, Site, Login, Password FROM Passwords WHERE user_id = ?", (user_id,))
        rows = self.cursor.fetchall()

        results = []
        for row in rows:
            if row:
                results.append([row[0], row[1], row[2], row[3]])  # Append document ID and login details


        for i, item in enumerate(results):
            decrypted_password = Cryptography.decryptSentence(item[3], key)
            results[i][3] = decrypted_password
        
        return results
    
    def deleteItem(self, logged_user_id: int, item_id: int) -> tuple:
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
            query = "DELETE FROM Passwords WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, (item_id, logged_user_id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return "Item deleted successfully."
            else:
                return "Item not found."

        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            return f"Failed to delete item: {e}"
        
    
    def addNewLog(self, user_id: int, site: str, login: str, password: str) -> str:
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
        self.cursor.execute("SELECT Login FROM Users WHERE id = ?", (user_id))
        secret = self.cursor.fetchone()
        key = Cryptography.keyGenerator(secret[0])
        password = Cryptography.encryptSentence(password, key)
        
        try:
            query = "INSERT INTO Passwords (user_id, Site, Login, Password) VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, (user_id, site, login, password))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return 'Log added successfully.'
        except Exception as e:
            logging.error(f"Failed to add new log: {e}")
            return str(e)
        
    
    def validEditArgs(self, user_id: int, log_id: str):
        try:
            query = f"SELECT user_id FROM Passwords WHERE id = {log_id}"
            self.cursor.execute(query)
            log_entry = self.cursor.fetchone()
            if log_entry and log_entry[0] == user_id:
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
            query = f"UPDATE Passwords SET {parameter} = ? WHERE id = ?"
            self.cursor.execute(query, (new_value, log_id))
            self.connection.commit()
            # Check if the update was successful
            if self.cursor.rowcount > 0:
                return f"{parameter.capitalize()} updated successfully."
            else:
                return "Log entry not found or no update required."

        except Exception as e:
            logging.error(f"Failed to edit log: {e}")
            return f"Failed to edit log: {e}"
        
    
    def filterPasswords(self, filter: str, mode: str, user_id):
        try:
            # Retrieve user key
            key = self.createKey(user_id)


            # Construct query based on mode
            sql_query = f"SELECT id, Site, Login, Password FROM Passwords WHERE user_id = ? AND {mode} LIKE ?"
            self.cursor.execute(sql_query, (user_id, f'%{filter}%'))
            logs = self.cursor.fetchall()

            # Process logs and decrypt passwords
            items = []
            for log in logs:
                try:
                    decrypted_password = Cryptography.decryptSentence(log[3] ,key)
                    items.append([log[0], log[1], log[2], decrypted_password])
                except Exception as e:
                    print(f"Error decrypting password for log {log[0]}: {e}")
            return items
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
        
    def changeColor(self, user_id, newColor):
        try:
            query = f"UPDATE Users SET Color = ? WHERE id = ?"
            self.cursor.execute(query, (newColor, user_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error ocorred: {e}")
            
            
    def findColor(self, user_id):
        query = "SELECT Color FROM Users WHERE id = ?"
        self.cursor.execute(query, (user_id))
        color = self.cursor.fetchone()

        return color[0]
        

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
                                                                                                                 