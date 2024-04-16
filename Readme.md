
# MainDug

Secure Password Manager is a Python application that helps users manage and store their passwords securely using modern encryption techniques. The application features a graphical user interface built with CustomTkinter, providing a user-friendly way to handle login credentials for various websites.

## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Contributors](#contributors)
- [License](#license)

## Installation

Before installing, ensure you have Python 3.6+ and pip installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LeoGotardo/MainDug.git
   cd MainDug
   ```

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python view.py
   ```

## Features

- **Secure login system:** Authentication to access stored passwords.
- **Encryption:** Uses Fernet encryption to securely store passwords.
- **Customizable UI:** Users can choose themes and customize the UI color.
- **Password generation:** Generate strong passwords based on user-selected criteria.
- **Password storage and management:** Add, edit, delete, and search for stored passwords.

## Usage

Upon launching the application, users will be prompted to log in or sign up. Once authenticated, users can:

- **Add new passwords:** Click on the 'Add' button and fill in the details.
- **View passwords:** All stored passwords are listed in the main window.
- **Edit passwords:** Select a password entry and use the 'Edit' button.
- **Delete passwords:** Select a password entry and use the 'Delete' button.
- **Change themes:** Toggle between light and dark modes.

## Dependencies

- Python 3.6+
- CustomTkinter
- PyMongo
- Cryptography
- Dotenv
- Python Imaging Library (PIL)

## Configuration

The application requires a MongoDB database. Configure the database connection by setting environment variables in a `.env` file:

```plaintext
DB_USER=your_username
DB_PASSWORD=your_password
```

## Documentation

Further documentation is available in the `docs` folder. This includes API documentation, detailed setup instructions, and user guides.


## Contributors

- **Leonardo Gorardo** - Programation and documentacion.
- **Pablo Romero** - Programation and documentacion.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
