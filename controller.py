from model import Model, PasswordGenerator

class Controller:
    def __init__(self):
        self.model = Model()
        self.PasswordGenerator = PasswordGenerator()


    def addUser(self, login: str, password: str, password_confirm: str) -> bool:
        """Adds a new user if the credentials are valid and unique.
        
        Args:
            login: User's login name.
            password: User's password.
            password_confirm: Confirmation of the user's password.

        Returns:
            True if the user was added successfully, otherwise returns an error message.
        """
        item = self.model.isCredentialValid(login, password, password_confirm)
        if item == True:
            user_add_result = self.model.addUser(login, password)
            if type(user_add_result) != None:
                return True
            else:
                return user_add_result
        else:
            return item
        

    def isLoginValid(self, login: str, password: str) -> bool:
        """Checks if login credentials are valid.
        
        Args:
            login: User's login name.
            password: User's password.

        Returns:
            True if the login credentials are valid, False otherwise.
        """
        return self.model.isLoginValid(login, password)


    def updateUser(self, user_id, parameter: str, new_value: str) -> bool:
        """Updates a user's information.
        
        Args:
            user_id: The ID of the user to update.
            parameter: The field to update.
            new_value: The new value for the field.

        Returns:
            True if the update was successful, False otherwise.
        """
        return self.model.updateUser(user_id, parameter, new_value)
    

    def deleteUser(self, user_id) -> bool:
        """Deletes a user.
        
        Args:
            user_id: The ID of the user to delete.

        Returns:
            True if the user was successfully deleted, False otherwise.
        """
        return self.model.deleteUser(user_id)
    

    def findUserId(self, login: str, password: str) -> int:
        """Finds a user's ID based on login credentials.
        
        Args:
            login: User's login name.
            password: User's password.

        Returns:
            The user's ID if found, otherwise returns None.
        """
        return self.model.findUserId(login, password)
    

    def findPasswords(self, user_id) -> list:
        """Finds all passwords associated with a user.
        
        Args:
            user_id: The ID of the user.

        Returns:
            A list of passwords associated with the user.
        """
        return self.model.findPasswords(user_id)
    

    def deleteItem(self, user_id, item_id) -> bool:
        """Deletes an item for a user.
        
        Args:
            user_id: The ID of the user.
            item_id: The ID of the item to delete.

        Returns:
            True if the item was successfully deleted, False otherwise.
        """
        return self.model.deleteItem(user_id, item_id)
    

    def addNewLog(self, user_id, site: str, login: str, password: str) -> bool:
        """Adds a new log for a user.
        
        Args:
            user_id: The ID of the user.
            site: The site associated with the log.
            login: The login name for the site.
            password: The password for the site.

        Returns:
            True if the log was successfully added, False otherwise.
        """
        return self.model.addNewLog(user_id, site, login, password)
    

    def editLog(self, user_id: int, parameter: str, log_id, new_log: str) -> bool:
        """Edits a log for a user.
        
        Args:
            parameter: The parameter to edit in the log.
            user_id: The ID of the user.
            log_id: The ID of the log to edit.
            new_log: The new value for the log.

        Returns:
            True if the log was successfully edited, False otherwise.
        """
        return self.model.editLog(user_id, parameter, log_id, new_log)
    
    
    def generatePassword(self, number: bool, lower: bool, symbol: bool, upper: bool, length: int) -> str:
        """Generates a password based on specified criteria.
        
        Args:
            number: Include numbers in the password.
            lower: Include lowercase letters.
            symbol: Include symbols.
            upper: Include uppercase letters.
            length: The length of the password.

        Returns:
            The generated password.
        """
        return self.PasswordGenerator.generate_password(number, lower, symbol, upper, length)
    

    def validEditArgs(self, user_id, log_id: int) -> bool or str: # type: ignore
        """Validate arguments for editing credentials using the function of "model.py".
        
        Args: 
            user_id: The ID of the user.
            log_id: The ID of the log to edit.

        Returns:
            True if the validation is successful, False otherwise.
          """
        return self.model.validEditArgs(user_id, log_id)

    def copy(self, user_id , itemID: int) -> bool or str: # type: ignore
        """Copy login credentials and password to clipboard using the function of "model.py"

        Args:
            itemID: The credentials copied to the clipboard. 
        
            Returns:
            True if the user_id is the same as the credentials you want to copy, false otherwise.
        """
        return self.model.copy(user_id, itemID)
        
    def darkColor(self, color: str, amount: int) -> str:
        """Darkens the color chosen by the user for better visualization of the interface using the function of "model.py"
        
        Args:
            Color: Color in hexadecimal chosen by the user.
        
        Returns:
            The color chosen by the user but a little darker.
        """
        return self.model.darkColor(color, amount)
    
    def filterPasswords(self, filter: str, mode: str, user_id) -> list:
        return self.model.filterPasswords(filter, mode, user_id)
    
    def changeColor(self, user_id, newColor):
        return self.model.changeColor(user_id, newColor)

    def findColor(self, user_id):
        return self.model.findColor(user_id)

if __name__ == "__main__":
    controller = Controller()