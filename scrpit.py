from tkinter import *
from tkinter import ttk, filedialog
import mysql.connector
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from docxtpl import DocxTemplate
from home import *
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

def addItem():
    localcursor = mydb.cursor()
    localcursor.execute('SELECT NAME FROM VENDOR')
    values = localcursor.fetchall()
    root = Tk()
    openStk = IntVar()
    openStkDate = StringVar()
    GST = DoubleVar()
    HSN = StringVar()
    o_Price = DoubleVar()
    s_Price = DoubleVar()

    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")

    root.geometry('600x700')
    root.title('Add New Item')
    root.maxsize(width=820, height=300)
    root.minsize(width=820, height=300)

    Label(root,text='Select Item', font=('Times', 18)).grid(row=0, column=0)
    combo = AutocompleteCombobox(root, width=20, font=('Times', 18), completevalues=[ x[0] for x in myresult ])
    combo.grid(row=0 , column=1)

    Label(root,text='Select Vendor', font=('Times', 18)).grid(row=0, column=2)
    Vendor = AutocompleteCombobox(root, width=15, font=('Times', 18), completevalues=[ x[0] for x in values ])
    Vendor.grid(row=0 , column=3)

    ttk.Label(root, text='Opening Stock', font=('Times', 18)).grid(row=1, column= 0,padx=5)
    OS = ttk.Entry(root, font=('Times', 18), textvariable= openStk,width=10)
    OS.grid(row=1, column=1)

    Label(root, text= "Choose a Date", background= 'gray61', foreground="white", font=('Times',18)).grid(row=1,column=2,padx=20,pady=20)
    #Create a Calendar using DateEntry
    cal = DateEntry(root, selectmode='day',width= 20, background= "magenta3", foreground= "white",textvariable = openStkDate)
    cal.grid(row = 1, column = 3)

    Label(root, text='HSN',font=('Times',18),pady=5).grid(row=2,column=0)
    HSNCODE = ttk.Entry(root, font=('Times',18), textvariable= HSN, width=10)
    HSNCODE.grid(row=2, column=1,pady=5)

    Label(root, text='Select GST',font=('Times',18)).grid(row=2,column=2)
    GSTCODE = ttk.Entry(root, font=('Times',18), textvariable= GST, width=10)
    GSTCODE.grid(row=2, column=3)

    Label(root, text='Opening Price',font=('Times',18),pady=5).grid(row=3,column=0)
    OP = ttk.Entry(root, font=('Times',18), textvariable= o_Price, width=10)
    OP.grid(row=3, column=1)

    Label(root, text='Sale Price',font=('Times',18)).grid(row=3,column=2)
    SP = ttk.Entry(root, font=('Times',18), textvariable= s_Price,width=10)
    SP.grid(row=3, column=3)
    
    Label(root, text='Your Profit',font=('Times',18)).grid(row=4,column=0)
    ttk.Label(root, font=('Times',18), width=10).grid(row=4, column=1)
    def hitEnter():
        # Retrieve values from Tkinter variables
        product_name = combo.get()
        vendor_name = Vendor.get()
        opening_stock = int(OS.get())
        opening_stock_dte = cal.get_date().strftime('%Y-%m-%d')  # Convert to a suitable date format
        hsn = HSNCODE.get()
        gst = float(GSTCODE.get())
        o_price = float(OP.get())
        s_price = float(SP.get())
        cgst = gst / 2.0
        sgst = gst / 2.0
        CGST = s_price * cgst / 100
        SGST = s_price * sgst / 100

        # Assuming you have a "products" table with the specified schema
        sql = "INSERT INTO products (NAME, OPEN_STOCK, OPEN_STOCK_DATE, HSN, s_price, PRICE, GST, CGST, SGST, TOTAL, STOCK) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (product_name, opening_stock, opening_stock_dte, hsn, s_price, o_price, gst, CGST, SGST, s_price + (CGST + SGST), opening_stock)

        try:
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo(message="Item added successfully!")
        except Exception as e:
            # mydb.rollback()
            print("Error:", e)
            messagebox.showerror(title="Error", message='Error Code: '+e)

    ttk.Button(root,text='Add Item', command = hitEnter).grid(row=5,column=2)

    root.mainloop()

def editItem():
    localcursor = mydb.cursor()
    localcursor.execute('SELECT NAME FROM VENDOR')
    values = localcursor.fetchall()
    root = Tk()
    openStk = IntVar()
    openStkDate = StringVar()
    GST = DoubleVar()
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")

    root.geometry('600x700')
    root.title('Update Item')
    root.maxsize(width=820, height=300)
    root.minsize(width=820, height=300)

    Label(root,text='Select Item', font=('Times', 18)).grid(row=0, column=0)
    combo = AutocompleteCombobox(root, width=20, font=('Times', 18), completevalues=[ x[0] for x in myresult ])
    combo.grid(row=0 , column=1)

    Label(root,text='Select Vendor', font=('Times', 18)).grid(row=0, column=2)
    Vendor = AutocompleteCombobox(root, width=15, font=('Times', 18), completevalues=[ x[0] for x in values ])
    Vendor.grid(row=0 , column=3)

    ttk.Label(root, text='Opening Stock', font=('Times', 18)).grid(row=1, column= 0,padx=5)
    ttk.Entry(root, font=('Times', 18), textvariable= openStk,width=10).grid(row=1, column=1)

    Label(root, text= "Choose a Date", background= 'gray61', foreground="white", font=('Times',18)).grid(row=1,column=2,padx=20,pady=20)
    #Create a Calendar using DateEntry
    cal = DateEntry(root, selectmode='day',width= 20, background= "magenta3", foreground= "white",textvariable = openStkDate)
    cal.grid(row = 1, column = 3)

    Label(root, text='HSN',font=('Times',18),pady=5).grid(row=2,column=0)
    ttk.Entry(root, font=('Times',18), textvariable= GST, width=10).grid(row=2, column=1,pady=5)

    Label(root, text='Select GST',font=('Times',18)).grid(row=2,column=2)
    ttk.Entry(root, font=('Times',18), textvariable= GST, width=10).grid(row=2, column=3)

    Label(root, text='Opening Price',font=('Times',18),pady=5).grid(row=3,column=0)
    ttk.Entry(root, font=('Times',18), textvariable= GST, width=10).grid(row=3, column=1)

    Label(root, text='Sale Price',font=('Times',18)).grid(row=3,column=2)
    ttk.Entry(root, font=('Times',18), textvariable= GST,width=10).grid(row=3, column=3)
    
    Label(root, text='Your Profit',font=('Times',18)).grid(row=4,column=0)
    ttk.Label(root, font=('Times',18), width=10).grid(row=4, column=1)
    def hitEnter():
        print(combo.get())
        print(cal.get_date())
    ttk.Button(root,text='Update Item', command = hitEnter).grid(row=5,column=2)

    root.mainloop()

def deleteItem():
    root = Tk()
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")

    root.geometry('600x700')
    root.title('Delete Item')
    root.maxsize(width=820, height=200)
    root.minsize(width=820, height=200)

    Label(root,text='Select Item', font=('Times', 18)).grid(row=0, column=0)
    combo = AutocompleteCombobox(root, width=20, font=('Times', 18), completevalues=[ x[0] for x in myresult ])
    combo.grid(row=0 , column=1)

    def hitEnter():
        try:
            flag =  messagebox.askyesno(title='UC - Bhai Sochale EK Bar', message='Kr Du Delete ?')
            print(flag, type(flag), combo.get())
            if (flag):
                mycursor.execute('Delete From Products where NAME = %s',(combo.get(),))
                messagebox.showinfo(title='UC - Item Deleted', message="Status : Kr Diya Bhai !")
                mydb.commit()
            else:
                messagebox.showinfo(title='Unique Computers', message="Ok Bhai Cancel Krdiya !")
        except Exception as e:
            messagebox.showerror(title='Error In Deletting', message=e)
    ttk.Button(root,text='Delete Item', command = hitEnter).grid(row=2,column=2)

    root.mainloop()

def refreshstock(tree):
    try:
        tree.delete(*tree.get_children())
        mycursor.execute('SELECT NAME, PRICE, HSN, GST, CGST, SGST, OPEN_STOCK, OPEN_STOCK_DATE, TOTAL FROM PRODUCTS')
        stkresult = mycursor.fetchall()
        for i in stkresult:
          tree.insert("",0, values=i)
    except Exception as e:
        messagebox.showerror(title='UC',message=e)

def addVendor():
    root = Tk()
    Phone = StringVar()
    vendorName = StringVar()
    city = StringVar()
    Email = StringVar()
    wp = StringVar()
    address = StringVar()

    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")

    root.geometry('600x700')
    root.title('Add New Vendor')
    root.maxsize(width=820, height=300)
    root.minsize(width=820, height=300)

    ttk.Label(root, text='Name', font=('Times', 18)).grid(row=0, column= 0,padx=5)
    ttk.Entry(root, font=('Times', 18), textvariable= vendorName,width=20).grid(row=0, column=1)

    Label(root, text='City',font=('Times',18),pady=5).grid(row=0,column=2)
    ttk.Entry(root, font=('Times',18), textvariable= city, width=10).grid(row=0, column=3,pady=5)

    Label(root, text='Phone',font=('Times',18)).grid(row=1,column=0)
    ttk.Entry(root, font=('Times',18), textvariable= Phone, width=10).grid(row=1, column=1)

    Label(root, text='WhatsApp',font=('Times',18),pady=5).grid(row=1,column=2)
    ttk.Entry(root, font=('Times',18), textvariable= wp, width=10).grid(pady=5,row=1, column=3)

    Label(root, text='Email',font=('Times',18)).grid(row=2,column=1)
    ttk.Entry(root, font=('Times',18), textvariable= Email,width=20).grid(row=2, column=2,pady=5)
    
    Label(root, text='Full Office Add',font=('Times',18)).grid(row=3,column=0)
    ttk.Entry(root, font=('Times',18), textvariable= address,width=20).grid(row=3, column=1)
    def hitEnter():
        sql = "INSERT INTO VENDOR (NAME, CITY, PHONE, WP, EMAIL, ADDRESS) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (vendorName.get(), city.get(), Phone.get(), wp.get(), Email.get(), address.get())
        try:
            mycursor.execute(sql, val)
            mydb.commit()
            print("Record inserted successfully!")
        except Exception as e:
            mydb.rollback()
            print("Error:", e)
            messagebox.showerror(title='Error in Connectivity', message=e)

    ttk.Button(root,text='Add Vendor', command = hitEnter).grid(row=4,column=2)

    root.mainloop()


# addItem()
def fetchName():
    try:
        print("product")
        local_cursor = mydb.cursor()
        local_cursor.execute("select name from custumer")
        values = local_cursor.fetchall()
        print([ x[0] for x in values ])
        return([ x[0] for x in values ])
    except Exception as e:
        messagebox.showerror(title='Unique Computers', message=e)

def afterName(event, name, mob, add,selection):
    actualname = name.get()
    try:
        # print("in try Aftername N", actualname)
        local_cursor = mydb.cursor()
        local_cursor.execute("select phone, city, lastpurchase from custumer where name  = "+"'"+actualname+"'")
        values = local_cursor.fetchall()
        if values:
            row = []
            for tuples in values:
                for items in tuples:
                    row.append(items)
            # return([ x[0] for x in values ])
            mob.set(row[0])
            add.set(row[1])
            selection.focus_set()
            messagebox.showinfo(title="Unique Computers", message="Lastpurchase By "+actualname+" : "+ str(row[2]))
        else:
            # messagebox.showerror(title="Error", message = 'Custumer Not Found')
            answer = messagebox.askyesno(title='Custumer Not Found '+ actualname, message='Do You want to add custumer ?')
            if answer:
                add_customer()
    except Exception as e:
        messagebox.showerror(title='Unique Computers', message= e)

def sendInto(tre, combo, date):
    all_data = []
    for item_id in tre.get_children():
        item_values = tre.item(item_id, "values")
        all_data.append(item_values)
    # print("All Data:", all_data)

    try:
        # print('IN TRY OF U WANT')
        if(combo == '' and len(all_data) == 0):
            messagebox.showerror(title="Unique Computers",message='Select Custumer First !\n Majak Mt Kr Bhai !')
            return
        mycursor.execute("SELECT custid FROM CUSTUMER WHERE NAME = %s", (combo,))
        values = mycursor.fetchone()

        if values:
            customer_id = values[0]
            print('SEE ABOVE |^ custid = ', customer_id)            
            for tuples in all_data:
                mycursor.execute("INSERT INTO PURCHASE (CID, NAME, HSN, QTY, P_DATE, PRICE, TOTAL, TAG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (customer_id, tuples[1], tuples[2], tuples[3], date, tuples[6], tuples[7], tuples[0]))

            insertToSale((customer_id, date))            
            # Commit changes to the database
            mydb.commit()
            tre.delete(*tre.get_children())

        else:
            print("No customer found for name:", combo)
            messagebox.showerror(message="Custumer Not Found !")
    except Exception as e:
        print('Error:', e)
        messagebox.showerror(title='Unique Computers',message='Something Went Wrong')
        # Handle the exception accordingly

def insertToSale(agrs):
    if len(agrs) == 0:
        messagebox.showerror(title='UC - Error', message='No Purchases Found')
        return
    try:
        mycursor.callproc("tosale",agrs)
        messagebox.showinfo(message='Inserted to Sale !')
    except:
        messagebox.showerror(title='Unique Computers', message='Error in Backend')
    

def generate_bill():
    try:
        mycursor.execute('Select * from sale order by no limit 1')
        values  = mycursor.fetchall()
        row = []
        for tuples in values:
            for items in tuples:
                row.append(items)
        print(row)
        mycursor.execute('Select phone, city From custumer where custid = %s', (row[5],))
        result = mycursor.fetchone()
        if result:
            phone, city = result
            row.append(phone)
            row.append(city)
        print(row)
        print("After print row")
        mycursor.execute("select name,tag, hsn,qty,price,total from purchase where cid = %s and P_date = %s", (row[5], row[1]))
        frompurchase  = mycursor.fetchall()
        # invoc = []
        # mycursor.execute()
        for tuples in frompurchase:
            # for items in tuples:
                # invoc.append(items)
            print(tuples)
        gen_invoice(frompurchase, row)
        print("Exit", row)
    except Exception as e:
        messagebox.showerror(title='Error in Bill generation', message=e)

def gen_invoice(items, listItems):
    doc = DocxTemplate("invoice_template.docx")
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",initialfile = listItems[2]+'.docx', filetypes=[("Word documents", "*.docx"), ("All files", "*.*")])
        if file_path:
            doc.render({"name":listItems[2], 
                    "phone":listItems[6],
                    "address": listItems[7],
                    "invoice_list": items,
                    "subtotal":listItems[4],
                    "salestax":"18%",
                    "total":listItems[4],
                    "invoice_date":listItems[1],
                    "invoice_no": listItems[0]})
            doc.save(file_path) 
            messagebox.showinfo(title='Invoice Genrated Successfully', message='Status : Success !')
    except Exception as e:
        messagebox.showerror(title='Error in Renering', message=e)

def addToKart(Name, TAG, HSN, Qty, PRICE, GST):
    tax = (PRICE*GST)/100
    print(tax)
    tax += PRICE
    print(tax)
    try:
        mycursor.execute('INSERT INTO invoice (NAME, QTY, TAG, HSN, PRICE, GST, TOTAL) VALUES (%s, %s, %s, %s, %s, %s, %s)', (Name, Qty, TAG, HSN, PRICE, GST, Qty*tax))
        mydb.commit()
        return True
    except:
        messagebox.showerror(message='Error while Kart Compose !')
        return False

def moveToTemp(row):
    pass