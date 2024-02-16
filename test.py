import customtkinter as ctk

def on_enter_key(event):
    print("Enter key pressed!")

# Create the main window
root = ctk.CTk()

# Set the window size
root.geometry("400x300")

# Bind the "Enter" key to the on_enter_key function
root.bind("<Return>", on_enter_key)

# Run the application
root.mainloop()