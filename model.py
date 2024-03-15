from pymongo import MongoClient
from icecream import ic

import Debug as d
import logging
import hashlib
import os


class Model:
    def __init__(self):
        ic.configureOutput(prefix=f"{d.Margin}\nDebug | ")
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
        valid = self.logins.find_one({'$and':[{"Login": login},{"Password":hashed_password}]})

        itens = []


        if valid is not None:
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
    

    def findPasswords(self, user_id):
        # Use .find() to get a cursor for all documents matching the query
        users = self.passwords.find({"user_id": user_id})

        results = []  # A list to store the results

        for user in users:
            try:
                # Make sure to check the length of 'login' to avoid IndexError
                if "login" in user and len(user["login"]) >= 3:
                    value = [user["_id"], user["login"][0], user["login"][1], user["login"][2]]
                    results.append(value)
            except Exception as e:
                print(f"Error processing user {user['user_id']}: {e}")
                continue

        ic(results)
        return results


    def delete_item(self, logged_user_id, item_id):
        try:
            item = self.passwords.find({"_id":item_id})

            userID = item["user_id"]


            # Verifica se o usuário logado é o mesmo registrado na DB
            if logged_user_id == userID:
                result = self.logins.delete_one({'_id': item_id})
                if result.deleted_count > 0:
                    return True, "Item deleted successfully."
                else:
                    return False, "Item not found."
            else:
                return "Cant find matching logs, try again..."
        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            return False, "Failed to delete item: an error occurred."        


    def addNewLog(self, id, site, login, password):
        try:
            passwords = self.findPasswords(id)
            item = [site, login, password]
            
            ic(passwords)
            self.passwords.insert_one({'user_id': id, 'login' : item})

            return 'Process Done'
        except Exception as e:
            return e


if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)

    # Create an instance of the Model class for testing
    model = Model()
