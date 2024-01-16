from model import Model

class Controller:
    def __init__(self):
        # Initialize a Model object in the Controller instance
        self.model = Model()

    def add_user(self, login, password, password_confirm):
        # Calls the add_user method of Model and returns the result
        if self.model.is_password_valid(password, password_confirm):
            return self.model.add_user(login, password)
        else:
            return False

    def is_login_valid(self, login):
        # Calls the is_login_valid method of Model and returns the result
        return self.model.is_login_valid(login)

    def update_user(self, user_id, parameter, new_value):
        # Calls the update_user method of Model and returns the result
        return self.model.update_user(user_id, parameter, new_value)

    def delete_user(self, user_id):
        # Calls the delete_user method of Model and returns the result
        return self.model.delete_user(user_id)

    def find_user_id(self, login, password):
        # Calls the find_user_id method of Model and returns the user ID
        return self.model.find_user_id(login, password)

if __name__ == "__main__":
    # Create a Controller instance to test the class
    controller = Controller()

    # Example usage of the controller
    user_id = controller.add_user("username", "password123", "password123")
    print(f"Added user ID: {user_id}")

    # Verify if login is valid
    is_valid = controller.is_login_valid("username")
    print(f"Is login valid: {is_valid}")
    # Update user information
    update_status = controller.update_user(user_id, "password", "newpassword123")
    print(f"Password updated: {update_status}")

    # Find user ID
    found_id = controller.find_user_id("username", "newpassword123")
    print(f"Found user ID: {found_id}")

    # Delete user
    delete_status = controller.delete_user(user_id)
    print(f"User deleted: {delete_status}")
