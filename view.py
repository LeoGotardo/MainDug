import customtkinter as ctk
import tkinter as tk
from controller import Controller


class View:
    def __init__(self):
        self.c = Controller()
        tablExist = self.c.start()
        self.app = ctk.CTk()

        self.primaryC = "black"
        self.secC = "light_blue"
        self.theme = ctk.set_appearance_mode('dark')

        self.login(ctk.CTkFrame)


    def createButton(self, text, func):
        # Cria um botão personalizado
        button = ctk.CTkButton(
            master=self.app,
            text=text,
            command=func,
            text_font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=10,
            height=40,
            width=100
        )
        button.pack()
        return button


    def createEntry(self, place, password, see, auto_focus):
        # Cria um rótulo personalizado
        entry = ctk.CTkEntry(
            master=self.app,
            placeholder_text=place,
            show=not password,
            reveal=see,
            autofocus=auto_focus,
            text_font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200
        )
        entry.pack()
        return entry


    def sort(self, elements, align, page: ctk.CTkFrame):
        # Adiciona elementos à página em uma linha com alinhamento específico
        for element in elements:
            page.add(element, align=align)


    def validLogin(self, login, password, page):
        # Verifica se o login é válido e realiza a ação apropriada
        itens = self.c.verify(login, password)
        if itens[0] == True:
            self.pageSwitch("Logged", itens[1])
        else:
            self.alert(itens[2], page)


    def addCad(self, login, password, passwordConfirm, page):
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.credencialADD(login, password, passwordConfirm)
        if error == "Valid Cadaster":
            self.alert("Sussesfull Login", page)
        else:
            self.alert(error, page)


    def colorChange(self, goTo, page):
        # Altera as cores da interface e muda para a página desejada
        color1 = self.primaryC
        color2 = self.secC
        self.primaryC = color2
        self.secC = color1
        self.pageSwitch(goTo, None, page)


    def alert(self, text, page: ctk.CTkFrame):
        # Exibe um alerta na página
        ctk.CTkMessageBox.show_info("Alerta", text, text_font=("RobotoSlab", 12), text_color=self.secC, border_color=self.primaryC)


    def pageSwitch(self, goTo, id, page: ctk.CTkFrame):
        # Altera para a página desejada com base na ação fornecida
        if goTo == "Signup":
            page.clean()
            self.signup(page)
        elif goTo == "Login":
            page.clean()
            self.login(page)
        elif goTo == "Logged":
            page.clean()
            self.logged(page)
        elif goTo == "Edit":
            page.clean()
            self.edit(page, id)
        return goTo


    def login(self, page: ctk.CTkFrame):
        # Configura a página de login
        page.title = "Login"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.bgcolor = self.primaryC

        title = ctk.CTkTextbox(self.app)

        loginLabel = self.createEntry("Login", False, False, True)
        passwordLabel = self.createEntry("Password", True, True, False)

        loginButton = self.createButton("Login",lambda e: self.validLogin(loginLabel.value, passwordLabel.value, page))
        signupButton = self.createButton("Signup",lambda e: self.pageSwitch("Signup", None, page))

        elements = [title, loginLabel, passwordLabel, loginButton, signupButton]
        self.sort(elements, ctk.MainAxisAlignment.CENTER, page)


    def signup(self, page: ctk.CTkFrame):
        # Configura a página de cadastro
        page.title = "Signup"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.bgcolor = self.primaryC

        title = ctk.CTkTextbox(self.app)

        loginLabel = self.createEntry("Login", False, False, True)
        passwordLabel = self.createEntry("Password", True, True, False)
        passwordConfirmLabel = self.createEntry("Password Confirm", True, True, False)

        signupButton = self.createButton("Signup",lambda e: [self.addCad(loginLabel.value,passwordLabel.value,passwordConfirmLabel.value,page)])

        elements = [title, loginLabel, passwordLabel, passwordConfirmLabel, signupButton]
        self.sort(elements, ctk.MainAxisAlignment.CENTER, page)


if __name__ == "__main__":
    view = View()
