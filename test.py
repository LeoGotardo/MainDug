import customtkinter

app = customtkinter.CTk()
app.geometry('500x500')

label = customtkinter.CTkLabel(app, text="CTkLabel", fg_color="transparent")
label.pack()
entry = customtkinter.CTkEntry(app, placeholder_text="CTkEntry")
entry.pack()

app.mainloop()