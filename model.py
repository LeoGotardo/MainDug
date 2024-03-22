from cryptography.fernet import Fernet
from pymongo import MongoClient
from dotenv import load_dotenv
from hashlib import sha256
from icecream import ic
from PIL import Image
 
import random as r
import Debug as d
import pyperclip
import logging
import hashlib
import base64
import io
import os


class Model:
    def __init__(self)-> None:
        """Initializes the Model class and sets up MongoDB connection."""
        # Configure debug output prefix
        ic.configureOutput(prefix=f"{d.Margin}\nDebug | ")
        # Clear screen in a cross-platform way
        os.system('cls' if os.name == 'nt' else 'clear')

        load_dotenv()

        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')

        # MongoDB connection setup
        try:
            connection_string = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.gcolnp2.mongodb.net/"

            self.client = MongoClient(connection_string)
            self.db = self.client["Belle"]
            self.logins = self.db["Logins"]
            self.passwords = self.db["Password"]

            if "Logins" not in self.db.list_collection_names():
                self.db.create_collection("Logins")
            if "Password" not in self.db.list_collection_names():
                self.db.create_collection("Passwords")

        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")


    def imgToBinary(self, path: str) -> bytes:
        """
        Converts an image file to its binary representation.

        This function opens an image file from the given path, reads it in binary mode, and 
        returns the binary content. This is useful for storing or processing images in their 
        binary form.

        Args:
            path (str): The filesystem path to the image file to be converted.

        Returns:
            bytes: The binary content of the image file.
        """
        with open(path, 'rb') as file:
            binary_content = file.read()
        return binary_content


    def addUser(self, login: str, password: str) -> bool:
        """
        Adds a new user to the 'Logins' collection with a hashed password.

        Args:
            login (str): User's login name.
            password (str): User's password.

        Returns:
            The inserted user ID on success, or an error message on failure.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = {"Login": login, "Password": hashed_password}
        try:
            result = self.logins.insert_one(user)
            return result.inserted_id
        except Exception as e:
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
        valid = self.logins.find_one({'$and': [{"Login": login}, {"Password": hashed_password}]})
        if valid is not None:
            return [True, valid['_id']]
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
        if password == password_confirm:
            if password != "":
                if self.logins.find_one({'Login': login}) is None:
                    return True
                else:
                    return 'Login already exists.'
            else:
                return "Password can't be empty"
        else:
            return 'Password and confirmation do not match.'


    def updateUser(self, user_id: str, parameter: str, new_value: str) -> str:
        """
        Updates a specific user's information in the 'Logins' collection.

        This method allows updating a user's information by specifying a parameter to update and 
        the new value for it. If updating the password, the new password is hashed before storage.

        Args:
            user_id (str): The unique identifier of the user to update.
            parameter (str): The field of the user's information to update (e.g., 'Password').
            new_value (str): The new value to set for the specified parameter.

        Returns:
            str: A success message if the update was successful, or an error message if it failed.
        """
        if parameter == 'Password':
            new_value = hashlib.sha256(new_value.encode()).hexdigest()

        try:
            self.logins.update_one({'_id': user_id}, {'$set': {parameter: new_value}})
            return f'{parameter} successfully updated.'
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            return str(e)


    def findUserId(self, login: str, password: str) -> str:
        """
        Finds and returns the unique identifier (ID) of a user based on their login and password.

        This method attempts to find a user in the 'Logins' collection matching the provided login
        and password. If the password is not a special case ('$exists'), it will be hashed before 
        comparison. 

        Args:
            login (str): The login name of the user.
            password (str): The password of the user. If '$exists', the password check is bypassed.

        Returns:
            str: The user's ID if a match is found, None otherwise.
        """
        if password != "$exists":
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = self.logins.find_one({"Login": login, "Password": hashed_password})
        else:
            user = self.logins.find_one({"Login": login, "Password": password})
        return user["_id"] if user else None


    def deleteUser(self, user_id: str) -> bool:
        """
        Deletes a user and their associated data based on the user ID.

        This method attempts to delete a user from the 'Logins' collection and any related data 
        from the 'Passwords' collection using the user's ID. 

        Args:
            user_id (str): The unique identifier of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        try:
            result = self.logins.delete_one({'_id': user_id})
            self.passwords.delete_many({'user_id': user_id})
            return result.deleted_count > 0
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
            user_id (str): The unique identifier of the user to retrieve passwords for.

        Returns:
            list: A list of lists, each containing the document ID and the first three logins for each matching document.
        """
        secret = self.logins.find_one({'_id': user_id})
        secret = secret['Login']
        key = Cryptography.keyGenerator(secret)
        i=0

        users = self.passwords.find({"user_id": user_id})

        results = []  # A list to store the results

        for user in users:
            try:
                if "logins" in user and len(user["logins"]) >= 3:
                    value = [user["_id"], user["logins"]['site'], user["logins"]['login'], user["logins"]['password']]
                    results.append(value)
            except Exception as e:
                print(f"Error processing user {user['user_id']}: {e}")
                continue
        for item in results:
            decrypted_password = Cryptography.decryptSentence(item[3], key)
            results[i][3] = decrypted_password
            i+=1
        return results


    def deleteItem(self, logged_user_id: str, item_id: int) -> tuple:
        """
        Attempts to delete a specified item for a logged-in user.

        This method first verifies that the logged-in user is the owner of the item by comparing user IDs.
        If the user is the owner, it then attempts to delete the item from the 'logins' collection.

        Args:
            logged_user_id (str): The ID of the logged-in user attempting the deletion.
            item_id (str): The ID of the item to be deleted.

        Returns:
            tuple: A tuple containing a boolean indicating success or failure, and a message describing the outcome.
        """
        try:
            item = self.passwords.find_one({"_id": item_id})
            userID = item["user_id"]

            if logged_user_id == userID:
                result = self.passwords.delete_one({'_id': item_id})
                if result.deleted_count > 0:
                    return "Item deleted successfully."
                else:
                    return "Item not found."
            else:
                return "Item not found."
        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            return f"Failed to delete item: {e}"


    def addNewLog(self, user_id, site: str, login: str, password: str) -> str:
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
        secret = self.logins.find_one({'_id': user_id})
        secret = secret['Login']
        key = Cryptography.keyGenerator(str(secret))
        password = Cryptography.encryptSentence(password, key)
        try:
            passId = self.findPassID()
            self.passwords.insert_one({'_id': passId, 'user_id': user_id, 'logins': {'site':site, 'login':login, 'password':password}})
            return 'Log added successfully.'
        except Exception as e:
            logging.error(f"Failed to add new log: {e}")
            return str(e)


    def validEditArgs(self, user_id, log_id: int):
        try:
            log_entry = self.passwords.find_one({'_id': int(log_id)})
            # Check if the log entry exists and belongs to the user.
            if log_entry and log_entry.get('user_id') == user_id:
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
            secret = self.logins.find_one({'_id': user_id})
            secret = secret['login']
            key = Cryptography.keyGenerator(str(secret))
            new_value = Cryptography.encryptSentence(new_value, key)

        try:
            # Attempt to find and update the log entry
            itens = self.passwords.find_one({'_id':int(log_id)})
            item = itens['logins']
            item[parameter] = new_value
            update_result = self.passwords.update_one(
                {'_id': int(log_id)},
                {'$set': {'logins': item}}
            )

            # Check if the update was successful
            if update_result.modified_count == 1:
                return f"{parameter.capitalize()} updated successfully."
            else:
                return "Log entry not found or no update required."

        except Exception as e:
            logging.error(f"Failed to edit log: {e}")
            return f"Failed to edit log: {e}"
        

    def findPassID(self) -> int:
        # Buscar todos os documentos na coleção que tenham um campo _id.
        cursor = self.passwords.find({'_id': {'$exists': True}})
    
        # Extrair os _id's e colocá-los em um conjunto para busca rápida.
        ids_set = {doc['_id'] for doc in cursor}

        # Iniciar a busca pelo menor _id inteiro positivo ausente.
        i = 1
        while True:
            if i not in ids_set:
                return i
            i += 1


    def copy(self, id, itemID: int) -> str:
        try:
            item = self.passwords.find_one({'_id': int(itemID)})
            ic(item)
            if item['user_id'] == id:
                item = item['logins']
                password = item['password']
                key = self.logins.find_one({'_id': id})
                key = key['Login']
                key = Cryptography.keyGenerator(key)
                password = Cryptography.decryptSentence(password, key)
                ic(item)
                copy = f"Login: {item['login']} \nPassword: {password}"
                ic(copy)
                pyperclip.copy(copy)
                return True, "Login and Password copied to your clipboard"
            else:
                return False, "Cant find any matching item"
        except Exception as e:
            return e, "Cant find any matching item"


class PasswordGenerator:
    """
    A class for generating random passwords based on specified criteria.
    
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
        """
        Generates a random password based on the specified criteria.
        
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
        """
        Generates a secure key from a given secret using SHA-256 hashing and Base64 encoding.

        The function first hashes the secret using SHA-256 to ensure a fixed-length output. Then, it encodes the hash
        in Base64 format to create a suitable key for cryptographic operations, such as Fernet encryption.

        Args:
            secret (str): The secret string from which to generate the key.

        Returns:
            bytes: The generated secure key in Base64 format.
        """
        # Step 1: Hash the string using SHA-256 to ensure 32 bytes
        hash_bytes = sha256(secret.encode('utf-8')).digest()
        
        # Step 2: Encode the hash result in base64 to be used as a Fernet key
        base64_key = base64.urlsafe_b64encode(hash_bytes)
        
        return base64_key
    
    
    def encryptSentence(message: str, key: bytes) -> bytes:
        """
        Encrypts a message using Fernet symmetric encryption with the provided key.

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
        """
        Decrypts an encrypted message using Fernet symmetric decryption with the provided key.

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