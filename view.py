from tkinter import messagebox as msg
from controller import Controller
from PIL import Image as img
from customThread import CustomThread
from CTkColorPicker import *
from CTkTable import *
from icecream import ic

import customtkinter as ctk
import time





class View(ctk.CTk):
    def __init__(self):
        """
        Initializes the application.

        Functionality:
            - Clears the console screen.
            - Configures the output for debug logging.
            - Initializes the Controller instance.
            - Creates the main application window.
            - Loads various icons for different functionalities.
            - Sets primary and secondary colors for the application.
            - Sets appearance mode to 'dark'.
            - Sets initial mode to 'dark' and calls the login function.
            - Sets the geometry of the application window and prevents resizing.
            - Starts the main event loop of the application.
        """
        

        self.c = Controller()
        self.app = ctk.CTk()

        self.see = ctk.CTkImage(dark_image=img.open("icons/see.ico"))
        self.unsee = ctk.CTkImage(dark_image=img.open("icons/unsee.ico"))
        self.white = ctk.CTkImage(dark_image=img.open("icons/White.ico"))
        self.dark = ctk.CTkImage(dark_image=img.open("icons/Dark.ico"))
        self.exit = ctk.CTkImage(dark_image=img.open("icons/Exit.ico"))
        self.Config = ctk.CTkImage(dark_image=img.open("icons/Config.ico"))
        self.Add = ctk.CTkImage(dark_image=img.open("icons/add.ico"))
        self.Delete = ctk.CTkImage(dark_image=img.open("icons/delete.ico"))
        self.edit = ctk.CTkImage(dark_image=img.open("icons/edit.ico"))
        self.copy = ctk.CTkImage(dark_image=img.open("icons/copy.ico"))
        self.newColor = ctk.CTkImage(dark_image=img.open("icons/newColor.ico"))
        self.search = ctk.CTkImage(dark_image=img.open("icons/search.ico"))
        self.x = ctk.CTkImage(dark_image=img.open("icons/X.ico"))

        self.priColor = '#1b1b1b'
        self.secColor = self.c.darkColor(self.priColor, 50)
        self.filterMode = 'Filter'
        self.user_id = None
        self.mode = 'dark'
        self.loginvar = None
        self.passwordvar = None
        self.thread = None

        ctk.set_appearance_mode('dark')

        self.login()

        self.app.protocol("WM_DELETE_WINDOW", self.askClose)
        self.app.geometry("500x600")
        self.app.resizable(width=False, height=False)
        self.app.mainloop()
        
        
    def getValue(self, *entryes):
        self.values = []
        for entry in entryes:
            self.values.append(entry.get())

    
    def callloading(self, lastscreen, frame, screen, func):
        if func:
            try:
                self.thread = CustomThread(target=func)
                self.thread.start()
                frame.destroy()
                self.loading()
                self.app.after(100, self.is_alive, screen, lastscreen)
            except Exception as e:
                print(f"Error: {e}")
                return False
        else:
            lastscreen
    
    def is_alive(self, screen, lastscreen):
        if self.thread.is_alive():
            self.app.after(200, self.is_alive, screen, lastscreen)
        else:
            result = self.thread.join()
            print(self.user_id, result)
            self.loading_complete()
            print(result)
            if result == False:
                lastscreen()
            else:
                screen()


    def selectMode(self, mode):
        """
        Sets the filter mode.

        Args:
            self: The instance of the class.
            mode (str): The filter mode to be set.

        Functionality:
            - Updates the filter mode attribute with the provided mode value.
        """
        self.filterMode = mode


    def unfilter(self, user_id):
        """
        Removes the filter and displays all passwords.
        
        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Calls the findPasswords method to retrieve all passwords for the user.
            - Destroys the current logged frame.
            - Calls the logged method to display all passwords again.
        """
        self.findPasswords(user_id)
        self.loggedFrame.destroy()
        self.logged(user_id)


    def filterItens(self, filter, user_id):
        """
        Filters items based on the selected filter.

        Args:
            self: The instance of the class.
            filter (str): The filter to apply.
            user_id (int): Identifier of the user.

        Returns:
            list or False: A list of filtered items if successful, False otherwise.

        Functionality:
            - Checks if a filter mode is selected, if not, shows an information message and returns False.
            - Attempts to filter passwords based on the provided filter and filter mode.
            - Inserts the title at the beginning of the filtered passwords list.
            - Destroys the current logged frame.
            - Calls the logged method to display the filtered passwords.
            - Returns the filtered passwords list.
        """
        if self.filterMode == 'Filter':
            msg.showinfo(message="You need to select a filter.")
            return False

        try:
            self.passwords = self.c.filterPasswords(filter, self.filterMode, user_id)
            self.passwords.insert(0, self.title)
            self.loggedFrame.destroy()
            self.logged(user_id)
            return self.passwords
        except Exception as e:
            msg.showwarning(title="ERROR", message=e)


    def askColor(self, user_id):
        """
        Prompt the user to choose a color. Opens a color picker dialog and sets the primary and secondary colors based on the chosen color, and configures the frame accordingly.
        Args:
            id(int): Identifier parameter.
            pick_color = Open the color picker.
            self.priColor: Get the color string.
            self.secColor: Computes a darker shade for secondary color.
            self.configFrame: Destroys the configuration frame.
            self.config: Configures the frame based on the provided identifier.
        """
        pick_color = AskColor() # open the color picker
        self.priColor = pick_color.get() # get the color string
        self.secColor = self.c.darkColor(self.priColor, 50)
        self.c.changeColor(user_id, self.priColor)
        self.configFrame.destroy()
        self.config(user_id)


    def fullGeneratePass(self, user_id, len, upper, lower, symbol, number):
        """
        Generates a password based on the provided parameters and displays it to the user.
        Args:
            self: The instance of the class.
            user_id (int):Identifier of the user.
            len (int): Lenght of the password to be generated.
            upper (bool): Indicates wheter to include uppercase letters in the password.
            lower (bool): Indicates wheter to include lowercase letters in the password.
            symbol (bool): Indicates wheter to include symbols in the password.
            number (bool): Indicates wheter to include numbers in the password.
            
        Returns:
            bool: False if an error occurs during password generations, otherwise returns true.
        """
        try:
            len = int(len)
        except:
            msg.showerror(message='Password Length must be a integer number.', title="Error")
            return False
        
        if len > 20:
            msg.showinfo(title='Item Len', message='Item Len must be lower than 20.')
            return 0
        else:
            password = CustomThread(target=self.c.generatePassword, args=(number,lower,symbol,upper,len))
            password.start()

            fullPassword = password.join()
            
            self.generatePassFrame.destroy()
            self.addWithPass(user_id, fullPassword)


    def passVerify(self, password, passwordConfirm, user_id, itemId):
        """
        Verifies and updates a user's password.
        
        Args:
            self: The instance of the class.
            password (str): The new password entered by the user.
            passwordConfirm (str): The confirmation of the new password.
            user_id (int): Identifier of the user.
            itemID (int): Identifier of the item.
        
        Functionality:
            - Checks if the provided password and its confirmation match using the passVerifyFunc method.
            - If the passwords match, attempts to update the password in the system's log using the editLogFunc method.
            - If an exception occurs during the update process, displays an error message.
        """
        if self.passVerifyFunc(password, passwordConfirm):
            try:
                self.editLogFunc("password", user_id, itemId, password)
            except Exception as e:
                msg.showerror(title="Error", message=str(e))


    def passVerifyFunc(self, password, confirm):
        """
         Verifies if the provided password matches its confirmation.
         
         Args:
            self: The instance of the class.
            password (str): The password entered by the user.
            confirm (str): The confirmation of the password entered by the user.

        Functionality:
            - Compares the provided password with its confirmation.
            - If they match:
                - Checks if the password is not empty.
                - If the password is not empty, returns True.
                - If the password is empty, displays an error message and returns False.
            - If they do not match, displays an error message and returns False.
        """
        if password == confirm:
            if password != "":
                return True
            else:
                self.alert("ERROR", "Password can't be empty")
                return False
        else:
            self.alert("ERROR", "Passwords do not metch")
            return False


    def deleteItem(self, user_id):
        """
        Deletes an item associated with the provided user ID.
        
        Args:
            self: the instance of the class.
            user_id (int): Identifier of the user whose item is to be deleted.
        
        Functionality:
            - Prompts the user to input the item ID to be deleted using a dialog window.
            - Attempts to convert the input item ID to an integer.
            - If conversion fails, displays an error message and returns 0.
            - Attempts to delete the item associated with the provided user ID and item ID using the deleteItem method.
            - Displays an information message about the deletion result.
            - Destroys the current frame (loggedFrame).
            - Calls the findPasswords and logged methods to update the user interface with the remaining items and user information.
        """
        dialog = ctk.CTkInputDialog(title="Delete Item", text="What's the item ID that you want to delete?")
        item_id = dialog.get_input()
        try:
            item_id = int(item_id)
        except:
            msg.showerror(title="Error", message="ID must be a number.")
            dialog
            return 0
        try:
            deleted = self.c.deleteItem(user_id, item_id)
            msg.showinfo(title='Info', message=deleted)
            self.loggedFrame.destroy()
            self.findPasswords(user_id)
            self.logged(user_id)
        except Exception as e:
            msg.showerror(title="Error", message=e)
    
    
    def editCred(self, user_id, paramter, newPar):
        """
        Edits the user credentials such as login or password.
        
        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            parameter (str): The parameter to be edited, either "Login" or "Password".
            newPar (str or tuple): The new parameter value(S) to be set.
            
        Functionality:
            - Check if the new parameter value is not empty.
            - If editing the login:
                - Checks if the new parameter value is not empty.
                - If the new login does not exist, updates the user's login with the new value.
                - Displays an information message about the update result.
                - Destroys the current frame (editLoginFrame).
                - Calls the findPasswords and logged methods to update the user's interface.
                - Otherwise, displays an error message that the login already exists.
            If editing the password:
                - Verifies if the new password and its confirmation match using the passVerifyFunc method.
                - If the password match and are not empty, update the user's password with the new value.
                - Displays an information message about the update result.
                - Destroys the current frame (editPasswordFrame).
                - Calls the findPasswords and logged methods to update the user interface.
            If the new parameter value is empty, displays an error message.
        """
        if newPar != '':
            if paramter == "Login":
                new = self.c.findUserId(newPar, "EXISTS")
                if new == None:
                    sull = self.c.updateUser(user_id, paramter, newPar)
                    self.alert("Info", sull)

                    self.editLoginFrame.destroy()
                    self.findPasswords(user_id)
                    self.logged(user_id)
                else:
                    self.alert("ERROR",f'This login alredy exists.')
            if paramter == "Password":
                if self.passVerifyFunc(newPar[0], newPar[1]):
                    sull = self.c.updateUser(user_id, paramter, newPar[0])
                    self.alert("Info", sull)

                    self.editPasswordFrame.destroy()
                    self.findPasswords(user_id)
                    self.logged(user_id)
        else:
            self.alert('ERROR', f"{paramter} can't be empty.")


    def add(self, user_id):
        """
        Adds a new login for the user.
        
        Args:
            Self: The instance of the class.
            user_id (int): Identifier of the user.
        
        Functionality:
            - Prompt the users wheter ther want to generate a new password.
            - If the user chooses to generate a new password:
            - Destroys the current frame (loggedFrame).
            - Calls the generatePass method to generate a new password for the user.
            - If the user chooses not to generate a new password:
            - Destroys the current frame (loggedFrame).
            - Calls the addLog method to add a new login for the user.
        """
        newPass = msg.askquestion(title='New Login', message='Do you want to generate a new passwrd?')

        if newPass == 'yes':
            self.loggedFrame.destroy()
            self.generatePass(user_id)
        elif newPass == 'no':
            self.loggedFrame.destroy()
            self.addLog(user_id)


    def addLogDB(self, user_id, site, login, password, frame):
        """
        Adds a new login entry to the database.
        
        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            site (str): Website or service associated with the login.
            login (str): Username or login ID for the site.
            password (str): Password for the site.
            frame (object): Frame object to be destroyed upon successful addition of the login entry.
        
        Functionality:
            - Adds a new login entry to the database using the addNewLog method.
            - If a frame object is provided:
                - Displays an information message about the addition result.
                - Destroys the current frame (addPassFrame).
                - Calls the findPasswords and logged methods to update the user interface.
            - If no frame object is provided:
                - Displays an information message about the addition result.
        """
        if frame is not None:
            ret = self.c.addNewLog(user_id, site, login, password)
            msg.showinfo(title="Info", message=ret)

            self.addPassFrame.destroy()
            self.findPasswords(user_id)
            self.logged(user_id)
        else:
            ret = self.c.addNewLog(user_id, site, login, password)
            msg.showinfo(title="Info", message=ret)


    def delete(self, user_id):
        """
        Deletes a user account.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.  

        Returns:
            bool: True if the user confirms deletion, False otherwise.

        Functionality:
            - Prompts the user with a warning message to confirm account deletion.
            - If the user confirms (response is "yes"):
             - Attempts to delete the user account using the deleteUser method.
             - Displays an information message confirming successful deletion.
             - Destroys the current frame (eraseFrame).
             - Calls the login method to return to the login screen.
            - If an exception occurs during account deletion, displays an error message.
            - If the user cancels deletion (response is not "yes"), returns False.
        """
        response = msg.askquestion(title="Delete Account",
                               message="Are you sure you want to delete this account? This action cannot be undone.",
                               icon="warning")  # Use askquestion for a clear yes/no choice
        if response == "yes":
            try:
                # Perform account deletion logic here
                self.c.deleteUser(user_id)
                msg.showinfo('Done',f'Account {user_id} sucessfull deleted.')
                self.eraseFrame.destroy()
                self.login()
            except Exception as e:
                msg.showerror("Error", "An error occurred while deleting the account.")
        else:
            return False


    def editLog(self, user_id):
        """
        Edits an item for the user.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Prompts the user to input the item ID using a dialog window.
            - Attempts to convert the input item ID to an integer.
            - If conversion fails, displays an error message.
            - Calls the validEditArgs method to check if the provided user ID and item ID are valid for editing.
            - If the item ID is valid for editing:
                - Destroys the current frame (loggedFrame).
                - Calls the editItem method to edit the item associated with the user and item IDs.
            - If the item ID is not valid for editing, displays an error message.
        """
        dialog = ctk.CTkInputDialog(text="What's the item ID:", title='Edit item')
        itemID = dialog.get_input()
        try:
            int(itemID)
        except:
            msg.showerror(text='Item must be a number')
        if self.c.validEditArgs(user_id, itemID) == True:
            self.loggedFrame.destroy()
            self.editItem(user_id, itemID)
        else:
            msg.showerror(title="Error", message=self.c.validEditArgs(user_id, itemID))


    def findPasswords(self, user_id):
        """
        Finds passwords associated with the provided user ID.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Retrieves passwords associated with the provided user ID using the findPasswords method.
            - Constructs a list of titles for the passwords table.
            - Inserts the titles as the first row of the passwords list.
        """
        self.passwords = self.c.findPasswords(user_id)
        self.title = ['ID', 'Site', 'Login', 'Password']
        self.passwords.insert(0, self.title)


    def validLogin(self, login, password):
        """
        Validates a user login.

        Args:
            self: The instance of the class.
            login (str): User login.
            password (str): User password.
            
        Functionality:
        - Checks if the login and password are not empty.
        - Calls the isLoginValid method to check if the provided login and password are valid.
        - If the login is valid:
            - Destroys the current frame (loginFrame).
            - Calls the findPasswords method to retrieve passwords associated with the user.
            - Calls the logged method to update the user interface.
        - If the login is invalid:
            - Displays an error message.
            - Destroys the current frame (loginFrame).
            - Calls the login method to return to the login screen.
        - If the login or password is empty, displays an error message.
        """
        print('valid login')
        time.sleep(5)
        if login != '' or password != '':
            itens = self.c.isLoginValid(login, password)
            self.user_id = itens[1]
            if itens[0] == True:
                self.findPasswords(itens[1])
                return True
            else:
                self.alert("ERROR",itens[1])
                return False
        else:
            self.alert("ERROR", "Login or Password can't be empty")
            return False
        


    def addCad(self, login, password, passwordConfirm):
        """
        Adds a new user.

        Args:
        self: The instance of the class.
        login (str): New user's login.
        password (str): New user's password.
        passwordConfirm (str): Confirmation of the new user's password.
        
        Functionality:
            - Calls the addUser method to add a new user with the provided login and password.
            - If the user addition is successful:
                - Displays a success message.
                - Destroys the current frame (signupFrame).
                - Calls the login method to return to the login screen.
            - If there's an error adding the user:
                - Displays an error message.
                - Destroys the current frame (signupFrame).
                - Calls the signup method to return to the signup screen.
        """
        error = self.c.addUser(login, password, passwordConfirm)

        if error != False:
            self.alert("Susses","Sussesfull Signup")
            self.signupFrame.destroy()
            self.login()
        else:
            self.alert("ERROR",error)
            self.signupFrame.destroy()
            self.signup()

    
    def seePass(self, entry, button):
        """
        Toggles the visibility of a password in an entry widget.

        Args:
            self: The instance of the class.
            entry (Tkinter.Entry): Entry widget containing the password.
            button (Tkinter.Button): Button widget used to toggle password visibility.

        Functionality:
            - Checks the current state of the entry widget.
            - If the password is currently hidden:
                - Configures the entry widget to display the password.
                - Changes the button image to indicate that the password is visible.
            - If the password is currently visible:
                - Configures the entry widget to hide the password.
                - Changes the button image to indicate that the password is hidden.
        """
        if entry.cget('show') == "*":
            entry.configure(show="")
            button.configure(image=self.unsee)
        elif entry.cget('show') == "":
            entry.configure(show="*")
            button.configure(image=self.see)


    def theme(self, button):
        """
        Toggles between dark and light themes.

        Args:
            self: The instance of the class.
            button (Tkinter.Button): Button widget used to toggle the theme.

        Functionality:
            - Checks the current theme mode.
            - If the current mode is 'dark':
                - Sets the appearance mode to 'light'.
                - Changes the button image to indicate the light theme.
                - Updates the mode attribute to 'light'.
        - If the current mode is 'light':
                - Sets the appearance mode to 'dark'.
                - Changes the button image to indicate the dark theme.
                - Updates the mode attribute to 'dark'.
        """
        if self.mode == 'dark':
            ctk.set_appearance_mode('light')
            button.configure(image=self.dark)
            self.mode = 'light'
        else:
            ctk.set_appearance_mode('dark')
            button.configure(image=self.white)
            self.mode = 'dark'


    def alert(self, title, text):
        """
        Displays an alert message.

        Args:
            self: The instance of the class.
            title (str): Title of the alert message.
            text (str): Text of the alert message.

        Functionality:
            - Displays an alert message with the provided title and text using the showwarning method from the messagebox module.
        """
        msg.showwarning(title=title,message=text)


    def editLogFunc(self, paramter, user_id, ID, newLog):
        """
        Edits a log entry.

        Args:
            self: The instance of the class.
            paramter (str): Parameter to be edited.
            user_id (int): Identifier of the user.
            ID (int): Identifier of the log entry.
            newLog (str): New value for the parameter.

        Returns:
            bool: True if the log entry is successfully edited, False otherwise.

        Functionality:
            - Attempts to edit the log entry using the editLog method.
            - If successful, displays an information message with the result.
            - If an exception occurs during editing, displays a warning message with the error.
        """
        try:
            e = self.c.editLog(user_id, paramter, ID, newLog)
            msg.showinfo(title="Info", message=e)
            return True
        except Exception as e:
            msg.showwarning(title='Error', message=str(e))
            return False


    def copyFunc(self, user_id):
        """
        Copies item credentials.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Prompts the user to input the item ID using a dialog window.
            - Attempts to copy the item credentials using the copy method.
            - Displays an information message with the result of the copy operation.
            - If an exception occurs during copying, displays an error message.
        """
        try:
            dialog = ctk.CTkInputDialog(text="What's the item ID:", title='Copy item credentials...')
            itemID = dialog.get_input()
            copy = self.c.copy(user_id, itemID)
            msg.showinfo(message=copy[1])
        except Exception as e:
            msg.showerror(title="ERROR", message=e)
            
    
    def askClose(self): 
        """
        Prompts the user to confirm the application's exit.

        Args:
            self: The instance of the class.

        Functionality:
            - Prompts the user to confirm the application's exit.
            - If the user confirms the exit, the application is closed.
            - If the user cancels the exit, the application remains open.
        """
        response = msg.askyesno(title="Exit?", message="Are you sure you want to exit?")
        if response == True:
            if self.thread is not None:
                if self.thread.is_alive():
                    self.thread.raise_exception()
            self.app.destroy()
        else:
            pass


    def login(self):
        """
        Sets up the login page.

        Args:
            self: The instance of the class.

        Functionality:
            - Creates and configures the login frame.
            - Creates labels, entry fields, buttons, and icons for login, password entry, show/hide password, login button, signup button, and theme change button.
            - Binds the Return key to trigger the validLogin method when pressed.
            - Places all widgets within the login frame with appropriate configurations.
        """
        self.loginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Login")
        self.loginFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Alien.ico")

        title = ctk.CTkLabel(
            master=self.loginFrame,
            text="Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        self.loginEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            border_width=2,
            border_color=self.priColor,
            height=40,
            width=200
        )
        
        self.loginvar = self.loginEntry.get()

        self.passwordEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            border_width=2,
            border_color=self.priColor,
            height=40,
            width=200,
            show="*"
        )
        
        self.passwordvar = self.passwordEntry.get()

        showPass = ctk.CTkButton(
            master=self.loginFrame,
            text="",
            command=lambda:[self.seePass(self.passwordEntry, showPass)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.see
        )

        loginButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Login",
            command= lambda: [self.getValue(self.loginEntry, self.passwordEntry), self.callloading(self.login, self.loginFrame, lambda: self.logged(self.user_id), lambda : self.validLogin(self.values[0], self.values[1]))], 
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        signupButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Signup",
            command=lambda: [self.loginFrame.destroy(), self.signup()],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.loginFrame,
            text="",
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        self.loginEntry.pack(padx=50, pady=10)
        self.passwordEntry.pack(padx=50, pady=10)
        showPass.place(relx=0.85, rely=0.39)
        loginButton.pack(padx=50, pady=10)
        signupButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: [ self.getValue(self.loginEntry, self.passwordEntry), self.callloading(self.login, self.loginFrame, lambda: self.logged(self.user_id), lambda : self.validLogin(self.values[0], self.values[1]))])


    def signup(self):
        """
        Sets up the signup page.

        Args:
            self: The instance of the class.

        Functionality:
            - Creates and configures the signup frame.
            - Creates labels, entry fields, buttons, and icons for signup, login entry, password entry, password confirmation entry, show/hide password, signup button, login button, and theme change button.
            - Binds the Return key to trigger the addCad method when pressed.
            - Places all widgets within the signup frame with appropriate configurations.
        """
        self.signupFrame = ctk.CTkFrame(master=self.app,)
        self.app.title("Signup")
        self.signupFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Heart.ico")
        
        title = ctk.CTkLabel(
            master=self.signupFrame, 
            text="Signup",
            font=ctk.CTkFont(family="Helvetica",
                            size=36, weight="bold",
                            slant="italic")
        )

        loginEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            border_width=2,
            border_color=self.priColor,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            border_width=2,
            border_color=self.priColor,
            height=40,
            width=200,
            show="*"
        )

        showpass = ctk.CTkButton(
            master=self.signupFrame,
            command=lambda:[self.seePass(passwordEntry, showpass)],
            text="",
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.see
        )

        passwordConfirmEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Password Confirm",
            font=("RobotoSlab", 12),
            border_width=2,
            border_color=self.priColor,
            height=40,
            width=200,
            show="*"
        )
        
        showPassConfirm = ctk.CTkButton(
            master=self.signupFrame,
            text="",
            command=lambda:[self.seePass(passwordConfirmEntry, showPassConfirm)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=10,
            image=self.see
        )

        signupButton = ctk.CTkButton(
            master=self.signupFrame,
            text="Signup",
            command=lambda: [self.addCad(loginEntry.get(), passwordEntry.get(), passwordConfirmEntry.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100,
        )

        
        loginButton = ctk.CTkButton(
            master=self.signupFrame,
            text="Login",
            command=lambda:[self.signupFrame.destroy(), self.login()],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )


        theme = ctk.CTkButton(
            master=self.signupFrame,
            text="",
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showpass.place(relx=0.85, rely=0.338)
        passwordConfirmEntry.pack(padx=50, pady=10)
        showPassConfirm.place(relx=0.85, rely=0.48)
        signupButton.pack(padx=50, pady=10)
        loginButton.pack(padx=50, pady=10)
        theme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.addCad(loginEntry.get(), passwordEntry.get(), passwordConfirmEntry.get()))


    def logged(self, user_id):
        """
        Sets up the logged page.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Creates and configures the logged frame.
            - Sets the title and icon for the application window.
            - Retrieves primary and secondary colors for the user interface.
            - Creates labels, buttons, entry fields, and icons for menu, mode selection, item filtering, table display, exit, configuration, theme change, add, delete, edit, and copy functionalities.
            - Binds the Return key to trigger the filterItens method when pressed.
            - Places all widgets within the logged frame with appropriate configurations.
        """
        self.loggedFrame = ctk.CTkFrame(master=self.app)
        self.app.title("MainDug")
        self.app.geometry("900x650")
        self.loggedFrame.pack(in_=self.app, anchor="center", fill='both', expand=True)
        self.app.iconbitmap(default="icons/Star.ico")
        self.priColor = self.c.findColor(user_id)
        self.secColor = self.c.darkColor(self.priColor, 50)
        
        modes = ['Filter', 'Site', 'Login', 'Password']
     
        title = ctk.CTkLabel(
            master=self.loggedFrame, 
            text="Menu",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        tableFixFrame = ctk.CTkScrollableFrame(
            master=self.loggedFrame,
            width=800,
            height=400)
        
        tableFrame = ctk.CTkFrame(
            master=tableFixFrame,
            height=10000)

        modeSelector = ctk.CTkComboBox(
            self.loggedFrame,
            values=modes,
            border_color=self.priColor,
            command=self.selectMode,
            button_color=self.priColor,
            width=80)
        
        filterEntry = ctk.CTkEntry(
            master=self.loggedFrame,
            border_color=self.priColor,
            placeholder_text='Item name',
            width=300)
        
        filterItens = ctk.CTkButton(
            self.loggedFrame,
            text='',
            command=lambda: self.filterItens(filterEntry.get(), user_id),
            width=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            image=self.search)
        
        unfilterButton = ctk.CTkButton(
            master= self.loggedFrame,
            text='',
            width=10,
            command= lambda: self.unfilter(user_id),
            fg_color=self.priColor,
            hover_color=self.secColor,
            image=self.x
        )

        table = CTkTable(
            master=tableFrame,
            row=len(self.passwords),
            column=4,
            values=self.passwords,
            width=200,
            colors=[self.priColor,'#292b29']
        )

        exitButton = ctk.CTkButton(
            master=self.loggedFrame,
            command=lambda: [self.loggedFrame.destroy(), self.login()],
            text="",
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.exit
        )

        configButton = ctk.CTkButton(
            master=self.loggedFrame,
            command=lambda: [self.loggedFrame.destroy(), self.config(user_id)],
            text="",
            height=10,
            width=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            image=self.Config
        )

        theme = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )

        add = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.add(user_id)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=50,
            height=10,
            width=10,
            image=self.Add
        )

        delete = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.deleteItem(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.Delete
        )

        edit = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.editLog(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=10,
            image=self.edit
        )

        copy = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.copyFunc(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.copy
        )


        configButton.place(relx=0.05, rely=0.05,anchor="center")
        title.place(relx=0.5, rely=0.05, anchor="center")

        modeSelector.place(relx=0.3, rely=0.15, anchor="e")
        filterEntry.place(relx=0.31, rely=0.15, anchor="w")
        unfilterButton.place(relx=0.65, rely = 0.15, anchor= 'w')
        filterItens.place(relx=0.7, rely=0.15, anchor="w")

        tableFixFrame.place(relx=0.5, rely=0.2, anchor="n")
        tableFrame.pack(fill='both', expand=True)
        table.place(in_=tableFrame)

        copy.place(relx=0.25,rely=0.9, anchor="center")
        edit.place(relx=0.35,rely=0.9, anchor="center")
        add.place(relx=0.45,rely=0.9, anchor="center")
        exitButton.place(relx=0.55, rely=0.9, anchor="center")
        theme.place(relx=0.65, rely=0.9, anchor="center")
        delete.place(relx=0.75,rely=0.9, anchor="center")

        self.app.bind("<Return>", lambda _: self.filterItens(filterEntry.get(), user_id))


    def config(self, user_id):
        """
        Sets up the configuration page.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Creates and configures the configuration frame.
            - Sets the title and icon for the application window.
            - Creates labels, buttons, and icons for account configuration options such as editing login, editing password, erasing account, and changing theme/color.
            - Binds the Back button to trigger the findPasswords and logged methods when clicked.
            - Places all widgets within the configuration frame with appropriate configurations.
        """
        self.configFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Config")
        self.configFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Star.ico")

        title = ctk.CTkLabel(
            master=self.configFrame, 
            text="Account Config:",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEditButton = ctk.CTkButton(
            master=self.configFrame,
            text="Edit Login",
            command=lambda: [self.configFrame.destroy(), self.editLogin(user_id)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        passEditButton = ctk.CTkButton(
            master=self.configFrame,
            text="Edit Password",
            command=lambda: [self.configFrame.destroy(), self.editPass(user_id)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        eraseButton = ctk.CTkButton(
            master=self.configFrame,
            text="Erase Account",
            command=lambda: [self.configFrame.destroy(), self.erase(user_id)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )
        
        backButton = ctk.CTkButton(
            master=self.configFrame,
            text="Back",
            command=lambda:[self.configFrame.destroy(), self.findPasswords(user_id), self.logged(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.configFrame,
            text="",
            command=lambda:[self.theme(changeTheme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            image=self.white
        )

        changeColor = ctk.CTkButton(
            master=self.configFrame,
            text="",
            command=lambda:self.askColor(user_id),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.newColor
        )

        title.pack(padx=50, pady=10)
        loginEditButton.pack(padx=50, pady=10)
        passEditButton.pack(padx=50, pady=10)
        eraseButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)
        changeColor.pack(padx=50, pady=10)


    def editLogin(self, user_id):
        """
        Sets up the edit login page.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Creates and configures the edit login frame.
            - Sets the title for the application window.
            - Creates labels, entry fields, buttons, and icons for entering new login, editing login, navigating back, and changing theme.
            - Binds the Return key to trigger the editCred method when pressed.
            - Places all widgets within the edit login frame with appropriate configurations.
        """
        self.editLoginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Login")
        self.editLoginFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)


        title = ctk.CTkLabel(
            master=self.editLoginFrame, 
            text="New Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEntry = ctk.CTkEntry(
            master=self.editLoginFrame,
            placeholder_text="New Login",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200
        )

        loginEditButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Edit Login",
            command=lambda:[self.editCred(user_id, "Login", loginEntry.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Back",
            command=lambda: [self.editLoginFrame.destroy(), self.config(user_id)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.editLoginFrame,
            text="",
            command=lambda:[self.theme(changeTheme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        loginEditButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.editCred(user_id, "Login", loginEntry.get()))


    def editPass(self, user_id):
        """
        Sets up the edit password page.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Creates and configures the edit password frame.
            - Sets the title for the application window.
            - Creates labels, entry fields, buttons, and icons for entering new password, confirming new password, editing password, navigating back, and changing theme.
            - Binds the Return key to trigger the editCred method when pressed.
            - Places all widgets within the edit password frame with appropriate configurations.
        """
        self.editPasswordFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Password")
        self.editPasswordFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)


        title = ctk.CTkLabel(
            master=self.editPasswordFrame, 
            text="New Password",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        passwordEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )
        

        showPass = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.seePass(passwordEntry, showPass)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.see
        )

        passwordConfirmEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password Confirm",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            border_color=self.priColor,
            width=200,
            show="*"
        )

        showPassConfirm = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.seePass(passwordConfirmEntry, showPassConfirm)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.see
        )

        passEditButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Edit Password",
            command=lambda: [self.editCred(user_id, "Password", [passwordEntry.get(), passwordConfirmEntry.get()])],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Back",
            command=lambda: [self.editPasswordFrame.destroy(), self.config(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        theme = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showPass.place(relx=0.8, rely=0.22)
        passwordConfirmEntry.pack(padx=50, pady=10)
        showPassConfirm.place(relx=0.8, rely=0.39)
        passEditButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        theme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _:self.editCred(user_id, "Password", [passwordEntry.get(), passwordConfirmEntry.get()]))


    def erase(self, user_id):
        """
        Sets up the erase page for deleting the account.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Creates and configures the erase frame.
            - Sets the title for the application window.
            - Creates labels, buttons, and icons for deleting the account, navigating back, and changing theme.
            - Binds the Return key to trigger the delete method when pressed.
            - Places all widgets within the erase frame with appropriate configurations.
        """
        self.eraseFrame = ctk.CTkFrame(master=self.app)
        self.app.title ("Erase")
        self.eraseFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Skull.ico")


        title = ctk.CTkLabel(
            master=self.eraseFrame, 
            text="Delete Account",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        eraseButton = ctk.CTkButton(
            master=self.eraseFrame,
            text="DELETE ACCOUNT",
            command=lambda: [self.delete(user_id)],
            font=("RobotoSlab", 12),
            border_color="#000000",
            hover_color="#000000",
            fg_color="red",
            corner_radius=20,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.eraseFrame,
            text="Back",
            command=lambda: [self.eraseFrame.destroy(), self.config(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.eraseFrame,
            text="",
            command=lambda:[self.theme(changeTheme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=10,
            image=self.white
        )
        
        title.pack(padx=50, pady=10)
        eraseButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.delete(user_id))


    def generatePass(self, user_id):
        self.generatePassFrame = ctk.CTkFrame(master=self.app)
        self.app.title("New Login")
        self.generatePassFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Alien.ico")

        title = ctk.CTkLabel(
            master=self.generatePassFrame,
            text="Add a new login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        passLen = ctk.CTkEntry(
            self.generatePassFrame,
            placeholder_text="Password Length",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200
                               )

        numberValue = ctk.StringVar(value="on")
        number = ctk.CTkCheckBox(self.generatePassFrame, text="Numbers",
                                     variable=numberValue, onvalue=True, offvalue=False)

        lowerLetterValue = ctk.StringVar(value="on")
        lowerLetter = ctk.CTkCheckBox(self.generatePassFrame, text="Lower Case Letters",
                                     variable=lowerLetterValue, onvalue=True, offvalue=False)

        upperLetterValue = ctk.StringVar(value="on")
        upperLetter = ctk.CTkCheckBox(self.generatePassFrame, text="Upper Case Letters",
                                     variable=upperLetterValue, onvalue=True, offvalue=False)

        symbolValue = ctk.StringVar(value="on")
        symbol = ctk.CTkCheckBox(self.generatePassFrame, text="Symbols",
                                     variable=symbolValue, onvalue=True, offvalue=False)
        
        confirmButton = ctk.CTkButton(
            master=self.generatePassFrame,
            text="Next",
            command=lambda: [self.fullGeneratePass(user_id, passLen.get(), upperLetterValue.get(), lowerLetterValue.get(), symbol.get(), numberValue.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        cancelButton = ctk.CTkButton(
            master=self.generatePassFrame,
            text="Cancel",
            command=lambda: [self.generatePassFrame.destroy(), self.findPasswords(user_id), self.logged(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        title.pack(padx=50, pady=30)
        passLen.pack(padx=50, pady=10)
        number.pack(padx=50, pady=10)
        symbol.pack(padx=50, pady=10)
        lowerLetter.pack(padx=50, pady=10)
        upperLetter.pack(padx=50, pady=10)
        confirmButton.pack(padx=50, pady=10)
        cancelButton.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.fullGeneratePass(id ,passLen.get(), upperLetterValue.get(), lowerLetterValue.get(), symbol.get(), numberValue.get()))

    def addLog(self, user_id):
        """
        Sets up the generate password page for creating a new login.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.

        Functionality:
            - Creates and configures the generate password frame.
            - Sets the title for the application window.
            - Creates input fields for specifying password length and options for including numbers, upper case letters, lower case letters, and symbols.
            - Creates buttons for confirming or canceling the password generation process.
            - Binds the Return key to trigger the fullGeneratePass method when pressed.
            - Places all widgets within the generate password frame with appropriate configurations.
        """
        self.addLogFrame = ctk.CTkFrame(master=self.app)
        self.app.title("New Login")
        self.addLogFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Alien.ico")


        title = ctk.CTkLabel(
            master=self.addLogFrame,
            text="Add a new login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        siteEntry = ctk.CTkEntry(
            master=self.addLogFrame,
            placeholder_text="Site",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200
        )

        loginEntry = ctk.CTkEntry(
            master=self.addLogFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.addLogFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        showPass = ctk.CTkButton(
            master=self.addLogFrame,
            text="",
            command=lambda:[self.seePass(passwordEntry, showPass)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.see
        )

        doneButton = ctk.CTkButton(
            master=self.addLogFrame,
            text="Done",
            command=lambda: [self.addLogDB(user_id, siteEntry.get(), loginEntry.get(), passwordEntry.get(), None)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        cancelButton = ctk.CTkButton(
            master=self.addLogFrame,
            text="Cancel",
            command=lambda: [self.addLogFrame.destroy(), self.findPasswords(user_id), self.logged(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.addLogFrame,
            text="",
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        siteEntry.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showPass.place(relx=0.78, rely=0.48)
        doneButton.pack(padx=50, pady=10)
        cancelButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.addLogDB(user_id, siteEntry.get(), loginEntry.get(), passwordEntry.get(), None))

    
    def editItem(self, user_id, itemId):
        """
        Sets up the edit item page for modifying a specific item.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            itemId (int): Identifier of the item to be edited.

        Functionality:
            - Creates and configures the edit item frame.
            - Sets the title for the application window.
            - Creates buttons for editing site, login, and password fields of the specified item.
            - Creates a button for canceling the editing process.
            - Binds the Return key to trigger the findPasswords method when pressed.
            - Places all widgets within the edit item frame with appropriate configurations.
        """
        self.editItemFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Item")
        self.editItemFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Alien.ico")


        title = ctk.CTkLabel(
            master=self.editItemFrame,
            text="Edit Item",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        siteButton = ctk.CTkButton(
            master=self.editItemFrame,
            text="Edit Site",
            command=lambda: [self.editItemFrame.destroy(), self.siteEdit(user_id, itemId)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        loginButton = ctk.CTkButton(
            master=self.editItemFrame,
            text="Edit Login",
            command=lambda: [self.editItemFrame.destroy(), self.loginEdit(user_id, itemId)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        passwordButton = ctk.CTkButton(
            master=self.editItemFrame,
            text="Edit Password",
            command=lambda: [self.editItemFrame.destroy(), self.passwordEdit(user_id, itemId)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        cancelButton = ctk.CTkButton(
            master=self.editItemFrame,
            text="Cancel",
            command=lambda: [self.editItemFrame.destroy(), self.findPasswords(user_id), self.logged(user_id)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.editItemFrame,
            text="",
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        siteButton.pack(padx=50, pady=10)
        loginButton.pack(padx=50, pady=10)
        passwordButton.pack(padx=50, pady=10)
        cancelButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)


    def siteEdit(self, user_id, itemId):
        """
        Sets up the edit site page for modifying the site field of a specific item.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            itemId (int): Identifier of the item to be edited.

        Functionality:
            - Creates and configures the edit site frame.
            - Sets the title for the application window.
            - Creates an entry field for entering the new site.
            - Creates a button for editing the site field of the specified item.
            - Creates a button for canceling the editing process.
            - Binds the Return key to trigger the editCred method with the "site" argument when pressed.
            - Places all widgets within the edit site frame with appropriate configurations.
        """
        self.editSiteFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit site")
        self.editSiteFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)


        title = ctk.CTkLabel(
            master=self.editSiteFrame, 
            text="New site",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        siteEntry = ctk.CTkEntry(
            master=self.editSiteFrame,
            placeholder_text="New site",
            border_color=self.priColor,
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200
        )

        siteEditButton = ctk.CTkButton(
            master=self.editSiteFrame,
            text="Edit site",
            command=lambda:[self.editLogFunc("site", user_id, itemId, siteEntry.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editSiteFrame,
            text="Back",
            command=lambda: [self.editSiteFrame.destroy(), self.editItem(user_id, itemId)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.editSiteFrame,
            text="",
            command=lambda:[self.theme(changeTheme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        siteEntry.pack(padx=50, pady=10)
        siteEditButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.editCred(id, "site", siteEntry.get()))


    def loginEdit(self, user_id, itemId):
        """
        Sets up the edit login page for modifying the login field of a specific item.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            itemId (int): Identifier of the item to be edited.

        Functionality:
            - Creates and configures the edit login frame.
            - Sets the title for the application window.
            - Creates an entry field for entering the new login.
            - Creates a button for editing the login field of the specified item.
            - Creates a button for canceling the editing process.
            - Binds the Return key to trigger the editCred method with the "Login" argument when pressed.
            - Places all widgets within the edit login frame with appropriate configurations.
        """
        self.editLoginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Login")
        self.editLoginFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)


        title = ctk.CTkLabel(
            master=self.editLoginFrame, 
            text="New Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEntry = ctk.CTkEntry(
            master=self.editLoginFrame,
            placeholder_text="New Login",
            border_color=self.priColor,
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200
        )

        loginEditButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Edit Login",
            command=lambda:[self.editLogFunc("login", user_id, itemId, loginEntry.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Back",
            command=lambda: [self.editLoginFrame.destroy(), self.editItem(user_id, itemId)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.editLoginFrame,
            text="",
            command=lambda:[self.theme(changeTheme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        loginEditButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.editCred(user_id, "Login", loginEntry.get()))


    def passwordEdit(self, user_id, itemId):
        """
        Sets up the edit password page for modifying the password field of a specific item.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            itemId (int): Identifier of the item to be edited.

        Functionality:
            - Creates and configures the edit password frame.
            - Sets the title for the application window.
            - Creates an entry field for entering the new password.
            - Creates a button for toggling password visibility.
            - Creates an entry field for confirming the new password.
            - Creates a button for editing the password field of the specified item.
            - Creates a button for canceling the editing process.
            - Creates a button for changing the theme.
            - Binds the Return key to trigger the passVerify method with the entered passwords, user_id, and itemId when pressed.
            - Places all widgets within the edit password frame with appropriate configurations.
        """
        self.editPasswordFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Password")
        self.editPasswordFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)


        title = ctk.CTkLabel(
            master=self.editPasswordFrame, 
            text="New Password",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        passwordEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password",
            border_color=self.priColor,
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200,
            show="*"
        )
        

        showPass = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.seePass(passwordEntry, showPass)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.see
        )

        passwordConfirmEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password Confirm",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        showPassConfirm = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.seePass(passwordConfirmEntry, showPassConfirm)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.see
        )

        passEditButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Edit Password",
            command=lambda: [self.passVerify(passwordEntry.get(),passwordConfirmEntry.get(), user_id, itemId)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            fg_color=self.priColor,
            hover_color=self.secColor,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Back",
            command=lambda: [self.editPasswordFrame.destroy(), self.editItem(user_id, itemId)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        theme = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        passwordConfirmEntry.pack(padx=50, pady=10)
        passEditButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        theme.pack(padx=50, pady=10)


    def addWithPass(self, user_id, password):
        """
        Sets up the page for adding a new login with a pre-determined password.

        Args:
            self: The instance of the class.
            user_id (int): Identifier of the user.
            password (str): The pre-determined password to be associated with the new login.

        Functionality:
            - Creates and configures the frame for adding a new login with a pre-determined password.
            - Sets the title for the application window.
            - Creates an entry field for entering the site name.
            - Creates an entry field for entering the login username.
            - Creates a button for adding the new login to the database.
            - Creates a button for canceling the addition process.
            - Creates a button for changing the theme.
            - Binds the Return key to trigger the addLogDB method with the entered site name, login username, password, user_id, and frame when pressed.
            - Places all widgets within the add password frame with appropriate configurations.
        """
        self.addPassFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Login")
        self.addPassFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Alien.ico")

        title = ctk.CTkLabel(
            master=self.addPassFrame,
            text="Add New Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        site = ctk.CTkEntry(
            master=self.addPassFrame,
            placeholder_text="site",
            font=("RobotoSlab", 12),
            border_color=self.priColor,
            border_width=2,
            height=40,
            width=200
        )

        login = ctk.CTkEntry(
            master=self.addPassFrame,
            placeholder_text="login",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            border_color=self.priColor,
            width=200
        )

        done = ctk.CTkButton(
            master=self.addPassFrame,
            text="Done",
            command=lambda: [self.addLogDB(user_id, site.get(), login.get(), password, self.addPassFrame)],
            font=("RobotoSlab", 12),
            fg_color=self.priColor,
            hover_color=self.secColor,
            corner_radius=20,
            height=40,
            width=100
        )

        cancel = ctk.CTkButton(
            master=self.addPassFrame,
            text="Cancel",
            command=lambda: [self.loginFrame.destroy(), self.findPasswords(user_id), self.logged(user_id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.addPassFrame,
            text="",
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )
        
        title.pack(padx=50, pady=10)
        site.pack(padx=50, pady=10)
        login.pack(padx=50, pady=10)
        done.pack(padx=50, pady=10)
        cancel.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.addLogDB(user_id, site.get(), login.get(), password, self.addPassFrame))

    
    def loading(self):
        """
        Sets up the loading page for displaying a loading animation.

        Args:
            self: The instance of the class.

        Functionality:
            - Creates and configures the loading frame.
            - Sets the title for the application window.
            - Creates a loading animation using the tkinter.Animation module.
            - Creates a button for exiting the application.
            - Binds the Return key to trigger the exit method when pressed.
            - Places all widgets within the loading frame with appropriate configurations.
        """
        print("Loading...")
        self.loadingFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Loading...")
        self.loadingFrame.place(relx=0.5, rely=0.5, anchor="center")
        self.app.iconbitmap(default="icons/Alien.ico")

        title = ctk.CTkLabel(
            master=self.loadingFrame, 
            text="Loading...",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )
        
        wait = ctk.CTkLabel(
            master=self.loadingFrame,
            text='Please wait',
            font=ctk.CTkFont(family="Helvetica", size=16)
        )

        self.loadingbar = ctk.CTkProgressBar(master=self.loadingFrame, mode='indeterminate', progress_color=self.priColor)
        self.loadingbar.start()

        title.pack(padx=100, pady=5)
        wait.pack(padx=50, pady=0)
        self.loadingbar.pack(padx=50, pady=10)
        

    def loading_complete(self):
        self.loadingbar.stop()
        self.loadingFrame.destroy()
        print("Loading finished")

    
if __name__ == "__main__":
    """
    Entry point of the application.
    
    Functionality:
        - Instantiates the View class.
        - Starts the application.
    """
    view = View()