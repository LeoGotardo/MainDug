import customtkinter as ctk
from tkinter import messagebox as msg
from controller2 import Controller
from PIL import Image as img

class View(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.app = ctk.CTk()

        self.app.geometry("500x500")
        self.see = ctk.CTkImage(dark_image=img.open("./icons/see.ico"))
        self.unsee = ctk.CTkImage(dark_image=img.open("./icons/unsee.ico"))
        self.white = ctk.CTkImage(dark_image=img.open("./icons/White.ico"))
        self.dark = ctk.CTkImage(dark_image=img.open("./icons/Dark.ico"))
        self.login()

        self.app.mainloop()

    def valid_login(self, login, password):
        user_id = self.controller.find_user_id(login, password)
        if user_id:
            self.loginFrame.destroy()
            self.logged(user_id)
        else:
            self.alert("ERROR", "Invalid login or password")

    def add_user(self, login, password, password_confirm):
        user_added = self.controller.add_user(login, password, password_confirm)
        if user_added:
            self.alert("Success", "User successfully added")
            self.signupFrame.destroy()
            self.login()
        else:
            self.alert("ERROR", "Error adding user")

    def delete_user(self, user_id):
        response = msg.askquestion("Delete Account", "Are you sure you want to delete this account?", icon="warning")
        if response == "yes":
            delete_successful = self.controller.delete_user(user_id)
            if delete_successful:
                self.eraseFrame.destroy()
                self.login()
            else:
                msg.showerror("Error", "An error occurred while deleting the account.")

    def update_user(self, user_id, parameter, new_value):
        update_successful = self.controller.update_user(user_id, parameter, new_value)
        if update_successful:
            self.alert("Success", "User information updated successfully")
        else:
            self.alert("ERROR", "Error updating user information")

    def seePass(self, entry, button):
        if entry.cget('show') == "*":
            entry.configure(show="")
            button.configure(image=self.unsee)
        else:
            entry.configure(show="*")
            button.configure(image=self.see)

    def theme(self, frame, button):
        current_mode = ctk.get_appearance_mode()
        new_mode = 'light' if current_mode == 'dark' else 'dark'
        ctk.set_appearance_mode(new_mode)
        button.configure(image=self.dark if new_mode == 'light' else self.white)

    def alert(self, title, text):
        msg.showwarning(title=title, message=text)

    def login(self):
        # Configura a página de login
        self.loginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Login")
        self.loginFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="./icons/Alien.ico")
        ctk.set_appearance_mode('dark')

        title = ctk.CTkLabel(
            master=self.loginFrame,
            text="Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        showPass = ctk.CTkButton(
            master=self.loginFrame,
            text="",
            command=lambda:[self.seePass(passwordEntry, showPass)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.see
        )

        loginButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Login",
            command=lambda: [self.validLogin(loginEntry.get(), passwordEntry.get())],
            font=("RobotoSlab", 12),
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
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.loginFrame,
            text="",
            command=lambda:self.theme(self.loginFrame, changeTheme),
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showPass.pack(padx=50, pady=10)
        loginButton.pack(padx=50, pady=10)
        signupButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)


    def signup(self):
        # Configura a página de cadastro
        self.signupFrame = ctk.CTkFrame(master=self.app,)
        self.app.title("Signup")
        self.signupFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="./icons/Heart.ico")
        ctk.set_appearance_mode('dark')

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
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        showpass = ctk.CTkButton(
            master=self.signupFrame,
            command=lambda:[self.seePass(passwordEntry, showpass)],
            text="",
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.see
        )

        passwordConfirmEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Password Confirm",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            bg_color='black',
            width=200,
            show="*"
        )
        
        showPassConfirm = ctk.CTkButton(
            master=self.signupFrame,
            text="",
            command=lambda:[self.seePass(passwordConfirmEntry, showPassConfirm)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.see
        )

        signupButton = ctk.CTkButton(
            master=self.signupFrame,
            text="Signup",
            command=lambda: [self.addCad(loginEntry.get(), passwordEntry.get(), passwordConfirmEntry.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100,
        )
        
        loginButton = ctk.CTkButton(
            master=self.signupFrame,
            text="Login",
            command=lambda:[self.signupFrame.destroy(), self.login()],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        theme = ctk.CTkButton(
            master=self.signupFrame,
            text="",
            command=lambda:[self.theme(self.signupFrame, theme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showpass.pack(padx=50, pady=10)
        passwordConfirmEntry.pack(padx=50, pady=10)
        showPassConfirm.pack(padx=50, pady=10)
        signupButton.pack(padx=50, pady=10)
        loginButton.pack(padx=50, pady=10)
        theme.pack(padx=50, pady=10)


    def logged(self, id):
        self.loggedFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Logged")
        self.loggedFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="./icons/Star.ico")
        ctk.set_appearance_mode('dark')

        title = ctk.CTkLabel(
            master=self.loggedFrame, 
            text="Logged",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEditButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Edit Login",
            command=lambda: [self.loggedFrame.destroy(), self.editLogin(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        passEditButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Edit Password",
            command=lambda: [self.loggedFrame.destroy(), self.editPass(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        eraseButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Erase Account",
            command=lambda: [self.loggedFrame.destroy(), self.erase(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )
        
        exitButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Exit",
            command=lambda:[self.loggedFrame.destroy(), self.login()],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.theme(self.loggedFrame, changeTheme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEditButton.pack(padx=50, pady=10)
        passEditButton.pack(padx=50, pady=10)
        eraseButton.pack(padx=50, pady=10)
        exitButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)


    def editLogin(self, id):
        self.editLoginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Login")
        self.editLoginFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        ctk.set_appearance_mode('dark')

        title = ctk.CTkLabel(
            master=self.editLoginFrame, 
            text="New Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEntry = ctk.CTkEntry(
            master=self.editLoginFrame,
            placeholder_text="New Login",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200
        )

        loginEditButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Edit Login",
            command=lambda:[self.isNew(id, "login", loginEntry.get(), "editLogin")],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Back",
            command=lambda: [self.editLoginFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.editLoginFrame,
            text="",
            command=lambda:[self.theme(self.editLoginFrame, changeTheme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        loginEditButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)


    def editPass(self, id):
        self.editPasswordFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Password")
        self.editPasswordFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        ctk.set_appearance_mode('dark')

        title = ctk.CTkLabel(
            master=self.editPasswordFrame, 
            text="New Password",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        passwordEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password",
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
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
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
            width=200,
            show="*"
        )

        showPassConfirm = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.seePass(passwordConfirmEntry, showPassConfirm)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.see
        )

        passEditButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Edit Password",
            command=lambda: [self.isNew(id, "password", passwordEntry.get(), "editPassword")],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Back",
            command=lambda: [self.editPasswordFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        theme = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="",
            command=lambda:[self.theme(self.editPasswordFrame, theme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
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


    def erase(self, id):
    # Configura a página Erase
        self.eraseFrame = ctk.CTkFrame(master=self.app)
        self.app.title ("Erase")
        self.eraseFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="./icons/Skull.ico")
        ctk.set_appearance_mode('dark')

        title = ctk.CTkLabel(
            master=self.eraseFrame, 
            text="Erase Account",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        eraseButton = ctk.CTkButton(
            master=self.eraseFrame,
            text="ERASE ACCOUNT",
            command=lambda: [self.delete(id)],
            font=("RobotoSlab", 12),
            text_color=self.secC,
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
            command=lambda: [self.eraseFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.eraseFrame,
            text="",
            command=lambda:[self.theme(self.eraseFrame, changeTheme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        eraseButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

if __name__ == "__main__":
    view = View()