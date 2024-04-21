
import tkinter as tk
from tkinter import messagebox

def authenticate(): 
    def validate_login():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        # Replace this with actual authentication logic (check against a database, etc.)
        if entered_username == "user1" and entered_password == "password123":
            messagebox.showinfo("Login Successful", "Welcome, " + entered_username + "!")
            root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Create the main window
    root = tk.Tk()
    root.title("Login - Sales Invoice Manager")
    root.geometry('400x200')
    # Create and place widgets in the window
    un = tk.Label(root, text="Username:").place(x=50, y = 10)

    username_entry = tk.Entry(root)
    username_entry.place(x=200, y = 10)

    tk.Label(root, text="Password:").place(x=50, y = 30)
    password_entry = tk.Entry(root, show="*")
    password_entry.place(x=200, y = 30)

    login_button = tk.Button(root, text="Login", command=validate_login)
    login_button.place(x=70 , y=70)

    login_button = tk.Button(root, text="Register", command=validate_login)
    login_button.place(x=150 , y=70)
    # Start the GUI event loop
    root.mainloop()

