from scrpit import *
import tkinter as tk	
from datetime import datetime
from tkinter import messagebox
from home import *
from authentication import *

authenticate()

def is_record_present(new_age):
    for item_id in tv.get_children():
        item_age = tv.item(item_id, "values")[1]  # Index 1 corresponds to the second column (Age)
        if str(item_age) == str(new_age):
            return True
    return False

def addProduct():
    if(quantity.get() == 0):
        messagebox.showerror(message="Invalid Quantity : " + str(quantity.get()))
        return
    query = "SELECT TOTAL, STOCK FROM PRODUCTS WHERE NAME ='"+ combo.get()+"'"
    mycursor.execute(query)
    stk = mycursor.fetchall()
    if len(stk) <= 0:
            messagebox.showerror(message= "No Item Found Like " + combo.get())
            return
    STOCK = int(stk[0][1])
    if((STOCK == 0) or ((STOCK + 1) < quantity.get())):
        messagebox.showerror(message=combo.get()+" OUT OF Stock !")
    else:
        # ('no', 'Product', 'HSN CODE', 'QTY','CGST','SGST','PRICE', 'TOTAL')
        global  SALE_PRICE
        CGST = SALE_PRICE.get()*9/100
        amt = 2*CGST + SALE_PRICE.get()
        print(CGST,"\n",amt)
        row = []
        query = "SELECT HSN FROM PRODUCTS WHERE NAME ='"+ combo.get()+"'"
        mycursor.execute(query)
        record = mycursor.fetchall()
        for i in record:
            for j in i:
                row.append(j)
        if(len(DESC.get()) > 1):     
            row.insert(0,DESC.get())
        else:
            row.insert(0,'UC-S/N')        
        row.insert(1,combo.get())
        row.insert(3,quantity.get())
        row.insert(4,CGST)
        row.insert(5,CGST)
        row.insert(6, SALE_PRICE.get())
        row.insert(8, amt*quantity.get())
        print(row)
        if not is_record_present(combo.get()):
            # global combo, qtyEntry, salePrice, taxEntry, txbl
            # if addToKart(combo.get(),txbl.get(),row[2],quantity.get(),SALE_PRICE.get(), Tax.get()) == 1:
                # messagebox.showinfo(message=combo.get()+"added to KART !")
            tv.insert("",0, values=tuple(row))
                # moveToTemp(row)
            sort() 
                # updateValues(CGST, SALE_PRICE.get(), amt)
            SALE_PRICE.set(0)
        else:
            messagebox.showerror(message="Item is already present")

def sort():
    rows = [(tv.item(item, 'values'), item) for item in tv.get_children('')]
    # if you want to sort according to a single column:
    # rows = [(tree.set(item, column), item) for item in tree.get_children('')]
    rows.sort()

    # rearrange items in sorted positions
    for index, (values, item) in enumerate(rows):
        tv.move(item, '', index)


def delete():
    try:
        # Get selected item to Delete
        selected_item = tv.selection()[0]
        product = tv.item(selected_item, 'values')[1]
        # Delete from Treeview
        tv.delete(selected_item)

        # Delete from Database
        print(f"Deleting from database: {product}")
        
        mycursor.execute('DELETE FROM INVOICE WHERE NAME = %s', (product,))
        mydb.commit()

    except Exception as e:
        mydb.rollback()
        messagebox.showerror(title='UC', message='Select Item First')
        print(f"Error: {e}")

# mycursor = mydb.cursor()
mycursor.execute("SELECT name FROM products")
myresult = mycursor.fetchall()
STOCKCURSOR = mydb.cursor()
STOCKCURSOR.execute('SELECT NAME, PRICE, HSN, GST, CGST, SGST, OPEN_STOCK, OPEN_STOCK_DATE, TOTAL FROM PRODUCTS')
stkresult = STOCKCURSOR.fetchall()
root = tk.Tk() 
root.title("Unique Computers")

height = root.winfo_screenheight()
width = root.winfo_screenwidth()
# root.attributes('-fullscreen',True)
root.geometry("%dx%d" %(width,height))


tabControl = ttk.Notebook(root) 

tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl) 
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)

homeWindow(tab3, root, tabControl)
createwindo(tab4)
# dynamicTab(tab3, tabControl)
# bill = tk.Text(tab1)

tv = ttk.Treeview(tab1,height = 30)
tv['columns']=('TAG', 'Product', 'HSN CODE', 'QTY','CGST','SGST','PRICE', 'TOTAL')
tv.column('#0', width=0, stretch=NO)
tv.column('TAG', anchor=CENTER, width=100)
tv.column('Product', anchor=CENTER, width=100)
tv.column('HSN CODE', anchor=CENTER, width=100)
tv.column('QTY', anchor=CENTER, width=100)
tv.column('CGST', anchor=CENTER, width=100)
tv.column('SGST', anchor=CENTER, width=100)
tv.column('PRICE', anchor=CENTER, width=100)
tv.column('TOTAL', anchor=CENTER, width=100)


tv.heading('#0', text='', anchor=CENTER)
tv.heading('TAG', text='TAG', anchor=CENTER)
tv.heading('Product', text='Product', anchor=CENTER)
tv.heading('HSN CODE', text='HSN CODE', anchor=CENTER)
tv.heading('CGST', text='CGST', anchor=CENTER)
tv.heading('SGST', text='SGST', anchor=CENTER)
tv.heading('QTY', text='QTY', anchor=CENTER)
tv.heading('PRICE', text='PRICE', anchor=CENTER)
tv.heading('TOTAL', text='TOTAL', anchor=CENTER)

style=ttk.Style()
style.theme_use('classic')
style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")

# Create a vertical scrollbar
verscrlbar = ttk.Scrollbar(tab1,
                           orient ="vertical", 
                           command = tv.yview)

verscrlbarTAB2 = ttk.Scrollbar(tab2,
                           orient ="vertical", 
                           command = tv.yview) 
# Configuring treeview
tv.configure(yscrollcommand = verscrlbar.set)
verscrlbar.pack(side ='right', fill =BOTH)

tv.pack(anchor= "e")

try:
    global close_image, enter_Image, bill_Image, add_Image, remove_Image, qty_Image, phone_Image, city_Image, name_Image, price_Image, product_Image
    close_image = PhotoImage(file='close.png').subsample(15,15)
    enter_Image = PhotoImage(file='done.png').subsample(15,15)
    bill_Image = PhotoImage(file='gen_bill.png').subsample(28,28)
    add_Image = PhotoImage(file='add_kart.png').subsample(10,10)
    remove_Image = PhotoImage(file='remove.png').subsample(20,20)
    qty_Image = PhotoImage(file='quantity.png').subsample(13,13)
    phone_Image = PhotoImage(file='phone.png').subsample(13,13)
    city_Image = PhotoImage(file='city.png').subsample(40,40)
    name_Image = PhotoImage(file='name.png').subsample(18,18)
    price_Image = PhotoImage(file='price.png').subsample(10,10)
    product_Image = PhotoImage(file='new_product.png').subsample(14,14)

except Exception as e:
    messagebox.showerror(title='Error in Icon Placement',message=e)

item = 1
MOB = StringVar()
NAME = StringVar()
ADD = StringVar()
prdt = StringVar()
quantity = IntVar()
SALE_PRICE = DoubleVar()
DESC = StringVar()
Tax = DoubleVar()
# datetime object containing current date and time
now = datetime.now()
 
# dd/mm/YY H:M:S
datetime = now.strftime("%d/%m/%Y %H:%M:%S")

Label(tab1,text='Mob No',anchor='w',font = ('Times',15),image=phone_Image, compound='right').place(x = 10, y = 10)
mob= ttk.Entry(tab1, textvariable= MOB,font = ('Times',15),width=20).place(x = 110, y = 10)

Label(tab1,text='Date-Time', anchor='w',font = ('Times',15)).place(x=10, y= 150)
Label(tab1, text=datetime, anchor='w',font = ('Times',15)).place(x = 130, y = 150)
Label(tab1,text='GST INCLUDED',anchor='w',font = ('Times',15)).place(x=310, y=150)
# name = ttk.Entry(tab1, textvariable=NAME).place(x = 80, y=50)
name = AutocompleteCombobox(
    tab1, 
    width=20, 
    font=('Times', 15),
    completevalues=fetchName()
    )
name.place(x = 110, y=60)
name.bind("<Return>", lambda event: afterName(event, name,MOB,ADD, combo))
name.bind("<<ComboboxSelected>>", lambda event: afterName(event, name, MOB, ADD, combo))

Label(tab1, text='Name',anchor='w', font = ("Times",15), image=name_Image, compound='right').place(x = 10, y=60)

Label(tab1,text='City',anchor='w',font = ('Times',15), image=city_Image, compound='left').place(x=10, y = 100)
ttk.Entry(tab1,textvariable=ADD,font = ("Times",15),width=20).place(x=110, y=100)

Label(tab1,text='Add Product',anchor='w',font = ('Times',15), image=product_Image, compound='left').place(x=10, y=250)
combo = AutocompleteCombobox(
    tab1, 
    width=25, 
    font=('Times', 15),
    completevalues=[ x[0] for x in myresult ]
    )
combo.place(x=170, y=250)
Label(tab1,text='Select Qty',anchor='w',font = ('Times',15), image= qty_Image, compound='left').place(x=10, y = 290)
qtyEntry = ttk.Entry(tab1, textvariable= quantity, font = ('Times',15),width = 10)
qtyEntry.place(x=170, y=290)
taxEntry = ttk.Entry(tab1, width= 7, textvariable= Tax, font=('Times', 15))
taxEntry.place(x=290, y=290)
Label(tab1,text='Sale Price',font = ('Times',15), image=price_Image, compound='right').place(x=10, y=330)
salePrice = ttk.Entry(tab1, textvariable= SALE_PRICE,font = ('Times',15), width = 25)
salePrice.place(x=170, y=330)

Label(tab1,text='DESC',font=('Times',15)).place(x=10, y = 370)
txbl = ttk.Entry(tab1,textvariable=DESC, width = 25, font= ('Times', 15))
txbl.place(x=170, y = 370)


def callback(eventObject):
    product = combo.get()
    try:
        print(product)
        local_cursor = mydb.cursor()
        local_cursor.execute("select s_price from products where NAME = "+ "'" + product + "'")
        values = local_cursor.fetchall()
        if len(values) <= 0:
            messagebox.showerror(message= "No Item Found Like " + combo.get())
            return
        SALE_PRICE.set([ x[0] for x in values ][0])
        qtyEntry.focus_set()
    except Exception as e:
        messagebox.showerror(title='Unique Computers', message=e)

combo.bind("<<ComboboxSelected>>", callback)
combo.bind("<Return>",callback)
qtyEntry.bind("<Return>",lambda _:salePrice.focus_set())
salePrice.bind("<Return>", lambda _: txbl.focus_set())
txbl.bind("<Return>", lambda _ : addProduct())


Button(tab1,font = ('Times',15), text='Enter',command=lambda : generate_bill(),image=enter_Image, compound='right').place(x=20, y = 190)
Button(tab1,font = ('Times',15), text='Close',command=lambda : root.destroy(), image=close_image, compound='left').place(x=110, y = 190)
Button(tab1,text='Generate Bill',font = ('Times',15),command=lambda : sendInto(tv,name.get(),now.strftime("%Y%m%d")),image=bill_Image, compound='right').place(x=210, y=190)

Button(tab1,text='ADD',font = ('Times',15),command=addProduct, image=add_Image, compound='left').place(x=150, y=420)
Button(tab1,text='REMOVE',font = ('Times',15),command=delete, image=remove_Image, compound='right').place(x=240, y=420)


tabControl.add(tab3, text='Home')
tabControl.add(tab1, text ='Sale') 
tabControl.add(tab2, text ='Stock') 
tabControl.add(tab4, text='Anvi EnterPries')
tabControl.pack(expand = 1, fill ="both")

# ttk.Label(tab1, text ="Welcome to GeeksForGeeks").grid(column = 0, row = 0, padx = 30, pady = 30) 
# ttk.Label(tab2, text ="Lets dive into the world of computers").grid(column = 0, row = 0, padx = 30, pady = 30) 
# SELECT NAME, PRICE, HSN, GST, CGST, SGST, BATCH, OPEN_STOCK, OPEN_STOCK_DATE, TOTAL FROM PRODUCTS;

STKtv = ttk.Treeview(tab2, height=25)
STKtv['columns']=('NAME', 'PRICE', 'HSN', 'GST', 'CGST', 'SGST', 'OPEN_STOCK', 'OPEN_STOCK_DATE', 'TOTAL')
STKtv.column('#0', width=0, stretch=NO)
STKtv.column('NAME', anchor=CENTER, width=100)
STKtv.column('PRICE', anchor=CENTER, width=100)
STKtv.column('HSN', anchor=CENTER, width=100)
STKtv.column('GST', anchor=CENTER, width=100)
STKtv.column('CGST', anchor=CENTER, width=100)
STKtv.column('SGST', anchor=CENTER, width=100)
STKtv.column('OPEN_STOCK', anchor=CENTER, width=100)
STKtv.column('OPEN_STOCK_DATE', anchor=CENTER, width=100)
STKtv.column('TOTAL', anchor=CENTER, width=100)

STKtv.heading('#0', text='', anchor=CENTER)
STKtv.heading('NAME', text='NAME', anchor=CENTER)
STKtv.heading('PRICE', text='PRICE', anchor=CENTER)
STKtv.heading('HSN', text='HSN CODE', anchor=CENTER)
STKtv.heading('GST', text='GST', anchor=CENTER)
STKtv.heading('CGST', text='CGST', anchor=CENTER)
STKtv.heading('SGST', text='SGST', anchor=CENTER)
STKtv.heading('OPEN_STOCK', text='OPENSTOCK', anchor=CENTER)
STKtv.heading('OPEN_STOCK_DATE', text='DATEOFOPENING', anchor=CENTER)
STKtv.heading('TOTAL', text='TOTAL', anchor=CENTER)

for i in stkresult:
    STKtv.insert("",0, values=i)

STKtv.configure(yscrollcommand = verscrlbar.set)
verscrlbarTAB2.pack(side ='right', fill =BOTH)
STKtv.pack(anchor = CENTER)

Button(tab2,text='Refersh',command=lambda: refreshstock(STKtv),padx=20,pady=20).place(x=20, y=550)
Button(tab2,text='Delte',command=deleteItem,padx=20,pady=20).place(x=150, y=550)
Button(tab2,text='Add New Item',command=addItem,padx=20,pady=20).place(x=250, y=550) 
root.mainloop() 
mycursor.close()