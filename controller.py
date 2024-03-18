from model import Model, Generator

class Controller:
    def __init__(self):
        # Initialize a Model object in the Controller instance
        self.model = Model()
        self.Generator = Generator()

    def add_user(self, login, password, password_confirm):
        # Calls the add_user method of Model and returns the result
        if self.model.is_credential_valid(login, password, password_confirm) == True:
            if type(self.model.add_user(login, password)) != str :
                return True
            else:
                return self.model.add_user(login, password)
        else:
            return self.model.is_credential_valid(login, password, password_confirm)


    def is_login_valid(self, login, Password):
        # Calls the is_login_valid method of Model and returns the result
        return self.model.is_login_valid(login, Password)
    

    def update_user(self, user_id, parameter, new_value):
        # Calls the update_user method of Model and returns the result
        return self.model.update_user(user_id, parameter, new_value)


    def delete_user(self, user_id):
        # Calls the delete_user method of Model and returns the result
        return self.model.delete_user(user_id)


    def find_user_id(self, login, password):
        # Calls the find_user_id method of Model and returns the user ID
        return self.model.find_user_id(login, password)
    

    def findPasswords(self,id):
        return self.model.findPasswords(id)
    

    def delete_item(self, id, item_id):
        return self.model.delete_item(id, item_id)
    

    def addNewLog(self, id, site, login, password):
        return self.model.addNewLog(id, site, login, password)


    def editLog(self, paramter, user_id, id, newLog):
        return self.model.editLog(paramter, user_id, id, newLog)
    
    def generator(self, number, lower, symbol, upper, len):
        return self.Generator.generator(number, lower, symbol, upper, len)


if __name__ == "__main__":
    # Create a Controller instance to test the class
    controller = Controller()