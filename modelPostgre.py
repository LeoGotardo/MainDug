from psycopg2.extras import RealDictCursor
from cryptography.fernet import Fernet
from dotenv import load_dotenv
 
import random as r
import psycopg2
import hashlib
import logging
import base64
import os


class Model:
    def __init__(self) -> None:
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
                Password BYTEA NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            )
        ''')
        
        self.connection.commit()
        self.close()
        
    
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
        
        
    def createKey(self, user_id: str):
        self.connect()
        self.cursor.execute("SELECT Login FROM Users WHERE id = %s", (user_id,))
        secret = self.cursor.fetchone()

        key = Cryptography.keyGenerator(secret[0])
        self.close()
    
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
    
    
    def addUser(self, login: str, password: str) -> str:
        self.connect()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = (login, hashed_password)
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("INSERT INTO Users (id, Login, Password) VALUES (uuid_generate_v4(), %s, %s) RETURNING id", user)
                result = cursor.fetchone()
                self.connection.commit()
                self.close()
                if result:
                    return result['id']
                else:
                    print("No UUID returned.")
                    return None
        except psycopg2.IntegrityError as e:
            logging.error(f"Failed to add user: {e}")
            return None
        
        
    def isLoginValid(self, login: str, password: str) -> list:
        """
        Checks if the given login and password are valid.
        
        Args:
            login (str): The login to check.
            password (str): The password to check, will be hashed.
            
        Returns:
            A list containing a boolean of validity and either the user's ID or an error message.
        """
        
        self.connect()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        query = "SELECT id FROM Users WHERE Login = %s AND Password = %s"
        valid = self.cursor.execute(query, (login, hashed_password))
        valid = self.cursor.fetchone()
        self.close()
        
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
        try:
            self.connect()
            if login == '':
                return "Login can't be empty."
            if password != password_confirm:
                return 'Password and confirmation do not match.'
            if password == '':
                return "Password can't be empty"
            
            query = "SELECT id FROM Users WHERE Login = %s"
            self.cursor.execute(query, (login,))
            if self.cursor.fetchone() is None:
                # If no existing user is found, the credentials are considered valid for new user creation.
                return True
            else:
                return 'Login already exists.'
        except Exception as e:
            print(f'An error occured:{e}')
        finally:
            self.close()
            
            
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
        self.connect()
        if parameter == 'Password':
            new_value = hashlib.sha256(new_value.encode()).hexdigest()

        try:
            # Assuming 'conn' is your SQLite database connection object
            # Safely constructing the SQL query to prevent SQL injection
            query = f"UPDATE Users SET {parameter} = %s WHERE id = %s"
            self.cursor.execute(query, (new_value, user_id))
            self.connection.commit()  # Commit the changes
            self.close()
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
            password (str): The password of the user. If 'EXISTS', the password check is bypassed.

        Returns:
            str: The user's ID if a match is found, None otherwise.
        """
        self.connect()

        if password == "EXISTS":
            query = "SELECT id FROM Users WHERE Login = %s"
            params = (login,)
        else:
            query = "SELECT id FROM Users WHERE Login = %s AND Password = %s"
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            params = (login, hashed_password)

        try:
            self.cursor.execute(query, params)
            user = self.cursor.fetchone()
            if user:
                return user[0]
            else:
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return None
        finally:
            self.close()
            
            
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
            self.connect()
            self.cursor.execute("DELETE FROM Users WHERE id = %s", (user_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Failed to delete user: {e}")
            return False
        finally:
            self.close()
            
    
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
        
        self.connect()
        self.cursor.execute("SELECT id, Site, Login, Password FROM Passwords WHERE user_id = %s", (user_id,))
        rows = self.cursor.fetchall()

        results = []
        for row in rows:
            if row:
                results.append([row[0], row[1], row[2], row[3]])  # Append document ID and login details


        for i, item in enumerate(results):
            decrypted_password = Cryptography.decryptSentence(item[3], key)
            results[i][3] = decrypted_password
            
        self.close()
        
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
            query = "DELETE FROM Passwords WHERE id = %s AND user_id = %s"
            self.cursor.execute(query, (item_id, logged_user_id))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return "Item deleted successfully."
            else:
                return "Item not found."

        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            return f"Failed to delete item: {e}"
        finally:
            self.close()
            

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
        key = self.createKey(user_id)
        self.connect()
        password = Cryptography.encryptSentence(password, key)
        
        try:
            query = "INSERT INTO Passwords (user_id, Site, Login, Password) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (user_id, site, login, password))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                return 'Log added successfully.'
        except Exception as e:
            logging.error(f"Failed to add new log: {e}")
            return str(e)          
        finally:
            self.close()
            
            
    def validEditArgs(self, user_id: int, log_id: str):
        try:
            self.connect()
            query = f"SELECT user_id FROM Passwords WHERE id = {log_id}"
            self.cursor.execute(query)
            log_entry = self.cursor.fetchone()
            if log_entry and log_entry[0] == user_id:
                return True
            else:
                return False, "Cannot find matching log entry or user mismatch. Please try again."
        except Exception as e:
            return e
        finally:
            self.close()
            
    
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
            self.connect()
            # Attempt to find and update the log entry
            query = f"UPDATE Passwords SET {parameter} = %s WHERE id = %s"
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
        finally:
            self.close()
            

    def filterPasswords(self, filter: str, mode: str, user_id):
        try:
            # Retrieve user key
            key = self.createKey(user_id)


            # Construct query based on mode
            self.connect()
            sql_query = f"SELECT id, Site, Login, Password FROM Passwords WHERE user_id = %s AND {mode} LIKE %s"
            self.cursor.execute(sql_query, (user_id, filter))
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
        finally:
            self.close()
            

    def changeColor(self, user_id, newColor):
        try:
            self.connect()
            query = f"UPDATE Users SET Color = %s WHERE id = %s"
            self.cursor.execute(query, (newColor, user_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error ocorred: {e}")
        finally:
            self.close()
            
    
    def findColor(self, user_id):
        try:
            self.connect()
            query = "SELECT Color FROM Users WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            color = self.cursor.fetchone()

            return color[0]
        except Exception as e:
            print(f'An error occurred:{e}')
        finally:
            self.close()
        
            
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
    def decryptSentence(encrypted_string: str, key: bytes) -> str:
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
                                                                                                                 