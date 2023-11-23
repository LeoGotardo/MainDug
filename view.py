import customtkinter as ctk
from controller import Controller


class View:
    def __init__(self):
        self.c = Controller()
        tablExist = self.c.start()
        self.app = ctk.CTk()

        self.primaryC = "black"
        self.secC = "white"
        self.theme = ctk.set_appearance_mode('dark')

        self.login()


    def createButton(self, text, func):
        # Cria um botão personalizado
        button = ctk.CTkButton(
            master=self.app,
            text=text,
            command=func,
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.primaryC,
            corner_radius=10,
            height=40,
            width=100
        )
        button.pack()
        return button


    def createEntry(self, place):
        # Cria um rótulo personalizado
        entry = ctk.CTkEntry(
            master=self.app,
            placeholder_text=place,
            font=("RobotoSlab", 12),
            text_color=self.secC,
            border_color=self.secC,
            border_width=2,
            height=40,
            width=200
        )
        entry.pack()
        return entry


    def validLogin(self, login, password):
        # Verifica se o login é válido e realiza a ação apropriada
        itens = self.c.verify(login, password)
        if itens[0] == True:
            self.pageSwitch("Logged", itens[1])
        else:
            self.alert(itens[2])


    def addCad(self, login, password, passwordConfirm):
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.credencialADD(login, password, passwordConfirm)
        if error == "Valid Cadaster":
            self.alert("Sussesfull Login", self.app)
        else:
            self.alert(error, self.app)


    def colorChange(self, goTo):
        # Altera as cores da interface e muda para a página desejada
        color1 = self.primaryC
        color2 = self.secC
        self.primaryC = color2
        self.secC = color1
        self.pageSwitch(goTo, None)


    def alert(self, text):
        # Exibe um alerta na página
        ctk.CTkMessageBox.show_info("Alerta", text, text_font=("RobotoSlab", 12), text_color=self.secC, border_color=self.primaryC)


    def pageSwitch(self, goTo, id):
        # Altera para a página desejada com base na ação fornecida
        if goTo == "Signup":
            self.app.clean()
            self.signup(self.app)
        elif goTo == "Login":
            self.app.clean()
            self.login(self.app)
        elif goTo == "Logged":
            self.app.clean()
            self.logged(self.app)
        elif goTo == "Edit":
            self.app.clean()
            self.edit(self.app, id)
        return goTo


    def login(self):
        # Configura a página de login
        self.app.title = "Login"
        self.app.vertical_alignment = "center"
        self.app.horizontal_alignment = "center"
        self.app.bgcolor = self.primaryC
        self.app.geometry("500x500")

        title = ctk.CTkTextbox(self.app)

        loginLabel = self.createEntry("Login")
        passwordLabel = self.createEntry("Password")

        loginButton = self.createButton("Login",lambda: self.validLogin(loginLabel.value, passwordLabel.value, self.app))
        signupButton = self.createButton("Signup",lambda: self.pageSwitch("Signup", None))
        self.app.mainloop()

    def signup(self):
        # Configura a página de cadastro
        self.app.title = "Signup"
        self.app.vertical_alignment = "center"
        self.app.horizontal_alignment = "center"
        self.app.bgcolor = self.primaryC

        title = ctk.CTkTextbox(self.app)

        loginLabel = self.createEntry("Login")
        passwordLabel = self.createEntry("Password")
        passwordConfirmLabel = self.createEntry("Password Confirm")

        signupButton = self.createButton("Signup",lambda: [self.addCad(loginLabel.value,passwordLabel.value,passwordConfirmLabel.value,self.app)])
        self.app.mainloop()

if __name__ == "__main__":
    view = View()
