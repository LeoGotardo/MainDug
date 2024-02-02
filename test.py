import customtkinter as ctk


def imput():
    dialog = ctk.CTkInputDialog(text='What is your name?', title='Hello word!!')

def main():
    app = ctk.CTk()
    app.title('dialog')
    app.geometry('400x400')
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('green')
    frame = ctk.CTkFrame(master=app)
    frame.pack()
    button = ctk.CTkButton(frame,text='Press me', command=lambda:[imput()])

    button.pack()

    app.mainloop()

main()