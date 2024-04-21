from anvienterprises import *
try:     
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database = "stock"
    )

    mycursor = mydb.cursor()
except Exception as e:
    messagebox.showerror(title="Error",message=e)


def homeWindow(homeTab, root, tabNoteBook):
    
    try:
        hoemTabStyle = ttk.Style(homeTab)
        hoemTabStyle.theme_use('clam')
        hoemTabStyle.configure("Treeview",background='gray')
    except Exception as e:
        messagebox.showerror(title='Error', message=e)

    Collection = DoubleVar()
    Balance = DoubleVar()
    calS = StringVar()
    tillS = StringVar()
    try:
        global new_party,new_vendor,delete_party,delete_vendor, coll_Image, sale_Image, apply_Image
        new_party = PhotoImage(file = 'new_party.png').subsample(5,5)
        new_vendor = PhotoImage(file = 'edit_vendor.png').subsample(5,5)
        delete_party = PhotoImage(file = 'delete_party.png').subsample(6,6)
        delete_vendor = PhotoImage(file = 'editVendor.png').subsample(7,7)
        coll_Image = PhotoImage(file = 'collection.png').subsample(15,15)
        sale_Image = PhotoImage(file = 'monthly_collection.png').subsample(15,15)
        apply_Image = PhotoImage(file = 'apply.png').subsample(15,15)
    except Exception as e:
        messagebox.showerror(title='Error in Home Icon Placement', message=e)
    try:
        mycursor.execute('Select sum(total) from sale')
        balanceSheet = mycursor.fetchone()
    except Exception as error:
        messagebox.showerror(title='Error in Home Tab', message=error)
    ttk.Label(homeTab, text='Todays Collection',font = ('Times',15),padding=(10,10), image=coll_Image, compound='right').place(x=4, y = 10)
    cln = ttk.Label(homeTab,text=balanceSheet[0],font = ('Times', 15),width=10,padding=(10,10), foreground='black')
    cln.place(x=200, y = 10)

    ttk.Label(homeTab, text='Balance',font = ('Times',15),padding=(10,10), image= sale_Image, compound='right').place(x=320, y = 10)

    ttk.Label(homeTab,text=balanceSheet[0],font = ('Times', 15),padding=(10,10),background='Pink',width=10).place(x=420, y = 10)
    ttk.Label(homeTab, text='Monthly Sale',font = ('Times',15),padding=(10,10), image=coll_Image, compound='right').place(x=520, y = 10)
    ttk.Label(homeTab, text=balanceSheet[0],font = ('Times',15),padding=(10,10)).place(x=670, y = 10)
    cal = DateEntry(homeTab, selectmode='day',width= 20, background= "magenta3", foreground= "white",textvariable = calS)
    cal.place(x=780,y=20)
    upto = DateEntry(homeTab, selectmode='day',width= 20, background= "magenta3", foreground= "white",textvariable = tillS)
    upto.place(x=940,y=20)
    Button(homeTab, text='Apply', font=('Times', 12), command=lambda: applyCustum(cal, upto, combo), image=apply_Image, compound='left').place(x=1100, y=10)
    # ttk.Label(homeTab, text='Balance',font = ('Times',15),padding=(10,10)).place(x=320, y = 10)
    ttk.Label(homeTab,text='Today\'s Sale Logs', font=('Times',15),background='magenta3',foreground="white",
              width= 135,anchor="center"            
              ).place(x = 0, y=70)
    try:
        Button(homeTab, text='Add New Party', command= add_customer,font=('Times',15),image = new_party,compound='left',bg='white').place(x=870, y=450)
        Button(homeTab, text='Add New Vendor', command= None, bg='white', font=('Times',15),image= new_vendor, compound='left').place(x=1070, y=450)
        Button(homeTab, text='Delete Party', command= deleteParty, bg='white', font=('Times',15), image=delete_party, compound='left').place(x=700, y=450)
        Button(homeTab, text='Close', command=lambda: root.destroy(), bg='white', font=('Times',15),image=delete_vendor, compound='left').place(x=700, y=350)
        Button(homeTab, text='Delete Vendor', command= None, bg='white', font=('Times',15),image=delete_vendor, compound='left').place(x=850, y=350)
        Button(homeTab, text='Search Record', command= search_records, bg='white', font=('Times',15),image=delete_vendor, compound='left').place(x=1050, y=350)
        combo = AutocompleteCombobox(homeTab, width=15, font=('Times', 15), completevalues=['Unique Computers','Anvi Enterprises'])
        combo.place(x=1070, y=550) 
    except:
        messagebox.showerror(title='Error', message='Error In Icon Placement')
    createSaleTree(homeTab)
    showOutOfStock(homeTab)  

def createSaleTree(homeFrame):
    """ this will create a tree view in slae table
    """
    def onLogScroll(*args):
        STKtv.yview(*args)
    
    STKtv = ttk.Treeview(homeFrame, height=25)
    STKtv['columns']=('Invoice No', 'Custumer ID','Name', 'Items', 'Total')
    STKtv.column('#0', width=0, stretch=NO)
    STKtv.column('Invoice No', anchor=CENTER, width=100)
    STKtv.column('Custumer ID', anchor=CENTER, width=100)
    STKtv.column('Name', anchor=CENTER, width=200)
    STKtv.column('Items', anchor=CENTER, width=100)
    STKtv.column('Total', anchor=CENTER, width=100)

    STKtv.heading('#0', text='', anchor=CENTER)
    STKtv.heading('Invoice No', text='Invoice No', anchor=CENTER)
    STKtv.heading('Custumer ID', text='Custumer ID', anchor=CENTER)
    STKtv.heading('Name', text='NAME', anchor=CENTER)
    STKtv.heading('Items', text='Items', anchor=CENTER)
    STKtv.heading('Total', text='Total', anchor=CENTER)
    
    Button(homeFrame, text='Refresh', command=lambda: refresh(STKtv), bg='white', font=('Times', 15)).place(x=700, y= 550)

    scrollbar = ttk.Scrollbar(homeFrame, orient="vertical", command=onLogScroll)
    scrollbar.place(x=660, y= 100, height= 500)
    # scrollbar.config(height = 300)
    STKtv.configure(yscrollcommand=scrollbar.set)
    
    try:
        sales  = salesTable()
        for i in sales:
          STKtv.insert("",0, values=i)
    except Exception as e:
        messagebox.showerror(title='UC',message=e)
    STKtv.place(x=50, y=100)
    
def refresh(tree):
    try:
        tree.delete(*tree.get_children())

        sales  = salesTable()
        if not sales:
            messagebox.showerror(title='Unique Computers',message='Bhai Aj Kuch Bhi nahi Bika :(')
            return
        for i in sales:
          tree.insert("",0, values=i)
    except Exception as e:
        messagebox.showerror(title='UC',message=e)
    
def salesTable():
    try:
        mycursor.execute('select No, cid, NAME, Items, Total from sale where P_DATE = %s',(datetime.now().strftime('%Y-%m-%d'),))
        records = mycursor.fetchall()
        print('HAbibi-HomeWin',[ x for x in records])
        return records
    except Exception as e:
        print('error in sales query- Home Tab')
        messagebox.showerror(title='Error',message=e)


def applyCustum(fromdate, tilldate, combo):
    """ Used to Show the Collection Based on Custom Choice/Filter
    """
    try:
        mycursor.execute('SELECT SUM(Total), count(*) from sale WHERE P_DATE BETWEEN %s AND %s',(tilldate.get_date().strftime('%Y-%m-%d'),fromdate.get_date().strftime('%Y-%m-%d')))
        value = mycursor.fetchone()
        if value:
            print(x for x in value)
            choice = messagebox.askyesno(title='Collection', message= "Generate ? \n Amt = "+ str(value[0]) +"\ncount = "+ str(value[1]))
            if choice :
                toExcel(tilldate.get_date().strftime('%Y-%m-%d'),fromdate.get_date().strftime('%Y-%m-%d'), combo)
            else:
                messagebox.showinfo(title='Unique computers', message= 'Ok Bhai \n Samaz Gaya !')
        else:
            messagebox.showerror(title='Error', message='Can\'t find Data')
    except Exception as e:
        messagebox.showerror(title='Error-In Date', message=e)
    print(tilldate.get_date().strftime('%Y-%m-%d'), "\t\t", fromdate.get_date().strftime('%Y-%m-%d'))


def showOutOfStock(homeFrame):
    tree = ttk.Treeview(homeFrame,  height=10)

    tree['columns']=('StockDate', 'Name', 'OpenStock','Price')
    tree.column('#0', width=0, stretch=NO)
    tree.column('StockDate', anchor=CENTER, width=150)
    tree.column('Name', anchor=CENTER, width=200)
    tree.column('OpenStock', anchor=CENTER, width=100)
    tree.column('Price', anchor=CENTER, width=100)

    tree.heading('#0', text='', anchor=CENTER)
    tree.heading('StockDate', text='Stock Date', anchor=CENTER)
    tree.heading('Name', text='Name', anchor=CENTER)
    tree.heading('OpenStock', text='Open Stock', anchor=CENTER)
    tree.heading('Price', text='Price', anchor=CENTER)

    tree.place(x=700, y = 100)

    try:
        mycursor.execute('SELECT OPEN_STOCK_DATE, NAME, OPEN_STOCK, PRICE FROM PRODUCTS WHERE STOCK = 0 OR STOCK < 1')
        Values =  mycursor.fetchall()
        for i in Values:
          tree.insert("",0, values=i)
    except Exception as e:
        messagebox.showerror(title='Unique Compueters', message=e)
