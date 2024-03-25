---

# MainDug

Password Manager

## Introduction

This project is a Python-based password manager application that allows users to securely store and manage their passwords. The application utilizes a graphical user interface (GUI) built with the `customtkinter` and `Tkinter` libraries. It features encryption for secure password storage, with MongoDB as the backend database for persisting user information and passwords.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

Before you can use the Password Manager, you need to ensure that Python 3.6 or later is installed on your system. You also need MongoDB set up either locally or in the cloud. Follow these steps to install the application:

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

To start the application, run the `view.py` script from your terminal:

```bash
python view.py
```

The GUI should launch, allowing you to create an account, log in, and start managing your passwords.

## Features

- **Secure Password Storage:** Encrypts passwords before storing them in MongoDB.
- **Password Generation:** Generate strong passwords based on user-selected criteria.
- **Easy Management:** Add, edit, and delete login credentials for different sites.
- **User Accounts:** Support for multiple users with individual accounts.
- **Dark Mode:** Supports a dark mode for reduced eye strain.

## Dependencies

- `Tkinter` and `customtkinter` for the GUI.
- `PIL` for handling images.
- `Cryptography` for encryption and decryption.
- `MongoDB` as the backend database.
- `python-dotenv` for managing environment variables.
- Various other utility libraries like `icecream` for debugging and `pyperclip` for clipboard operations.

## Configuration

To connect to your MongoDB database, create a `.env` file in the root directory with the following content:

```
DB_USER=your_mongodb_username
DB_PASSWORD=your_mongodb_password
```

Replace `your_mongodb_username` and `your_mongodb_password` with your actual MongoDB credentials.

## Documentation

For more detailed information on the functions and classes, refer to the inline comments in the `view.py`, `controller.py`, and `model.py` files. The project is structured according to the MVC (Model-View-Controller) design pattern for clear separation of concerns.

## Troubleshooting

- **GUI does not start:** Make sure all dependencies are installed and Python 3.6+ is used.
- **Database connection issues:** Verify your `.env` file has the correct MongoDB credentials.

## Contributors

To contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

This template provides a solid foundation for your project's README. Adjust it as necessary to better fit your project's needs and details.
