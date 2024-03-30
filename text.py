import customtkinter as ctk
from CTkColorPicker import *

def generate_gradient(hex_color_start, hex_color_end, steps):
    """
    Gera um gradiente entre duas cores hexadecimais.

    :param hex_color_start: A cor inicial do gradiente em hexadecimal.
    :param hex_color_end: A cor final do gradiente em hexadecimal.
    :param steps: O número de cores no gradiente.
    :return: Uma lista de cores hexadecimais representando o gradiente.
    """

    # Função auxiliar para converter hex para RGB
    def hex_to_rgb(hex_color):
        return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    
    # Função auxiliar para converter RGB para hex
    def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    # Converte as cores de início e fim para RGB
    start_r, start_g, start_b = hex_to_rgb(hex_color_start)
    end_r, end_g, end_b = hex_to_rgb(hex_color_end)

    # Lista para armazenar o gradiente
    gradient = []

    # Gera o gradiente
    for step in range(steps):
        # Calcula a interpolação linear para cada componente
        r = round(start_r + (end_r - start_r) * step / (steps - 1))
        g = round(start_g + (end_g - start_g) * step / (steps - 1))
        b = round(start_b + (end_b - start_b) * step / (steps - 1))
        
        # Converte para hexadecimal e adiciona à lista do gradiente
        gradient.append(rgb_to_hex(r, g, b))
    
    return gradient


app = ctk.CTk()
app.geometry('500x500')
color = "#000000"

button = ctk.CTkButton(
    master=app,
    bg_color=color,
    text='rgb on',
    command=lambda:print(generate_gradient("#FF5733", "#33FF57", 10))
)

button.pack()

app.mainloop()

