import customtkinter as ctk
from tkinter import messagebox as msg
from controller import Controller
import PIL as P
from PIL import ImageTk as imgTK
from PIL import Image as img
import Debug as d


class View(ctk.CTk):
    def __init__(self):
        self.c = Controller()
        self.tablExist = self.c.start()
        self.app = ctk.CTk()

        self.theme = ctk.set_appearance_mode('dark')
        self.app.geometry("500x500")
        self.see = ctk.CTkImage(dark_image=img.open("icons/see.ico"))
        self.unsee = ctk.CTkImage(dark_image=img.open("icons/unsee.ico"))
        self.login()

        self.app.mainloop()

    
    def isNew(self, id, paramter, newPar, frame):
        new = self.c.isNew(id, paramter, newPar)
        if new == "new":
            sull = self.c.edit(id, paramter, newPar)
            self.alert("Susses", sull)

            if frame == "editLoguin":
                self.editLoginFrame.destroy()
                self.logged(id)
            elif frame == "editPassword":
                self.editPasswordFrame.destroy()
                self.logged(id)
            elif frame == "eraseFrame":
                self.eraseFrame.destroy()
                self.logged(id)
        else:
            self.alert("ERROR",new)

    def delete(self, id):
        response = msg.askquestion(title="Delete Account",
                               message="Are you sure you want to delete this account? This action cannot be undone.",
                               icon="warning")  # Use askquestion for a clear yes/no choice
        if response == "yes":
            try:
                # Perform account deletion logic here
                self.c.erase(id)
                print(f"{d.Margin}Account {id} deleted successfully.{d.Margin}")
                self.eraseFrame.destroy()
                self.login()
            except Exception as e:
                print(f"{d.Margin}Account deletion failed: {e}{d.Margin}")
                msg.showerror("Error", "An error occurred while deleting the account.")
        else:
            print("Account deletion canceled.")

    def validLogin(self, login, password):
        # Verifica se o login é válido e realiza a ação apropriada
        if login != '' or password != '':
            itens = self.c.verify(login, password)
            print(f"{d.Margin}Itens:{itens}\nLogin:{login}\nPassword:{password}{d.Margin}")
            if itens[1] == True:
                self.loginFrame.destroy()
                self.logged(itens[0])
            else:
                self.alert("ERROR",itens[2])
                self.loginFrame.destroy()
                self.login()
        else:
            self.alert("ERROR", "Login or Password can't be empty")
            self.loginFrame.destroy()
            self.login()


    def addCad(self, login, password, passwordConfirm):
        print(f"{d.Margin}Login:{login} \nPassword:{password}\nPasswordConfirm:{passwordConfirm}{d.Margin}")
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.credencialADD(login, password, passwordConfirm)
        print(f"{d.Margin}error = {error}{d.Margin}")
        if error[0] == "Valid Login":
            self.alert("Susses","Sussesfull Login")
            self.signupFrame.destroy()
            self.login()
        else:
            self.alert("ERROR",error[0])
            self.signupFrame.destroy()
            self.signup()

    
    def seePass(self, entry, button):
        if entry.cget('show') == "*":
            entry.configure(show="")
            button.configure(image=self.unsee)
        elif entry.cget('show') == "":
            entry.configure(show="*")
            button.configure(image=self.see)

    def theme(frame, button):
        if frame.cget('set_appearance_mode') == 'dark':
            frame.configure(ctk.set_appearance_mode('ligth'))
            button.configure(image='icons/Dark.ico')
        elif frame.cget('set_appearance_mode') == 'ligth':
            frame.configure(ctk.set_appearance_mode('dark'))
            button.configure(image='icons/White.ico')


    def alert(self, title, text):
        # Exibe um alerta na página
        msg.showwarning(title=title,message=text)


    def login(self):
        # Configura a página de login
        self.loginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Login")
        self.loginFrame.pack(fill=ctk.BOTH, expand=True)
        self.app.iconbitmap(default="icons/Alien.ico")
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

        theme = ctk.CTkButton(
            master=self.loginFrame,
            text="",
            command=lambda:[self.theme(self.loginFrame, theme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=img.open("icons/White.ico")
        )


        title.pack(padx=10, pady=10)
        loginEntry.pack(padx=10, pady=10)
        passwordEntry.pack(padx=10, pady=10)
        showPass.pack(padx=10, pady=10)
        loginButton.pack(padx=10, pady=10)
        signupButton.pack(padx=10, pady=10)


    def signup(self):
        # Configura a página de cadastro
        self.signupFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Signup")
        self.signupFrame.pack(fill="both", expand=True)
        self.app.iconbitmap(default="icons/Heart.ico")
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
            image=img.open("icons/White.ico")
        )

        title.pack(padx=10, pady=10)
        loginEntry.pack(padx=10, pady=10)
        passwordEntry.pack(padx=10, pady=10)
        showpass.pack(padx=10, pady=10)
        passwordConfirmEntry.pack(padx=10, pady=10)
        showPassConfirm.pack(padx=10, pady=10)
        signupButton.pack(padx=10, pady=10)
        loginButton.pack(padx=10, pady=10)
        theme.pack(padx=10, pady=10)


    def logged(self, id):
        self.loggedFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Logged")
        self.loggedFrame.pack(fill=ctk.BOTH, expand=True)
        self.app.iconbitmap(default="icons/Star.ico")
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

        theme = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.theme(self.loggedFrame, theme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=img.open("icons/White.ico")
        )


        title.pack(padx=10, pady=10)
        loginEditButton.pack(padx=10, pady=10)
        passEditButton.pack(padx=10, pady=10)
        eraseButton.pack(padx=10, pady=10)
        exitButton.pack(padx=10, pady=10)
        theme.pack(padx=10, pady=10)


    def editLogin(self, id):
        self.editLoginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Login")
        self.editLoginFrame.pack(fill=ctk.BOTH, expand=True)
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

        theme = ctk.CTkButton(
            master=self.editLoginFrame,
            text="",
            command=lambda:[self.theme(self.editLoginFrame, theme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=img.open("icons/White.ico")
        )


        title.pack(padx=10, pady=10)
        loginEntry.pack(padx=10, pady=10)
        loginEditButton.pack(padx=10, pady=10)
        backButton.pack(padx=10, pady=10)
        theme.pack(padx=10, pady=10)


    def editPass(self, id):
        self.editPasswordFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Password")
        self.editPasswordFrame.pack(fill=ctk.BOTH, expand=True)
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
            image=img.open("icons/White.ico")
        )


        title.pack(padx=10, pady=10)
        passwordEntry.pack(padx=10, pady=10)
        passwordConfirmEntry.pack(padx=10, pady=10)
        passEditButton.pack(padx=10, pady=10)
        backButton.pack(padx=10, pady=10)
        theme.pack(padx=10, pady=10)


    def erase(self, id):
    # Configura a página Erase
        self.eraseFrame = ctk.CTkFrame(master=self.app)
        self.app.title ("Erase")
        self.eraseFrame.pack(fill=ctk.BOTH, expand=True)
        self.app.iconbitmap(default="icons/Skull.ico")
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

        theme = ctk.CTkButton(
            master=self.eraseFrame,
            text="",
            command=lambda:[self.theme(self.eraseFrame, theme)],
            font=("RobotoSlab", 12),
            fg_color='#343638',
            hover_color='#343638',
            corner_radius=50,
            height=10,
            width=10,
            image=img.open("icons/White.ico")
        )


        title.pack(padx=10, pady=10)
        eraseButton.pack(padx=10, pady=10)
        backButton.pack(padx=10, pady=10)
        theme.pack(padx=10, pady=10)



if __name__ == "__main__":
    view = View()
