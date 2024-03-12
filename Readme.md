---

# Password Manager Application

## Introduction
This project is a Password Manager Application developed using Python. It provides a graphical user interface (GUI) for users to manage their passwords securely. The application allows users to generate strong passwords, store them, and manage login credentials for various websites.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)
- [Details](#`View.py` - GUI Management)

## Installation

Before running the application, ensure you have Python installed on your system. You will also need to install some external libraries. Navigate to the project's root directory and run:

```bash
pip install -r requirements.txt
```

This will install all the necessary dependencies such as `tkinter`, `pymongo`, `PIL`, and `customtkinter`.

## Usage

To start the application, run the `View.py` script from the terminal or command prompt:

```bash
python View.py
```

Follow the GUI prompts to log in, sign up, generate passwords, and manage your stored credentials.

## Features

- User authentication (login and signup)
- Password generation with customizable criteria (length, inclusion of numbers/symbols)
- Secure password storage and management
- GUI for easy interaction

## Dependencies

- Python 3.x
- tkinter
- pymongo
- PIL (Python Imaging Library)
- customtkinter
- alive_progress

## Configuration

No additional configuration is needed to run the application in its default state. Make sure to enter your MongoDB connection details in `Model.py` to connect to your database.

## Documentation

For more detailed information on how to use this application, refer to the inline comments within each script. The main components are:

- `View.py`: Contains the GUI and user interaction logic.
- `Model.py`: Handles database operations and password storage.
- `Controller.py`: Serves as an intermediary between the view and model.
- `PasswordGenerator.py`: Generates passwords based on given criteria.

## Examples

Here are some common actions you can perform with the application:

- **Generating a Password:** Navigate to the password generation section, select your criteria, and generate a strong password.
- **Adding a Login:** Store a new login by entering the site name, your username, and password.
- **Editing Credentials:** Update your stored credentials as needed.

Para detalhar cada função dos códigos fornecidos, organizarei as descrições com base em cada arquivo Python do seu projeto de gerenciamento de senhas. Isso fornecerá um entendimento claro do propósito e da funcionalidade de cada parte do código.

---

## `View.py` - GUI Management

### `CustomThread`
- **Purpose:** Subclass of `Thread` for running tasks in the background. Allows for the retrieval of the thread's return value.
- **Methods:**
  - `__init__`: Constructor to initialize the thread.
  - `run`: Overrides the `Thread.run` method to execute the target function and store its return value.
  - `join`: Waits for the thread to complete and returns the stored return value.

### `View`
- **Purpose:** Manages the application's graphical user interface (GUI), including displaying and handling user interactions.
- **Methods:**
  - `__init__`: Sets up the main application window and initializes GUI elements.
  - `fullGeneratePass`: Generates a password based on user criteria in a separate thread.
  - `deleteItem`: Opens a dialog for deleting an item based on its ID.
  - `editCred`: Allows editing of credentials (login or password) for a user.
  - `add`: Handles the addition of new login credentials.
  - `addLogDB`: Adds a new login entry to the database.
  - `delete`: Deletes a user account after confirmation.
  - `editLog`: Edits a specific log item.
  - `validLogin`: Validates user login credentials.
  - `addCad`: Adds a new user account.
  - `seePass`: Toggles the visibility of password entries.
  - `theme`: Switches the theme of the application.
  - `alert`: Displays an alert dialog.
  - `login`: Sets up the login page.
  - `signup`: Sets up the signup page.
  - `logged`: Displays the main user interface after login.
  - `config`: Displays account configuration options.
  - `editLogin`, `editPass`, `erase`, `generatePass`, `addLog`, `editItem`: Various methods for handling specific user interactions related to account and password management.

## `Model.py` - Database Operations

### `Model`
- **Purpose:** Manages database interactions for the application, including user and password management.
- **Methods:**
  - `__init__`: Initializes database connection and collections.
  - `add_user`: Adds a new user to the database.
  - `is_login_valid`: Validates login credentials.
  - `is_credential_valid`: Checks if the provided credentials are valid.
  - `update_user`: Updates user information.
  - `find_user_id`: Retrieves the user ID based on login credentials.
  - `delete_user`: Deletes a user from the database.
  - `findPasswords`: Finds passwords associated with a user.
  - `delete_item`: Deletes a specific item (password entry) for a user.
  - `addNewLog`: Adds a new login entry for a user.

## `Controller.py` - Application Logic

### `Controller`
- **Purpose:** Acts as an intermediary between the GUI (`View`) and the database (`Model`), processing user inputs and performing corresponding actions.
- **Methods:** Each method in the `Controller` class corresponds directly to an operation defined in the `Model` class, facilitating the required operations without directly interacting with the database layer.

## `PasswordGenerator.py` - Password Generation

### `Generator`
- **Purpose:** Generates passwords based on specified criteria (length, inclusion of numbers, symbols, etc.).
- **Methods:**
  - `__init__`: Constructs a password generator with specified criteria and generates a password.

---

Cada função e método detalhado acima desempenha um papel específico dentro da aplicação de gerenciamento de senhas, facilitando a interação do usuário com a interface gráfica, o processamento lógico das ações do usuário e a comunicação com o banco de dados para armazenamento e recuperação de dados. Esta visão detalhada ajuda a compreender como os componentes individuais da aplicação interagem para fornecer a funcionalidade completa.

## Troubleshooting

If you encounter issues connecting to MongoDB, ensure your connection string in `Model.py` is correct and that your database is accessible.

## Contributors

- Leonardo Gotardo
## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

