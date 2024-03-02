from passgenerator import Generator
from tkinter import messagebox as msg
from controller import Controller
from PIL import Image as img
from CTkTable import *
import customtkinter as ctk
import Debug as d


class View(ctk.CTk):
    def __init__(self):
        self.c = Controller()
        self.app = ctk.CTk()
        self.g = Generator()

        self.app.geometry("500x600")
        self.see = ctk.CTkImage(dark_image=img.open("icons/see.ico"))
        self.unsee = ctk.CTkImage(dark_image=img.open("icons/unsee.ico"))
        self.white = ctk.CTkImage(dark_image=img.open("icons/White.ico"))
        self.dark = ctk.CTkImage(dark_image=img.open("icons/Dark.ico"))
        self.exit = ctk.CTkImage(dark_image=img.open("icons/Exit.ico"))
        self.Config = ctk.CTkImage(dark_image=img.open("icons/Config.ico"))
        self.Add = ctk.CTkImage(dark_image=img.open("icons/add.ico"))
        self.Delete = ctk.CTkImage(dark_image=img.open("icons/delete.ico"))
        self.edit = ctk.CTkImage(dark_image=img.open("icons/edit.ico"))
        ctk.set_default_color_theme('green')
        self.mode = 'dark'
        self.login()

        self.app.mainloop()


    def fullGeneratePass(self, len, upper, lower, symbol, number):
        try:
            len = int(len)
        except:
            print('Password Length must be a integer number.')

        resp = [number,lower,symbol,upper,len]
        print(resp)
        password = self.g.generator(resp)

        print(password)

    def deleteItem(self, id):
        dialog = ctk.CTkInputDialog(title="Delete Iten", text="What's the iten ID that you want to delete?")
        item_id = dialog.get_input()
        try:
            item_id = int(item_id)
            deleted = self.c.delete_item(id, item_id)
            msg.showinfo(title='Info', message=deleted)
            self.loggedFrame.destroy()
            self.logged(id)
        except:
            msg.showerror(title="Error", message="ID must be a number.")
            dialog

    
    def editCred(self, id, paramter, newPar):
        if paramter == "Login":
            new = self.c.find_user_id(newPar, "$exists")
            if new == []:
                sull = self.c.update_user(id, paramter, newPar)
                self.alert("Info", sull)

                self.editLoginFrame.destroy()
                self.logged(id)
            else:
                self.alert("ERROR",f'This login alredy exists.')
        elif paramter == "Password":
            sull = self.c.update_user(id, paramter, newPar)
            self.alert("Info", sull)

            self.editPasswordFrame.destroy()
            self.logged(id)


    def add(self, id):
        newPass = msg.askquestion(title='New Login', message='Do you want to generate a new passwrd?')

        if newPass == 'yes':
            self.loggedFrame.destroy()
            self.generatePass(id)
        elif newPass == 'no':
            self.loggedFrame.destroy()
            self.addLog(id)

    def addLogDB(self, id, site, login, password):
        ret = self.c.addNewLog(id, site, login, password)
        msg.showinfo(title="Info", message=ret)

        self.addLogFrame.destroy()
        self.addLog(id)


    def delete(self, id):
        response = msg.askquestion(title="Delete Account",
                               message="Are you sure you want to delete this account? This action cannot be undone.",
                               icon="warning")  # Use askquestion for a clear yes/no choice
        if response == "yes":
            try:
                # Perform account deletion logic here
                self.c.delete_user(id)
                print(f"{d.Margin}Account {id} deleted successfully.{d.Margin}")
                msg.showinfo('Done',f'Account {id} sucessfull deleted.')
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
            itens = self.c.is_login_valid(login, password)
            print(f"{d.Margin}Itens:{itens}\nLogin:{login}\nPassword:{password}{d.Margin}")
            if itens[0] == True:
                self.loginFrame.destroy()

                self.logged(itens[1])
            elif itens[0] == False:
                self.alert("ERROR",itens[1])
                self.loginFrame.destroy()
                self.login()
        else:
            self.alert("ERROR", "Login or Password can't be empty")
            self.loginFrame.destroy()
            self.login()


    def addCad(self, login, password, passwordConfirm):
        print(f"{d.Margin}Login:{login} \nPassword:{password}\nPasswordConfirm:{passwordConfirm}{d.Margin}")
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.add_user(login, password, passwordConfirm)
        print(f"{d.Margin}error = {error}{d.Margin}")
        if error == True:
            self.alert("Susses","Sussesfull Signup")
            self.signupFrame.destroy()
            self.login()
        else:
            self.alert("ERROR",error)
            self.signupFrame.destroy()
            self.signup()

    
    def seePass(self, entry, button):
        if entry.cget('show') == "*":
            entry.configure(show="")
            button.configure(image=self.unsee)
        elif entry.cget('show') == "":
            entry.configure(show="*")
            button.configure(image=self.see)


    def theme(self, button):
        if self.mode == 'dark':
            ctk.set_appearance_mode('light')
            button.configure(image=self.dark)
            self.mode = 'light'
        else:
            ctk.set_appearance_mode('dark')
            button.configure(image=self.white)
            self.mode = 'dark'


    def alert(self, title, text):
        # Exibe um alerta na página
        msg.showwarning(title=title,message=text)


    def login(self):
        # Configura a página de login
        self.loginFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Login")
        self.loginFrame.place(in_=self.app, anchor="center", relx=0.5, rely=0.5)
        self.app.iconbitmap(default="icons/Alien.ico")
        


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
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showPass.place(relx=0.85, rely=0.39)
        loginButton.pack(padx=50, pady=10)
        signupButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.validLogin(loginEntry.get(), passwordEntry.get()))


    def signup(self):
        # Configura a página de cadastro
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
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        loginEntry.pack(padx=50, pady=10)
        passwordEntry.pack(padx=50, pady=10)
        showpass.place(relx=0.85, rely=0.332)
        passwordConfirmEntry.pack(padx=50, pady=10)
        showPassConfirm.place(relx=0.85, rely=0.48)
        signupButton.pack(padx=50, pady=10)
        loginButton.pack(padx=50, pady=10)
        theme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.addCad(loginEntry.get(), passwordEntry.get(), passwordConfirmEntry.get()))


    def logged(self, id):
        self.loggedFrame = ctk.CTkFrame(master=self.app)
        self.app.title("MainDug")
        self.app.geometry("900x600")
        self.loggedFrame.pack(in_=self.app, anchor="center", fill='both', expand=True)
        self.app.iconbitmap(default="icons/Star.ico")

        self.passwords = self.c.findPasswords(id)

        print(f"{d.Margin}passwords:{self.passwords}{d.Margin}")

        title = ctk.CTkLabel(
            master=self.loggedFrame, 
            text="Menu",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )
        tableFixFrame = ctk.CTkScrollableFrame(master=self.loggedFrame,width=800,height=400)
        tableFrame = ctk.CTkFrame(master=tableFixFrame, height=2000)

        table = CTkTable(
            master=tableFrame,
            row=len(self.passwords),
            column=4,
            values=self.passwords,
            width=200,
            colors=['#174a19','#292b29']
        )

        exitButton = ctk.CTkButton(
            master=self.loggedFrame,
            command=lambda: [self.loggedFrame.destroy(), self.login()],
            text="",
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.exit
        )

        configButton = ctk.CTkButton(
            master=self.loggedFrame,
            command=lambda: [self.loggedFrame.destroy(), self.config(id)],
            text="",
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image= self.Config
        )

        theme = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.white
        )

        add = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.add(id)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.Add
        )

        delete = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.deleteItem(id)],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.Delete
        )

        edit = ctk.CTkButton(
            master=self.loggedFrame,
            text="",
            command=lambda:[self.edit()],
            font=("RobotoSlab", 12),
            corner_radius=50,
            height=10,
            width=10,
            image=self.edit
        )

        configButton.place(relx=0.05, rely=0.05,anchor="center")
        title.place(relx=0.5, rely=0.1, anchor="center")

        tableFixFrame.place(relx=0.5, rely=0.5, anchor="center")
        tableFrame.pack(fill='both', expand=True)
        table.place(in_=tableFrame)

        edit.place(relx=0.3,rely=0.9, anchor="center")
        add.place(relx=0.4,rely=0.9, anchor="center")
        exitButton.place(relx=0.5, rely=0.9, anchor="center")
        theme.place(relx=0.6, rely=0.9, anchor="center")
        delete.place(relx=0.7,rely=0.9, anchor="center")


    def config(self, id):
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
            command=lambda: [self.configFrame.destroy(), self.editLogin(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        passEditButton = ctk.CTkButton(
            master=self.configFrame,
            text="Edit Password",
            command=lambda: [self.configFrame.destroy(), self.editPass(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        eraseButton = ctk.CTkButton(
            master=self.configFrame,
            text="Erase Account",
            command=lambda: [self.configFrame.destroy(), self.erase(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )
        
        backButton = ctk.CTkButton(
            master=self.configFrame,
            text="Back",
            command=lambda:[self.configFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
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
            image=self.white
        )


        title.pack(padx=50, pady=10)
        loginEditButton.pack(padx=50, pady=10)
        passEditButton.pack(padx=50, pady=10)
        eraseButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)


    def editLogin(self, id):
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
            border_width=2,
            height=40,
            width=200
        )

        loginEditButton = ctk.CTkButton(
            master=self.editLoginFrame,
            text="Edit Login",
            command=lambda:[self.editCred(id, "Login", loginEntry.get())],
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
            command=lambda:[self.theme(changeTheme)],
            font=("RobotoSlab", 12),
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

        self.app.bind("<Return>", lambda _: self.editCred(id, "Login", loginEntry.get()))


    def editPass(self, id):
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
            command=lambda: [self.editCred(id, "Password", passwordEntry.get())],
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
            command=lambda:[self.theme(theme)],
            font=("RobotoSlab", 12),
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
        self.app.iconbitmap(default="icons/Skull.ico")


        title = ctk.CTkLabel(
            master=self.eraseFrame, 
            text="Delete Account",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )

        eraseButton = ctk.CTkButton(
            master=self.eraseFrame,
            text="DELETE ACCOUNT",
            command=lambda: [self.delete(id)],
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
            command=lambda: [self.eraseFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
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
            width=10,
            image=self.white
        )

        title.pack(padx=50, pady=10)
        eraseButton.pack(padx=50, pady=10)
        backButton.pack(padx=50, pady=10)
        changeTheme.pack(padx=50, pady=10)

        self.app.bind("<Return>", lambda _: self.delete(id))

    def generatePass(self, id):
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
            border_width=2,
            height=40,
            width=200
                               )

        numberValue = ctk.StringVar(value="on")
        number = ctk.CTkCheckBox(self.generatePassFrame, text="Lower Case Letters",
                                     variable=numberValue, onvalue="on", offvalue="off")

        lowerLetterValue = ctk.StringVar(value="on")
        lowerLetter = ctk.CTkCheckBox(self.generatePassFrame, text="Lower Case Letters",
                                     variable=lowerLetterValue, onvalue="on", offvalue="off")

        upperLetterValue = ctk.StringVar(value="on")
        upperLetter = ctk.CTkCheckBox(self.generatePassFrame, text="Upper Case Letters",
                                     variable=upperLetterValue, onvalue="on", offvalue="off")

        symbolValue = ctk.StringVar(value="on")
        symbol = ctk.CTkCheckBox(self.generatePassFrame, text="Symbols",
                                     variable=symbolValue, onvalue="on", offvalue="off")
        
        confirmButton = ctk.CTkButton(
            master=self.generatePassFrame,
            text="Next",
            command=lambda: [self.fullGeneratePass(passLen.get(), upperLetterValue.get(), lowerLetterValue.get(), symbol.get(), numberValue.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        cancelButton = ctk.CTkButton(
            master=self.generatePassFrame,
            text="Cancel",
            command=lambda: [self.generatePassFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        title.pack(padx=50, pady=30)
        passLen.pack(padx=50, pady=10)
        number.pack(padx=50, pady=10)
        lowerLetter.pack(padx=50, pady=10)
        upperLetter.pack(padx=50, pady=10)
        confirmButton.pack(padx=50, pady=10)
        cancelButton.pack(padx=50, pady=10)


    def addLog(self, id):
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
            border_width=2,
            height=40,
            width=200
        )

        loginEntry = ctk.CTkEntry(
            master=self.addLogFrame,
            placeholder_text="Login",
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.addLogFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
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
            height=10,
            width=10,
            image=self.see
        )

        doneButton = ctk.CTkButton(
            master=self.addLogFrame,
            text="Done",
            command=lambda: [self.addLogDB(id, siteEntry.get(), loginEntry.get(), passwordEntry.get())],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        cancelButton = ctk.CTkButton(
            master=self.addLogFrame,
            text="Cancel",
            command=lambda: [self.addLogFrame.destroy(), self.logged(id)],
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )

        changeTheme = ctk.CTkButton(
            master=self.addLogFrame,
            text="",
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
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

        self.app.bind("<Return>", lambda _: self.addLogDB(id, siteEntry.get(), loginEntry.get(), passwordEntry.get()))

if __name__ == "__main__":
    view = View()