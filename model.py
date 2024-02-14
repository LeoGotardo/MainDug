import os
import hashlib
from pymongo import MongoClient
import logging


class Model:
    def __init__(self):
        # Clear screen in a cross-platform way
        os.system('cls' if os.name == 'nt' else 'clear')

        DB_USER = 'LeoGotardo'
        DB_PASSWORD = 'dawdasdawdasadwads'

        # MongoDB connection setup
        connection_string = f"mongodb+srv://leleo1208:1234@cluster0.gcolnp2.mongodb.net/"
        
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client["Belle"]
            self.logins = self.db["Logins"]
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")

    def  add_user(self, login, password):
        """
        Adds a new user to the 'Logins' collection.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = {"Login": login, "Password": hashed_password}
        try:
            result = self.logins.insert_one(user)
            return result.inserted_id
        except Exception as e:
            logging.error(f"Failed to add user: {e}")
            return str(e)

    def is_login_valid(self, login, Password):
        """
        Checks if the given login exists in the 'Logins' collection.
        """
        hashed_password = hashlib.sha256(Password.encode()).hexdigest()
        valid = self.logins.find_one({"Login": login},{"password":hashed_password})

        itens = []


        if self.logins.find_one({"Login": login},{"password":hashed_password}) is not None:
            itens.append(True) 
            itens.append(valid['_id'])
            return itens
        else:
            itens.append(False)
            itens.append('Invalid Credentials')
            return itens


    def is_credential_valid(self,login, password, password_confirm):
        
        """
        Checks if the password matches the confirmation password.
        """
        if password == password_confirm and password != "":
            if self.logins.find_one({'Login':login}) is None:
                return True
            else:
                return 'Invalid login'
        else:
            return 'Invalid password'

    def update_user(self, user_id, parameter, new_value):
        """
        Updates user information in the 'Logins' collection.
        """
        valid_parameters = {"login": "Login", "password": "Password"}
        if parameter not in valid_parameters:
            return False

        update_field = valid_parameters[parameter]
        new_value_hashed = hashlib.sha256(new_value.encode()).hexdigest() if parameter == "password" else new_value
        try:
            result = self.logins.update_one({'_id': user_id}, {'$set': {update_field: new_value_hashed}})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            return False

    def find_user_id(self, login, password):
        """
        Finds the ID of a user based on login and password.
        """

        if password != "$exists":
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user = self.logins.find_one({"Login": login, "Password": hashed_password})
        else:
            user = self.logins.find_one({"Login": login, "Password": password})
        return user["_id"] if user else None

    def delete_user(self, user_id):
        """
        Deletes a user based on the user ID.
        """
        try:
            result = self.logins.delete_one({'_id': user_id})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"Failed to delete user: {e}")
            return False

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Create an instance of the Model class for testing
    model = Model()
