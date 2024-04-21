from home_script import *
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from tkinter import messagebox
import mysql.connector
from tkinter import PhotoImage
from ttkwidgets.autocomplete import AutocompleteCombobox
from docxtpl import DocxTemplate
from tkinter import filedialog
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database = "stock"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT name FROM products")
    myresult = mycursor.fetchall()
except Exception as error:
    messagebox.showerror(title='Error In DB Connection', message=error)


def createwindo(tab):
    mycursor.execute("select name from custumer")
    values = mycursor.fetchall()
    # print([x[0] for x in values])
    name = AutocompleteCombobox(
    tab, 
    width=25, 
    font=('Times', 15),
    completevalues= [ x[0] for x in values ]
    )
    # name.place(x=10, y=10)
    name.grid(row=0, column=1)

    product = AutocompleteCombobox(
    tab, 
    width=25, 
    font=('Times', 15),
    completevalues= [ x[0] for x in myresult ]
    )
    # product.place(x=10, y = 60)
    product.grid(row=1, column=1)

    price = DoubleVar()
    qty = DoubleVar()
    phone = StringVar()
    city = StringVar()
    now = datetime.now()
    # dd/mm/YY H:M:S
    global samay
    samay = now.strftime("%Y%m%d")
    # Label(tab, text='Price', font=('Times', 15)).place(x=10, y=120)
    Label(tab, text='Price', font=('Times', 15)).grid(row=2, column=0, pady = 10)
    kimat = Entry(tab, textvariable= price, font=('Times', 15))
    # kimat.place(x=90, y=120)
    kimat.grid(row=2, column = 1, pady=10)

    # Label(tab, text='Phone', font=('Times', 15)).place(x=10, y=160)
    Label(tab, text='Phone', font=('Times', 15)).grid(row=3, column=0, pady = 10)
    number = Entry(tab, textvariable= phone, font=('Times', 15))
    # number.place(x = 90, y = 160)
    number.grid(row=3, column=1, pady = 10)

    # Label(tab, text='Quantity', font=('Times', 15)).place(x=10, y=200)
    Label(tab, text='Quantity', font=('Times', 15)).grid(row=4, column=0, pady = 10)
    sankhya = Entry(tab, textvariable= qty, font=('Times', 15))
    # sankhya.place(x = 90, y = 200)
    sankhya.grid(row=4, column=1, pady = 10)

    # Label(tab, text='City', font=('Times', 15)).place(x=10, y=240)
    Label(tab, text='City', font=('Times', 15)).grid(row=5, column=0, pady = 10)
    number = Entry(tab, textvariable= city, font=('Times', 15))
    # number.place(x = 90, y = 240)
    number.grid(row=5, column=1, pady = 10)

    columns = ["name", "qty", "price", "total"]

    # Create a Treeview widget
    treeview = ttk.Treeview(tab, columns=columns, show='headings')

    # Configure column headings
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100, anchor=tk.CENTER)  # Adjust width as needed

    # Pack the Treeview into the window
    treeview.grid(row=0, column=3, padx = 10)

    columns1 = ["No", "Name", "Date", "Total"]

    # Create a Treeview widget
    treeview1 = ttk.Treeview(tab, columns=columns1, show='headings')

    # Configure column headings
    for col in columns1:
        treeview1.heading(col, text=col)
        treeview1.column(col, width=100, anchor=tk.CENTER)  # Adjust width as needed
    try:
        sales  = recorsFromAnvi()
        for i in sales:
          treeview1.insert("",0, values=i)
    except Exception as e:
        messagebox.showerror(title='Anvi - Records Display Error',message=e)
    # Pack the Treeview into the window
    treeview1.grid(row=0, column=4)
  
    # Button(tab, text='Add', font=('Times', 15), command=lambda:add(product, price, qty, treeview)).place(x=10, y=280)
    # Button(tab, text='Render Bill', font=('Times', 15), command=lambda: printtake(treeview, name)).place(x=90, y=280)
    # Button(tab, text='Clear', command= lambda: treeview.delete(*treeview.get_children()) , font= ('Times', 15)).place(x=10, y=320)
    # Button(tab, text='save', command= lambda: renderBill(name.get(), samay, phone.get(),city.get()) , font= ('Times', 15)).place(x=100, y=320)
    Button(tab, text='Add', font=('Times', 15), command=lambda:add(product, price, qty, treeview)).grid(row=7, column=0, pady = 10)
    Button(tab, text='Render Bill', font=('Times', 15), command=lambda: printtake(treeview, name)).grid(row=7,column=1, pady = 10)
    Button(tab, text='Clear', command= lambda: treeview.delete(*treeview.get_children()) , font= ('Times', 15)).grid(row=8, column=0, pady = 10)
    Button(tab, text='save', command= lambda: renderBill(name.get(), samay, phone.get(),city.get()) , font= ('Times', 15)).grid(row=8, column=1, pady = 10)

def recorsFromAnvi():
    mycursor.execute('Select * from salesbyanvi')
    return mycursor.fetchall()

def add(product, price, qty, tree):
    if len(product.get()) == 0 or qty.get() == 0 or price.get() == 0:
        messagebox.showwarning(title='Bhai Ye Mat Krr !', message='Confidential H !\n Don\'t Play With Software !')
        return
    row = [product.get(), qty.get(), price.get(), qty.get()*price.get()]
    tree.insert("",0, values=tuple(row))

def printtake(tre, combo):
    all_data = []
    for item_id in tre.get_children():
        item_values = tre.item(item_id, "values")
        all_data.append(item_values)
    print("All Data:", all_data)
    if(len(all_data) == 0 and combo.get() == ''):
        messagebox.showwarning(title='Bhai Kya kr Rha h', message='Stop Kidding')
        return 

    try:
        print('IN TRY OF U WANT')
        now = datetime.now()
        # dd/mm/YY H:M:S
        global samy
        samay = now.strftime("%Y%m%d")
        if(combo == ''):
            messagebox.showerror(title="Unique Computers",message='Select Custumer Fisrt !')
            return
        for buckets in all_data:
            mycursor.execute('Insert into byanvi (name, qty, price, total,P_date, admi) values(%s, %s, %s, %s, %s, %s)', (buckets[0],buckets[1],buckets[2],buckets[3],samay, combo.get()))
        
        mydb.commit()

    except Exception as e:
        mydb.rollback()
        messagebox.showerror(title='Anvi EnterPrises', message=e)


def renderBill(name, date, phone, city):
    try:
        if name == '':
            messagebox.showwarning(message='No Custumer Selected')
            return
        print('Here !')
        
        mycursor.execute("select name, qty, price, total from byanvi where admi = %s and P_date = %s", (name, date))
        invoice_list = mycursor.fetchall()
        
        mycursor.execute('select sum(total) from byanvi where admi = %s and P_date = %s',(name, date))
        total = mycursor.fetchone()
        mycursor.execute('insert into salesByanvi (name, total, P_date) values (%s, %s, %s)', (name, total[0], date))
        mycursor.execute('select No from salesByanvi where name = %s and P_date = %s',(name, date))
        listItem = mycursor.fetchone()
        mydb.commit()
        doc = DocxTemplate("anvi_invoice_template.docx")
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".docx",initialfile = name + '.docx', filetypes=[("Word documents", "*.docx"), ("All files", "*.*")])
            if file_path:
                doc.render({"name":name, 
                        "phone":phone,
                        "address": city,
                        "invoice_list": invoice_list,
                        "subtotal":total[0],
                        "invoice_no": listItem[0],
                        "salestax":"18%",
                        "total":total[0],
                        "invoice_date":date,
                        })
                doc.save(file_path) 
                messagebox.showinfo(title='Invoice Genrated Successfully', message='Status : Success !')
        except Exception as e:
            messagebox.showerror(title='Anvi - Error in Renering', message=e)
    except Exception as e:
        print(e)
        messagebox.showerror(title='Anvi - Error in Bill Rendering', message= e)
