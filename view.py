from tkinter import messagebox as msg
from controller import Controller
from PIL import Image as img
from threading import Thread
from CTkColorPicker import *
from icecream import ic
from CTkTable import *

import customtkinter as ctk
import Debug as d
import os


class CustomThread(Thread):
    """
    Initialize CustomThread Object
    
    Args:
        group(object): Thread Group.
        target(callabe): Target Function to call when thread starts.
        name(str): Thread name.
        args(tuple): arguments to pass to the target function
        kwargs(dict): keyword arguments to pass to the target function.
        verbose(bool): Verbosity level.
        
    Returns:
        The return value of the target function if it exists.
    """
    def __init__(self, group=None, target= None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


class View(ctk.CTk):
    def __init__(self):
        os.system("cls")
        ic.configureOutput(prefix=f"{d.Margin}\nDebug | ")

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

        ctk.set_appearance_mode('dark')

        self.mode = 'dark'
        self.login()

        self.app.geometry("500x600")
        self.app.resizable(width=False, height=False)
        self.app.mainloop()


    def selectMode(self, mode):
        self.filterMode = mode


    def unfilter(self, user_id):
        self.findPasswords(user_id)
        self.loggedFrame.destroy()
        self.logged(user_id)


    def filterItens(self, filter, user_id):

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
        if self.passVerifyFunc(password, passwordConfirm):
            try:
                self.editLogFunc("password", user_id, itemId, password)
            except Exception as e:
                msg.showerror(title="Error", message=str(e))


    def passVerifyFunc(self, password, confirm):
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
        if newPar != '':
            if paramter == "Login":
                new = self.c.findUserId(newPar, "$exists")
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
                    sull = self.c.updateUser(user_id, paramter, newPar)
                    self.alert("Info", sull)

                    self.editPasswordFrame.destroy()
                    self.findPasswords(user_id)
                    self.logged(user_id)
        else:
            self.alert('ERROR', f"{paramter} can't be empty.")


    def add(self, user_id):
        newPass = msg.askquestion(title='New Login', message='Do you want to generate a new passwrd?')

        if newPass == 'yes':
            self.loggedFrame.destroy()
            self.generatePass(user_id)
        elif newPass == 'no':
            self.loggedFrame.destroy()
            self.addLog(user_id)


    def addLogDB(self, user_id, site, login, password, frame):
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
            self.passwords = self.c.findPasswords(user_id)
            self.title = ['ID', 'Site', 'Login', 'Password']
            self.passwords.insert(0, self.title)

    def validLogin(self, login, password):
        # Verifica se o login é válido e realiza a ação apropriada
        if login != '' or password != '':
            itens = self.c.isLoginValid(login, password)
            if itens[0] == True:
                self.loginFrame.destroy()
                self.findPasswords(itens[1])

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
        # Adiciona um novo usuário e exibe uma mensagem apropriada
        error = self.c.addUser(login, password, passwordConfirm)
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


    def editLogFunc(self, paramter, user_id, ID, newLog):
        try:
            e = self.c.editLog(user_id, paramter, ID, newLog)
            msg.showinfo(title="Info", message=e)
            return True
        except Exception as e:
            msg.showwarning(title='Error', message=str(e))
            return False


    def copyFunc(self, user_id):
        try:
            dialog = ctk.CTkInputDialog(text="What's the item ID:", title='Copy item credentials...')
            itemID = dialog.get_input()
            copy = self.c.copy(user_id, itemID)
            msg.showinfo(message=copy[1])
        except Exception as e:
            msg.showerror(title="ERROR", message=e)


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
            border_color=self.priColor,
            height=40,
            width=200
        )

        passwordEntry = ctk.CTkEntry(
            master=self.loginFrame,
            placeholder_text="Password",
            font=("RobotoSlab", 12),
            border_width=2,
            border_color=self.priColor,
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
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.see
        )

        loginButton = ctk.CTkButton(
            master=self.loginFrame,
            text="Login",
            command=lambda: [self.validLogin(loginEntry.get(), passwordEntry.get())],
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
        self.loggedFrame = ctk.CTkFrame(master=self.app)
        self.app.title("MainDug")
        self.app.geometry("900x650")
        self.loggedFrame.pack(in_=self.app, anchor="center", fill='both', expand=True)
        self.app.iconbitmap(default="icons/Star.ico")
        self.priColor = self.c.findColor(user_id)
        self.secColor = self.c.darkColor(self.priColor, 50)

        
        modes = ['Filter', 'Site', 'Login']
     
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

if __name__ == "__main__":
    view = View()