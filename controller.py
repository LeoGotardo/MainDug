from model import Model, Generator

class Controller:
    def __init__(self):
        self.model = Model()
        self.generator = Generator()

    def add_user(self, login: str, password: str, password_confirm: str) -> bool:
        """Adds a new user if the credentials are valid and unique.
        
        Args:
            login: User's login name.
            password: User's password.
            password_confirm: Confirmation of the user's password.

        Returns:
            True if the user was added successfully, otherwise returns an error message.
        """
        if self.model.is_credential_valid(login, password, password_confirm):
            user_add_result = self.model.add_user(login, password)
            if type(user_add_result) != str:
                return True
            else:
                return user_add_result
        else:
            return self.model.is_credential_valid(login, password, password_confirm)
        

    def is_login_valid(self, login: str, password: str) -> bool:
        """Checks if login credentials are valid.
        
        Args:
            login: User's login name.
            password: User's password.

        Returns:
            True if the login credentials are valid, False otherwise.
        """
        return self.model.is_login_valid(login, password)


    def update_user(self, user_id, parameter: str, new_value: str) -> bool:
        """Updates a user's information.
        
        Args:
            user_id: The ID of the user to update.
            parameter: The field to update.
            new_value: The new value for the field.

        Returns:
            True if the update was successful, False otherwise.
        """
        return self.model.update_user(user_id, parameter, new_value)
    

    def delete_user(self, user_id) -> bool:
        """Deletes a user.
        
        Args:
            user_id: The ID of the user to delete.

        Returns:
            True if the user was successfully deleted, False otherwise.
        """
        return self.model.delete_user(user_id)
    

    def find_user_id(self, login: str, password: str) -> int:
        """Finds a user's ID based on login credentials.
        
        Args:
            login: User's login name.
            password: User's password.

        Returns:
            The user's ID if found, otherwise returns None.
        """
        return self.model.find_user_id(login, password)
    

    def find_passwords(self, user_id) -> list:
        """Finds all passwords associated with a user.
        
        Args:
            user_id: The ID of the user.

        Returns:
            A list of passwords associated with the user.
        """
        return self.model.find_passwords(user_id)
    

    def delete_item(self, user_id, item_id) -> bool:
        """Deletes an item for a user.
        
        Args:
            user_id: The ID of the user.
            item_id: The ID of the item to delete.

        Returns:
            True if the item was successfully deleted, False otherwise.
        """
        return self.model.delete_item(user_id, item_id)
    

    def add_new_log(self, user_id, site: str, login: str, password: str) -> bool:
        """Adds a new log for a user.
        
        Args:
            user_id: The ID of the user.
            site: The site associated with the log.
            login: The login name for the site.
            password: The password for the site.

        Returns:
            True if the log was successfully added, False otherwise.
        """
        return self.model.add_new_log(user_id, site, login, password)
    

    def edit_log(self, parameter: str, user_id, log_id, new_log: str) -> bool:
        """Edits a log for a user.
        
        Args:
            parameter: The parameter to edit in the log.
            user_id: The ID of the user.
            log_id: The ID of the log to edit.
            new_log: The new value for the log.

        Returns:
            True if the log was successfully edited, False otherwise.
        """
        return self.model.edit_log(parameter, user_id, log_id, new_log)
    
    
    def generate_password(self, number: bool, lower: bool, symbol: bool, upper: bool, length: int) -> str:
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
        return self.generator.generate(number, lower, symbol, upper, length)

if __name__ == "__main__":
    controller = Controller()
