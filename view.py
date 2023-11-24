import customtkinter as ctk
import os
from tkinter import messagebox as msg
from controller import Controller


class View(ctk.CTk):
    def __init__(self):
        self.c = Controller()
        tablExist = self.c.start()
        self.app = ctk.CTk()

        self.primaryC = "black"
        self.secC = "white"
        self.theme = ctk.set_appearance_mode('dark')
        self.app.geometry("500x500")
        self.login()

        self.app.mainloop()


    
    def createLabel(self, text, frame, column, row):
        label = ctk.CTkLabel(master=frame, text=text)
        label.grid(column=column, row=row)


    def createButton(self, text, func, frame, column, row):
        # Cria um botão personalizado
        button = ctk.CTkButton(
            master=frame,
            text=text,
            command=func,
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=10,
            height=40,
            width=100
        )
        button.grid(column=column, row=row)


    def createEntry(self, place, frame, column, row, password):
        # Cria um rótulo personalizado
        entry = ctk.CTkEntry(
            master=frame,
            placeholder_text=place,
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200
        )
        if password == True:
            entry.configure(show="*")
        entry.grid(column=column, row=row)


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

        title = self.createLabel("Login", self.loginFrame, 2, 0)
        

        loginEntry = self.createEntry("Login", self.loginFrame, 2, 1, False)
        passwordEntry = self.createEntry("Password", self.loginFrame, 2, 2, True)

        loginButton = self.createButton("Login", lambda: self.validLogin(loginEntry.get(), passwordEntry.get(), self.app), self.loginFrame, 2, 3)
        signupButton = self.createButton("Signup", lambda: [self.loginFrame.destroy(), self.signup()], self.loginFrame, 2, 4)


    def signup(self):
        # Configura a página de cadastro
        os.system("cls")
        self.signupFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Signup")
        self.app.bgcolor = self.primaryC
        self.signupFrame.pack(fill="both", expand=True)

        title = self.createLabel("Signup", self.signupFrame, 2, 0)

        loginEntry = self.createEntry("Login", self.signupFrame, 2, 1, False)
        passwordEntry = self.createEntry("Password", self.signupFrame, 2, 2, True)
        passwordConfirmEntry = self.createEntry("Password Confirm", self.signupFrame, 2, 3, True)

        signupButton = self.createButton("Signup", lambda: [self.addCad(loginEntry.get(),passwordEntry.get(),passwordConfirmEntry.get(),self.app)], self.signupFrame, 2, 4)
        loginButton = self.createButton("Login", lambda:[self.signupFrame.destroy(), self.login()], self.signupFrame, 2, 5)


    def logged(self, id):
        pass


    def edit(self, id):
        pass
    

if __name__ == "__main__":
    view = View()
    