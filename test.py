import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_appearance_mode("green")

root = ctk.CTk()

root.title("Theme")
root.geometry("700x500")

mode = 'dark'

def change():
    global mode
    if mode == "dark":
        ctk.set_appearance_mode('light')
        mode = "light"
    elif mode == "ligth":
        