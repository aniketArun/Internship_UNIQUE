from docxtpl import DocxTemplate
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="uniquec",
  database = "stock"
)

mycursor = mydb.cursor()
def generate_bill():
    try:
        mycursor.execute('Select * from sale order by no limit 1')
        values  = mycursor.fetchall()
        row = []
        for tuples in values:
            for items in tuples:
                row.append(items)
        print(row)
        print("After print row")
        mycursor.execute("select name,hsn,qty,price,total from purchase where cid = %s and P_date = %s", (row[5], row[1]))
        frompurchase  = mycursor.fetchall()
        # invoc = []
        for tuples in frompurchase:
            # for items in tuples:
                # invoc.append(items)
            print(tuples)
        gen_invoice(frompurchase, row)
        print("Exit")
    except Exception as e:
        print(e)
    pass

def gen_invoice(items, listItems):
    doc = DocxTemplate("invoice_template.docx")

    doc.render({"name":listItems[2], 
                "phone":"555-55555",
                "invoice_list": items,
                "subtotal":listItems[4],
                "salestax":"10%",
                "total":listItems[4],
                "invoice_date":listItems[1],
                "invoice_no": listItems[0]})
    doc.save("new_invoice.docx") 

generate_bill()


