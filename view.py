import flet as ft
from controller import Controller


class View:
    def __init__(self, page: ft.Page):
        self.c = Controller()
        tablExist = self.c.start()

        self.primaryC = ft.colors.BLACK
        self.secC = ft.colors.WHITE

        self.login(page)


    def createButton(self, text, func):
        button = ft.TextButton(text=text, on_click=func, style=ft.ButtonStyle(bgcolor={ft.MaterialState.DEFAULT: self.secC}, shape={ft.MaterialState.HOVERED : ft.RoundedRectangleBorder(radius=10)}, color=self.primaryC, animation_duration=500, padding=18))

        return button
    

    def createLabel(self, place, password, see, auto_focus):
        label = ft.TextField(label=place, password=password, can_reveal_password=see, autofocus=auto_focus, content_padding=10, color=self.secC, border_color=self.secC)

        return label
    

    def sort(self, elements, align, page: ft.Page):
        i = 0
        max = len(elements)

        for i in range(max):
            element = elements[i]
            page.add(ft.Row([element], alignment=align))

    
    def validLogin(self, login, password, page):
        itens = self.c.verify(login, password)
        print(itens)
        if itens[0] == True:
            self.pageSwitch("Logged", itens[1])
        else:
            self.alert(itens[2], page)

    
    def addCad(self, login, password, passwordConfirm, page):
        error = self.c.credencialADD(login, password, passwordConfirm)

        if error == "Valid Cadaster":
            self.alert("Sussesfull Login", page)
        else:
            self.alert(error, page)


    def colorChange(self, goTo, page):
        color1 = self.primaryC
        color2 = self.secC
        
        self.primaryC = color2
        self.secC = color1
        self.pageSwitch(goTo, None, page)

    
    def alert(self, text, page: ft.Page):
        dialog = ft.AlertDialog( title=ft.Text(text), actions=lambda e: [ft.TextButton("OK")], modal=True, actions_alignment=ft.MainAxisAlignment.END, open=True)
        
        page.add(dialog)
        page.update()


    def pageSwitch(self, goTo, id, page: ft.Page):
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


    def login(self, page: ft.Page):
        page.title = "Login"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.bgcolor = self.primaryC

        title = ft.Text("Login", size=50, font_family="RobotoSlab", weight=ft.FontWeight.W_100, italic=True, color=self.secC)
        loginLabel = self.createLabel("Login", False, False, True)
        passwordLabel = self.createLabel("Password", True, True, False)

        loginButton = self.createButton("Login", lambda e: self.validLogin(loginLabel.value, passwordLabel.value, page))
        signupButton = self.createButton("Signup", lambda e: self.pageSwitch("Signup", None, page))

        theme = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=lambda e: self.colorChange("Login",page))

        elements = [title, loginLabel, passwordLabel, loginButton, signupButton, theme]

        self.sort(elements, ft.MainAxisAlignment.CENTER, page)


    def signup(self, page: ft.Page):
        page.title = "Signup"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.bgcolor = self.primaryC

        title = ft.Text("Signup", size=50, font_family="RobotoSlab", weight=ft.FontWeight.W_100, italic=True, color=self.secC, )
        loginLabel = self.createLabel("Login", False, False, True)
        passwordLabel = self.createLabel("Password", True, True, False)
        passwordConfirmLabel = self.createLabel("Password Confirm", True, True, False)

        signupButton = self.createButton("Signup", lambda e: [self.addCad(loginLabel.value, passwordLabel.value, passwordConfirmLabel.value, page)])
        loginButton = self.createButton("Login", lambda e: [self.pageSwitch("Login", None, page)])

        theme = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=lambda e: self.colorChange("Signup",page))


        elements = [title, loginLabel, passwordLabel, passwordConfirmLabel, signupButton, loginButton, theme]

        self.sort(elements, ft.MainAxisAlignment.CENTER, page)


    def logged(self, ID, page: ft.Page):
        page.title = "Logged"
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.bgcolor = self.primaryC

        title = ft.Text("Options")
        excludeButton = self.createButton("EXCLUDE", self.c.erase(ID))
        editButton = self.createButton("Edit", self.pageSwitch("edit", ID, page))

        theme = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=lambda e: self.colorChange("Logged",page))

        itens = [title, excludeButton, editButton, theme]

        self.sort(itens, ft.MainAxisAlignment.CENTER, page)


    def edit(self, page, id): # CRUDE page...
        pass

        
if __name__ == "__main__":
    ft.app(target=View)
