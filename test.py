import customtkinter as ctk
from tkinter import messagebox as msg

def alert(text):
        # Exibe um alerta na página
        msg.showwarning(title="ERROR",
                     message=text
                    )

app = ctk.CTk()
app.geometry('500x500')

label = ctk.CTkLabel(app, text="CTkLabel", fg_color="transparent")
label.pack()
entry = ctk.CTkEntry(app, placeholder_text="CTkEntry")
entry.pack()
text = ctk.CTkTextbox(app)
text.pack()
button = ctk.CTkButton(app, command=lambda:[alert("nice")])
button.pack()


app.mainloop()