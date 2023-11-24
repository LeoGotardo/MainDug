import customtkinter as ctk
from tkinter import messagebox as msg
from controller import Controller


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


    def validLogin(self, login, password):
        # Verifica se o login é válido e realiza a ação apropriada
        itens = self.c.verify(login, password)
        if itens[0] == True:
            self.loginFrame.destroy()
            self.logged(itens[1])
        else:
            self.alert(itens[2])


    def addCad(self, login, password, passwordConfirm):
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.credencialADD(login, password, passwordConfirm)
        if error == "Valid Cadaster":
            self.alert("Sussesfull Login", self.app)
        else:
            self.alert(error, self.app)


    def alert(self, text):
        # Exibe um alerta na página
        msg.showwarning(title="Error",message=text)


    def login(self):
        # Configura a página de login
        self.loginFrame = ctk.CTkFrame(master=self.app)
        self.app.title ("Login")
        self.app.bgcolor = self.primaryC
        self.loginFrame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            master=self.loginFrame,
            text="Login"
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
            corner_radius=10,
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
            corner_radius=10,
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
            text="Signup"
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
            command=lambda: [self.addCad(signupEntry.get(), passwordEntry.get(), passwordConfirmEntry.get(), self.app)],
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=10,
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
            corner_radius=10,
            height=40,
            width=100
        )

        title.pack(padx=10, pady=10)
        signupEntry.pack(padx=10, pady=10)
        passwordEntry.pack(padx=10, pady=10)
        passwordConfirmEntry.pack(padx=10, pady=10)
        signupButton.pack(padx=10, pady=10)
        loginButton.pack(padx=10, pady=10)


    def logged(self, id):
        pass


    def edit(self, id):
        pass
    

if __name__ == "__main__":
    view = View()
    