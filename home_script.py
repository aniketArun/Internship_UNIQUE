import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import filedialog
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="stock"
    )

    mycursor = mydb.cursor()
except mysql.connector.Error as e:
    messagebox.showerror(title="Error", message=e)

def add_customer():
    root = tk.Tk()

    Phone = tk.StringVar()
    CustName = tk.StringVar()
    city = tk.StringVar()

    root.geometry('600x700')
    root.title('Add New Customer')
    root.maxsize(width=820, height=300)
    root.minsize(width=820, height=300)

    ttk.Label(root, text='Name', font=('Times', 18)).grid(row=0, column=0, padx=5, pady=5)
    name = ttk.Entry(root, font=('Times', 18), textvariable=CustName, width=20)
    name.grid(row=0, column=1)

    ttk.Label(root, text='City', font=('Times', 18)).grid(row=0, column=2, pady=5)
    city = ttk.Entry(root, font=('Times', 18), textvariable=city, width=10)
    city.grid(row=0, column=3, pady=5)

    ttk.Label(root, text='Phone', font=('Times', 18)).grid(row=1, column=0)
    Phone = ttk.Entry(root, font=('Times', 18), textvariable=Phone, width=10)
    Phone.grid(row=1, column=1)

    ttk.Button(root, text='Add Customer', command=lambda: hit_enter(name, city, Phone)).grid(row=4, column=2)

    def print_values():
        print("CustName:", name.get())
        print("City:", city.get())
        print("Phone:", Phone.get())

    ttk.Button(root, text='Print Values', command=print_values).grid(row=5, column=2)  # Add a button to print values for debugging

    root.mainloop()


def hit_enter(CustName, city, Phone):
    sql = "INSERT INTO custumer (name, city, phone) VALUES (%s, %s, %s)"
    val = (CustName.get(), city.get(), Phone.get())
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        print("Record inserted successfully!")
        messagebox.showinfo(title='Customer Insertion', message='Status: Success!')
    except mysql.connector.Error as e:
        mydb.rollback()
        print("Error:", e)
        messagebox.showerror(title='Error in Customer Insertion', message=e)
        

def  toExcel(date1, date2, combo):
    try:
        profile = combo.get()
        if profile == 'Unique Computers':
            mycursor.execute('Select * from Sale WHERE P_DATE BETWEEN %s AND %s', (date1, date2))
        else:
            mycursor.execute('Select * from salesbyanvi WHERE P_DATE BETWEEN %s AND %s', (date1, date2))
        rows = mycursor.fetchall()

        # Get the column names
        column_names = [i[0] for i in mycursor.description]

        # Create a Pandas DataFrame from the fetched data
        df = pd.DataFrame(rows, columns=column_names)
        excel_file = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"{date1}.xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )        
        if excel_file:
            # Write the DataFrame to an Excel file
            df.to_excel(excel_file, index=False)
            messagebox.showinfo(title="Report Genreated",message='Status : Success\n Kr Diya Bhai !')
    except Exception as Error:
        print(Error)
        messagebox.showerror(title='UC - Error While Backup', message=Error)

def deleteParty():
    root = Tk()
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")
    try:
        mycursor.execute("select name from custumer")
        values = mycursor.fetchall()
    except Exception as Error:
        messagebox.showerror(title='Error In Deletion', message=Error)
    root.geometry('600x700')
    root.title('Delete Party')
    root.maxsize(width=820, height=200)
    root.minsize(width=820, height=200)

    Label(root,text='Select Party', font=('Times', 18)).grid(row=0, column=0)
    combo = AutocompleteCombobox(root, width=20, font=('Times', 18), completevalues=[ x[0] for x in values ])
    combo.grid(row=0 , column=1)

    def hitEnter():
        try:
            flag =  messagebox.askyesno(title='UC - Bhai Sochale EK Bar', message='Kr Du Delete ?')
            print(flag, type(flag), combo.get())
            if (flag):
                mycursor.execute('Delete From custumer where NAME = %s',(combo.get(),))
                messagebox.showinfo(title='UC - Party Removed ', message="Status : Kr Diya Bhai !")
                mydb.commit()
            else:
                messagebox.showinfo(title='Unique Computers', message="Ok Bhai Cancel Krdiya !")
        except Exception as e:
            messagebox.showerror(title='Error In Deletting', message=e)
    ttk.Button(root,text='Remove', command = hitEnter).grid(row=2,column=2)

    root.mainloop()

def search_records():
    def hit_enter():
        option = search_option.get()
        value = search_entry.get()
        table = 'sale'
        profile_selection = profile.get()
        if profile_selection == "Anvi Enterprises":
            table = 'salesbyanvi'
        try:
        # Execute SQL query based on the selected option
            if option == "No":
                query = f"SELECT * FROM {table} WHERE No = {value}"
            elif option == "Name":
                query = f"SELECT * FROM {table} WHERE NAME LIKE '{value}%'"
            elif option == "Date":
                query = f"SELECT * FROM {table} WHERE P_DATE = '{value}'"
            else:
                messagebox.showerror("Error", "Invalid search option")
                return
            mycursor.execute(query)
        except Exception as Error:
            messagebox.showerror(title='Error - Invalid Options Selected', message='Select all options correctly\n Bhai Thik se Kr !\n Samaza Nahi')
        rows = mycursor.fetchall()
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
    search_option = ttk.Combobox(root,font=("Times", 15),values=["No", "Name", "Date"])
    search_option.set("No")
    search_option.grid(row=0, column=0, pady=10)
    profile = ttk.Combobox(root,font=("Times", 15),values=["Anvi Enterprises", 'Unique Computers'])
    profile.set("Unique Computers")
    profile.grid(row=0, column=1, pady=10)
    # Entry for search value
    search_entry = ttk.Entry(root, font = ('Times', 15))
    search_entry.grid(row=0, column=2, padx=10, pady=10)
    search_entry.bind("<Return>", lambda _ :hit_enter())
    # Button to trigger search
    search_button = ttk.Button(root, text="Search", command=hit_enter)
    search_button.grid(row=0, column=3, padx=10, pady=10)

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
