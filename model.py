import os
import hashlib
import logging
import Debug as d
from pymongo import MongoClient


class Model:
    def __init__(self):
        # Clear screen in a cross-platform way
        os.system('cls' if os.name == 'nt' else 'clear')

        DB_USER = 'leleo1208'
        DB_PASSWORD = '1234'

        # MongoDB connection setup
        connection_string = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.gcolnp2.mongodb.net/"
        
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client["Belle"]
            self.logins = self.db["Logins"]
            self.passwords = self.db["Password"]
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
        if parameter == 'Password':
            new_value = hashlib.sha256(new_value.encode()).hexdigest()

        try:
            self.logins.update_one({'_id': user_id}, {'$set': {parameter: new_value}})
            return f'{parameter} sucessfull updated'
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            return e

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
    
    def findPasswords(self, id):
        user = self.passwords.find({"_id":id})

        if type(user) != 'list':
            user = []

        return user
    
    def delete_item(self, id, item_id):
        try:
            passwords = self.findPasswords(id)
            del passwords[item_id]

            self.passwords.delete_one({'_id': id})

            return 'Process Done'
        except Exception as e:
            return e
        
    def addNewLog(self, id, site, login, password):
        try:
            passwords = self.findPasswords(id)
            item = [site, login, password]
            
            print(d.Margin,passwords,d.Margin)
            self.passwords.insert_one({'user_id': id}, {'login' : item})

            return 'Process Done'
        except Exception as e:
            return e

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Create an instance of the Model class for testing
    model = Model()
