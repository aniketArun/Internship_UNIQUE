import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def search_records():
    def hit_enter():
        option = search_option.get()
        value = search_entry.get()
        # Execute SQL query based on the selected option
        if option == "No":
            query = f"SELECT * FROM sale WHERE No = {value}"
        elif option == "Name":
            query = f"SELECT * FROM sale WHERE NAME LIKE '{value}%'"
        elif option == "Date":
            query = f"SELECT * FROM sale WHERE P_DATE = '{value}'"
        else:
            messagebox.showerror("Error", "Invalid search option")
            return

        mycursor.execute(query)
        rows = cursor.fetchall()

    # Clear existing rows in Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Insert the fetched data into Treeview
    for row in rows:
        treeview.insert('', 'end', values=row)
    # GUI setup
    root = tk.Tk()
    root.title("Search Records")

    # Search option dropdown
    search_option = ttk.Combobox(root, values=["No", "Name", "Date"])
    search_option.set("No")
    search_option.grid(row=0, column=0, padx=10, pady=10)

    # Entry for search value
    search_entry = ttk.Entry(root)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    # Button to trigger search
    search_button = ttk.Button(root, text="Search", command=search_records)
    search_button.grid(row=0, column=2, padx=10, pady=10)

    # Treeview to display search results
    treeview = ttk.Treeview(root, columns=("No", "P_DATE", "NAME", "Items", "Total", "cid"), show="headings")
    treeview.heading("No", text="No")
    treeview.heading("P_DATE", text="Date")
    treeview.heading("NAME", text="Name")
    treeview.heading("Items", text="Items")
    treeview.heading("Total", text="Total")
    treeview.heading("cid", text="CID")

    treeview.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()
