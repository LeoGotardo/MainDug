import string

# Printable ASCII symbols
printable_ascii_symbols = list(string.ascii_letters + string.digits + string.punctuation)

# If you also want to include non-printable control characters (0-31 and 127 in ASCII)
# These are not directly accessible via the string module but can be added manually
control_chars = [chr(i) for i in range(32)] + [chr(127)]

# Complete ASCII symbols list including control characters
ascii_symbols = control_chars + printable_ascii_symbols

# Displaying the printable ASCII symbols list
print(printable_ascii_symbols)

# Uncomment the line below if you wish to see the complete ASCII symbols list
# print(ascii_symbols)
