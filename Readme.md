# Password Manager Application

## Overview

This project is a **Password Manager Application** developed using Python and the `tkinter` library for the GUI. The application allows users to manage their passwords securely by generating, storing, and managing login credentials for various websites. It supports features like encrypted password storage, login authentication, password generation, and more.

The project is divided into four main modules:
- `append.py`: Handles database operations and encryptions.
- `controller.py`: Acts as the controller, managing logic between the model and view.
- `model.py`: Contains the data models and operations such as user management, password storage, and encryption.
- `view.py`: Manages the GUI components of the application.

## Features

- **User Authentication**: Users can sign up, log in, and store their credentials.
- **Password Management**: Users can add, delete, update, and view their stored passwords.
- **Password Generation**: A built-in random password generator with customizable criteria (length, symbols, numbers, etc.).
- **Encryption**: Passwords are stored securely using AES encryption provided by the `cryptography` package.
- **Clipboard Support**: Users can copy credentials to their clipboard for quick access.
- **User Interface Customization**: Dark and light modes for user interface customization.
- **Color Configuration**: Users can change the interface color for a personalized experience.

## Installation

### Prerequisites

- Python 3.x installed on your system.
- The following Python packages are required:
  - `cryptography`
  - `sqlite3`
  - `hashlib`
  - `pyperclip`
  - `tkinter`
  - `Pillow`
  - `customtkinter`
  - `CTkColorPicker`
  - `CTkTable`
  
  You can install the necessary dependencies using:

  ```bash
  pip install -r requirements.txt

### Database Setup

The application uses an SQLite database to store user information and passwords. The database is automatically set up when the application is run for the first time.

## Usage

### Running the Application

To start the application, run the `view.py` file:

```bash
python view.py
```

### User Authentication

- **Sign Up**: New users can sign up by providing a unique login and password.
- **Log In**: Existing users can log in with their credentials.
- **Password Encryption**: User passwords are encrypted using the `Fernet` encryption method before being stored.

### Password Management

- **Add New Password**: Users can add a new website login, along with the site name, username, and password.
- **Edit Password**: Users can edit the stored credentials for any site.
- **Delete Password**: Users can delete a password from their list.
- **Copy to Clipboard**: Quickly copy login credentials to the clipboard for easy use.

### Password Generation

- Users can generate a new random password using the password generator.
- Customizable password length and character inclusion (uppercase, lowercase, numbers, symbols).

### Customization

- **Dark/Light Mode**: Toggle between dark and light themes for the application.
- **Color Picker**: Users can choose a custom color theme for the application interface.

## File Descriptions

### `append.py`

This script manages interactions with the SQLite database, including adding users and storing encrypted passwords. It uses the `cryptography` library to encrypt and decrypt password strings.

### `controller.py`

The controller serves as the intermediary between the model and the view. It handles user input, interacts with the model for data operations, and updates the view accordingly.

### `model.py`

Contains the logic for user and password management, including:
- User authentication (login, signup).
- Storing and retrieving passwords.
- Encryption and decryption of sensitive data.
- Managing database connections and queries.

### `view.py`

Implements the graphical user interface (GUI) using `tkinter` and `customtkinter`. It allows users to interact with the application, providing functions such as logging in, managing passwords, and more.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
