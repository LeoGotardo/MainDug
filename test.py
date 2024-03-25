def inverter_cor_hexadecimal(cor_hex):
    # Remove o símbolo '#' se estiver presente
    cor_hex = cor_hex.strip('#')

    # Converte o hexadecimal para RGB
    r, g, b = int(cor_hex[0:2], 16), int(cor_hex[2:4], 16), int(cor_hex[4:6], 16)

    # Inverte os valores RGB subtraindo de 255
    r_invertido, g_invertido, b_invertido = 255 - r, 255 - g, 255 - b

    # Converte de volta para o formato hexadecimal
    cor_hex_invertida = f"#{r_invertido:02x}{g_invertido:02x}{b_invertido:02x}"

    return cor_hex_invertida

# Vamos testar a função com uma cor de exemplo
cor_exemplo = "#123456"
cor_invertida = inverter_cor_hexadecimal(cor_exemplo)

print(cor_invertida)
