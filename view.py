import customtkinter as ctk
from tkinter import messagebox as msg
from controller import Controller
import Debug as d


class View(ctk.CTk):
    def __init__(self):
        self.c = Controller()
        self.tablExist = self.c.start()
        self.app = ctk.CTk()

        self.primaryC = "black"
        self.secC = "white"
        self.theme = ctk.set_appearance_mode('dark')
        self.app.geometry("500x500")
        self.login()

        self.app.mainloop()

    
    def isNew(self, id, paramter, newPar):
        new = self.c.same(id, paramter, newPar)
        if new == "new":
            sull = self.c.edit(id, paramter, newPar)
            self.alert("Susses", sull)
            self.editLoginFrame.destroy()
            self.logged(id)
        else:
            self.alert("ERROR",new)


    def validLogin(self, login, password):
        # Verifica se o login é válido e realiza a ação apropriada
        itens = self.c.verify(login, password)
        print(f"{d.Margin}{d.Default}Itens:{itens}\nLogin:{login}\nPassword:{password}{d.Margin}")
        if itens[0] == True:
            self.loginFrame.destroy()
            self.logged(itens[1])
        else:
            self.alert("ERROR",itens[2])


    def addCad(self, login, password, passwordConfirm):
        print(f"{d.Default}Login:{login} \nPassword:{password}\nPasswordConfirm:{passwordConfirm}{d.Margin}")
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.credencialADD(login, password, passwordConfirm)
        if error == "Valid Login":
            self.alert("Susses","Sussesfull Login")
        else:
            self.alert("ERROR",error)


    def alert(self, title, text):
        # Exibe um alerta na página
        msg.showwarning(title=title,message=text)


    def login(self):
        # Configura a página de login
        self.loginFrame = ctk.CTkFrame(master=self.app)
        self.app.title ("Login")
        self.app.bgcolor = self.primaryC
        self.loginFrame.pack(fill=ctk.BOTH, expand=True)

        title = ctk.CTkLabel(
            master=self.loginFrame,
            text="Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")

        )

        loginEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        loginButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Login",
            command=lambda: self.validLogin(loginEntry.get(), passwordEntry.get()),
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        signupButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Signup",
            command=lambda: [self.loginFrame.destroy(), self.signup()],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        title.pack(padx=10, pady=10)
        loginEntry.pack(padx=10, pady=10)
        passwordEntry.pack(padx=10, pady=10)
        loginButton.pack(padx=10, pady=10)
        signupButton.pack(padx=10, pady=10)


    def signup(self):
        # Configura a página de cadastro
        self.signupFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Signup")
        self.app.bgcolor = self.primaryC
        self.signupFrame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            master=self.signupFrame, 
            text="Signup",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        signupEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        passwordConfirmEntry = ctk.CTkEntry(
            master=self.signupFrame,
            placeholder_text="Password Confirm",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        signupButton = ctk.CTkButton(
            master=self.signupFrame,
            text="Signup",
            command=lambda: [self.addCad(signupEntry.get(), passwordEntry.get(), passwordConfirmEntry.get())],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )
        
        loginButton = ctk.CTkButton(
            master=self.signupFrame,
            text="Login",
            command=lambda:[self.signupFrame.destroy(), self.login()],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        title.pack(fill=ctk.BOTH, padx=10, pady=10)
        signupEntry.pack(fill=ctk.BOTH, padx=10, pady=10)
        passwordEntry.pack(fill=ctk.BOTH, padx=10, pady=10)
        passwordConfirmEntry.pack(fill=ctk.BOTH, padx=10, pady=10)
        signupButton.pack(fill=ctk.BOTH, padx=10, pady=10)
        loginButton.pack(fill=ctk.BOTH, padx=10, pady=10)


    def logged(self, id):
        self.loggedFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Logged")
        self.app.bgcolor = self.primaryC
        self.loggedFrame.pack(fill=ctk.BOTH, expand=True)

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
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        passEditButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Edit Password",
            command=lambda: [self.loggedFrame.destroy(), self.editPass(id)],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        eraseButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Erase Account",
            command=lambda: [self.loggedFrame.destroy(), self.erase(id)],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )
        
        exitButton = ctk.CTkButton(
            master=self.loggedFrame,
            text="Exit",
            command=lambda:[self.loggedFrame.destroy(), self.login()],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        title.pack(fill=ctk.BOTH, padx=10, pady=10)
        loginEditButton.pack(fill=ctk.BOTH, padx=10, pady=10)
        passEditButton.pack(fill=ctk.BOTH, padx=10, pady=10)
        eraseButton.pack(fill=ctk.BOTH, padx=10, pady=10)
        exitButton.pack(fill=ctk.BOTH, padx=10, pady=10)


    def editLogin(self, id):
        self.editLoginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Login")
        self.app.bgcolor = self.primaryC
        self.editLoginFrame.pack(fill=ctk.BOTH, expand=True)

        title = ctk.CTkLabel(
            master=self.editLoginFrame, 
            text="New Login",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        loginEntry = ctk.CTkEntry(
            master=self.editLoginFrame,
            placeholder_text="New Login",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200
        )

        loginEditButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Edit Login",
            command=lambda:[self.isNew(id, "login", loginEntry.get())],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Back",
            command=lambda: [self.editLoginFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        title.pack(fill=ctk.BOTH, padx=10, pady=10)
        loginEntry.pack(fill=ctk.BOTH, padx=10, pady=10)
        loginEditButton.pack(fill=ctk.BOTH, padx=10, pady=10)
        backButton.pack(fill=ctk.BOTH, padx=10, pady=10)


    def editPass(self, id):
        self.editPasswordFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Edit Password")
        self.app.bgcolor = self.primaryC
        self.editPasswordFrame.pack(fill=ctk.BOTH, expand=True)

        title = ctk.CTkLabel(
            master=self.editPasswordFrame, 
            text="New Password",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        passwordEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        passwordConfirmEntry = ctk.CTkEntry(
            master=self.editPasswordFrame,
            placeholder_text="New Password Confirm",
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200,
            show="*"
        )

        passEditButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Edit Password",
            command=lambda: [self.m.edit(id, "password", passwordEntry.get())],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        backButton = ctk.CTkButton(
            master=self.editPasswordFrame,
            text="Back",
            command=lambda: [self.editPasswordFrame.destroy(), self.loggedFrame(id)],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=20,
            height=40,
            width=100
        )

        title.pack(fill=ctk.BOTH, padx=10, pady=10)
        passwordEntry.pack(fill=ctk.BOTH, padx=10, pady=10)
        passwordConfirmEntry.pack(fill=ctk.BOTH, padx=10, pady=10)
        passEditButton.pack(fill=ctk.BOTH, padx=10, pady=10)
        backButton.pack(fill=ctk.BOTH, padx=10, pady=10)


    def erase(self, id):
        self.alert("Susses", "Erase")


if __name__ == "__main__":
    view = View()