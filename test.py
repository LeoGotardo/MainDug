import customtkinter as ctk
from PIL import Image as img


app = ctk.CTk()
icon = ctk.CTkImage(dark_image=img.open("./icons/amazon.svg"))

app.geometry('500x500')
app.title('test')

button = ctk.CTkButton(
    master=app,
    text='',
    image=icon     
)

app.mainloop()