import customtkinter
import time

def start():
    progress.start()

app = customtkinter.CTk()
app.geometry('500x500')

progress = customtkinter.CTkProgressBar(app,orientation='horizontal')
progress.pack(padx=40, pady=40)
progress.set(0)
button = customtkinter.CTkButton(app, text="click me", command=lambda: start())
button.pack()
app.mainloop()



