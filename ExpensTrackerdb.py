from tkinter import *
import sqlite3
from tkcalendar import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.geometry("500x500")
root.title("Expense Tracker")

try:
    #Connecting to Database
    dbconn = sqlite3.connect('Expense_Tracker.db')
    dbcursor = dbconn.cursor()

    dbcursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses_new (
            SNo INTEGER PRIMARY KEY AUTOINCREMENT,
            Date DATETIME,
            Payee VARCHAR(255),
            Description VARCHAR(255),
            Amount FLOAT,
            Mode_Of_Payment VARCHAR(255)
        )
    """)

    dbcursor.execute("""
        INSERT INTO expenses_new (SNo, Date, Payee, Description, Amount, Mode_Of_Payment)
        SELECT SNo, Date, Payee, Description, Amount, "Mode Of Payment"
        FROM expenses
    """)

    dbcursor.execute("DROP TABLE IF EXISTS expenses")
    dbcursor.execute("ALTER TABLE expenses_new RENAME TO expenses")


    #creating table named expenses...
   # dbcursor.execute("""
          #              CREATE TABLE IF NOT EXISTS expenses(
   #                           SNo INTEGER PRIMARY KEY AUTOINCREMENT ,
    #                          Date DATETIME,
     #                         Payee VARCHAR(255),
      #                        Description VARCHAR(255),
       #                       Amount FLOAT,
        #                      "Mode Of Payment" VARCHAR(255)
         #               )
               #     """)


    dbconn.commit()

except sqlite3.Error as e:
    print("Error while working with SQLite", e)

finally:
        if dbconn:
            dbconn.close()



frame1 = Frame(root,width=600,height=900)
frame1.pack(side="left",expand=1,fill="both")
#frame1.grid(row=0,column=0)

frame2 = Frame(root,width=500,height=900,bg="black")
frame2.pack(side="right",expand=1,fill="both")
#frame2.grid(row=0,column=1)


#added left image..on frame1
my_pic1 = Image.open("expense_img/main.png")
resized = my_pic1.resize((950, 700))
img_1 = ImageTk.PhotoImage(resized)
img = Label(frame1, image=img_1)
img.pack(fill="both",expand=1)


#added top right image.. on frame2..
my_pic2 = ImageTk.PhotoImage(Image.open("expense_img/main2.png"))
img2 = Label(frame2, image=my_pic2)
img2.pack(pady=20)
#img2.grid(row=0,column=0,sticky="n",pady=3)

def submit(_list):
    check = 0        #check if list does not contain any empty string..(if user has not entered any data)
    for i in _list:
        if i.get() == "":
            pass
        else:
            check += 1

    try:
        if check == 5:
            dbconn = sqlite3.connect('Expense_Tracker.db')
            dbcursor = dbconn.cursor()
            dbcursor.execute("""INSERT INTO expenses (Date, Payee, Description, Amount, Mode_Of_Payment)\
                             VALUES (:Date, :Payee, :Description, :Amount, :Mode_Of_Payment)""",
                             {
                                 'Date': (_list[0]).get(),
                                 'Payee': (_list[3]).get(),
                                 'Description': (_list[1]).get(),
                                 'Amount': float((_list[2].get())),
                                 'Mode_Of_Payment': _list[4].get()
                                        }
                            )
            dbconn.commit()
            dbconn.close()

            messagebox.showinfo("Success", "Successfully added the record to the database")
            for i in _list:
                i.delete(0,END)

        else:
            messagebox.showwarning("WARNING!", "One or more than one fields are empty\nPlease Check Again")
            pass

    except(ValueError):
        messagebox.showwarning("WARNING!", "Amount Paid must be integer number\nPlease Check Again")
    exp.destroy()


def remove():
    #this function removes the selected record from the database
    ch = 0
    dbconn = sqlite3.connect('Expense_Tracker.db')
    dbcursor = dbconn.cursor()

    x = my_tree.selection()      #get currently selected item...

    for record in x:
        dbcursor.execute("DELETE FROM expenses WHERE oid= " + str(ltt[(int(record) - 1)]))
        my_tree.delete(record)
        ch+=1
    if ch == 0:
        messagebox.showwarning("Attention", "You must select atleast one record to perform this action")

    dbconn.commit()
    dbconn.close()


#function for new window on clicking update record button and retreivingg the selected the record information...
def select_for_update():
    new_win = Tk()
    new_win.geometry("300x300")

    n1 = Label(new_win, text="Date Of Payment (MM/DD/YY)")
    n1.grid(row=0, column=0,padx=8, pady=8)
    n2 = Label(new_win, text="Method Of Payment")
    n2.grid(row=1, column=0,padx=8, pady=8)
    n3 = Label(new_win, text="Paid To")
    n3.grid(row=2, column=0,padx=8,pady=8)
    n4 = Label(new_win, text="Description")
    n4.grid(row=3, column=0,padx=8,pady=8)
    n5 = Label(new_win, text="Amount Paid")
    n5.grid(row=4, column=0,padx=8,pady=8)

    global name_box1, name_box2, name_box3, name_box4, name_box5

    name_box1 = DateEntry(new_win, background='grey', foreground='white', borderwidth=2)
    name_box1.grid(row=0, column=1,padx=9,pady=8)
    name_box2 = StringVar()
    name_box2.set("CASH")
    ttk.Combobox(new_win, values=["CARD", "PAYTM", "CHEQUE", "ONLINE TRANSACTION"]).grid(row=1, column=1,padx=9,pady=8)
    name_box3 = Entry(new_win)
    name_box3.grid(row=2, column=1,padx=9,pady=8)
    name_box4 = Entry(new_win)
    name_box4.grid(row=3, column=1,padx=9,pady=8)

    name_box = DoubleVar()
    #name_box.set("")
    name_box5 = Entry(new_win, textvariable=name_box)
    name_box5.grid(row=4, column=1,padx=9,pady=8)
    global name_box5_value
    name_box5_value = name_box.get()

    update_bt = Button(new_win, text="UPDATE RECORD", font=("Helvetica", 11), command=update1)
    update_bt.grid(row=6,column=0,columnspan=2,padx=8,pady=9)


    global p
    global z
    global listv
    listv = []
    m = 0
    selection = my_tree.focus()    #retrieves ID of selected record...

    values = my_tree.item(selection, 'values')        #returns a tuple containing values of selected record
    if selection == "":
        messagebox.showwarning("Attention", "You must select atleast one record to perform this action")
    else:
        for k in range(0, 5):
            listv.append(values[k])

        try:
            name_box1.insert(0, values[0])
            name_box2.set(values[1])
            name_box3.insert(0, values[2])
            name_box4.insert(0, values[3])
            name_box5.insert(0, values[4])
            z = 1
        except(IndexError):
            pass

    new_win.mainloop()

#update function
def update1():
    global p
    global z
    global listv

    m = 0
    selection = my_tree.focus()

    if [name_box1.get(), name_box2.get(), name_box3.get(), name_box4.get(), name_box5.get()] == listv:
        messagebox.showinfo("Attention", "Seems as if you didn't make any change to the existing record")
    else:
        if z == 1 and selection != "":
            z = 0
            try:
                dbconn = sqlite3.connect('Expense_Tracker.db')
                dbcursor = dbconn.cursor()
                selection = my_tree.focus()
                values = my_tree.item(selection, text="", values=(name_box1.get(),
                                                                name_box2.get(),
                                                                name_box3.get(),
                                                                name_box4.get(),
                                                                name_box5.get()))
                x = my_tree.selection()
                for record in x:
                    dbcursor.execute("UPDATE expenses" +
                                     "SET Date_Of_Payment = " + str(name_box1.get()) + ", Method_of_Payment = '"+str(name_box2.get())\
                                     + "' , Paid_To = '"+ str(name_box3.get()) + \
                                     "' , Description = '" + str(name_box4.get()) + \
                                     "' , Amount_Paid = " + str(name_box5.get())\
                    + " WHERE oid = " + str(ltt[(int(record) - 1)])+" ;")

            except(sqlite3.OperationalError):
                messagebox.showwarning("WARNING!", "Amount Paid must be a number\nPlease Check Again")

        else:
            messagebox.showwarning("Attention", "Seems You didn't select any record\nPlease Check Again")




def view_expenses(view_record_frame):
    global ltt
    ltt = []
    dbconn = sqlite3.connect('Expense_Tracker.db')
    dbcursor = dbconn.cursor()

    #fetch all expenses record
    dbcursor.execute("SELECT * FROM expenses")
    records = dbcursor.fetchall()
    print(records)

    #fetch oids separately...
    dbcursor.execute("SELECT oid FROM expenses")
    rec = dbcursor.fetchall()
    print(rec)

    for r in rec:
        ltt.append(r[0])

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="white", foreground="black", rowheight=40, fieldbackground="white")
    style.map('Treeview', background=[('selected', 'green')])

    tree_scroll = Scrollbar(view_record_frame,orient=VERTICAL)
    tree_scroll.pack(side=RIGHT, fill=Y)

    global my_tree
    my_tree = ttk.Treeview(view_record_frame,yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=my_tree.yview)
    my_tree.tag_configure("oddrow", background="WHITE")
    my_tree.tag_configure("evenrow", background="grey")

    my_tree['columns'] = ('SNo','Date Of Payment', 'Payee', 'Description', 'Amount Paid(In Rupees)','Method Of Payment')
    my_tree.column("#0", width=0, anchor=W, minwidth=0, stretch=NO)
    my_tree.column("SNo", width=200, anchor=W, minwidth=25)
    my_tree.column("Date Of Payment", width=200, anchor=W, minwidth=25)
    my_tree.column("Payee", width=200, anchor=W, minwidth=25)
    my_tree.column("Description", width=200, anchor=W, minwidth=50)
    my_tree.column("Amount Paid(In Rupees)", width=200, anchor=W, minwidth=25)
    my_tree.column("Method Of Payment", width=200, anchor=W, minwidth=25)

    my_tree.heading("#0", text="Label", anchor=W)
    my_tree.heading("SNo", text="SNo", anchor=W)
    my_tree.heading("Date Of Payment", text="Date Of Payment (MM/DD/YY)", anchor=W)
    my_tree.heading("Payee", text="Paid To", anchor=W)
    my_tree.heading("Description", text="Description", anchor=W)
    my_tree.heading("Amount Paid(In Rupees)", text="Amount Paid(In Rs)", anchor=W)
    my_tree.heading("Method Of Payment", text="Method Of Payment", anchor=W)

    p= 1
    for record in records:
        if p % 2 == 0:
            my_tree.insert(parent='', index='end', iid = p, text='Parent', values=record, tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid = p, text='Parent', values=record, tags=('oddrow',))
        p += 1
    my_tree.pack(padx=10, ipadx=50, ipady=20)


    del_button = Button(view_record_frame,text="DELETE THE SELECTED RECORD",bg="black",font=("BOLD", 15),command=remove,foreground="white")
    del_button.pack(padx=10,pady=20)

    update_bt = Button(view_record_frame,text="UPDATE THE SELECTED RECORD",bg="black",font=("BOLD",13),command=select_for_update,foreground="white")
    update_bt.pack(padx=10,pady=7)

    '''
    n1 = Label(new_win, text="Date Of Payment (MM/DD/YY)")
    n1.grid(row=1,column=0)
    n2 = Label(new_win, text="Method Of Payment")
    n2.grid(row=1, column=1)
    n3 = Label(new_win, text="Paid To")
    n3.grid(row=1, column=2)
    n4 = Label(new_win, text="Description")
    n4.grid(row=1, column=3)
    n5 = Label(new_win, text="Amount Paid")
    n5.grid(row=1, column=4)

    global name_box1
    global name_box2
    global name_box3
    global name_box4
    global name_box5
    global name_box

    name_box = IntVar()
    name_box.set("")
    name_box1 = DateEntry(view_record_frame,background='grey', foreground='white', borderwidth=2)
    name_box1.grid(row=2, column=0)

    name_box2 = StringVar()
    name_box2.set("CASH")
    ttk.Combobox(view_record_frame,values=["CARD","PAYTM", "CHEQUE", "ONLINE TRANSACTION"]).grid(row=2,column=1)
    name_box3 = Entry(view_record_frame)
    name_box3.grid(row=2, column=2)
    name_box4 = Entry(view_record_frame)
    name_box4.grid(row=2, column=3)
    name_box5 = Entry(view_record_frame, textvariable=name_box)
    name_box5.grid(row=2, column=4)
    '''

    dbconn.commit()
    dbconn.close()



#function get called on clicking track expense image on root window..
def open_expense():
    global exp
    exp = Tk()          #new window opens
    exp.geometry("500x500")
    exp.title("Track Expense")

    #creating a notebook containing different tabs..
    my_nb = ttk.Notebook(exp)
    my_nb.pack(expand=True, fill="both")

    new_record_frame = Frame(my_nb)
    my_nb.add(new_record_frame, text="Add New Expense")

    global view_record_frame
    view_record_frame = Frame(my_nb)
    my_nb.add(view_record_frame, text="View Expenses")
    view_expenses(view_record_frame)

    Amount_Paid = DoubleVar()
    #extracting data from user for a new record(expense)...
    #entry boxes...
    date_of_payment_entry = DateEntry(new_record_frame, width=12, background="black", foreground="white", borderwidth=2)
    date_of_payment_entry.grid(row=0, column=1, padx=20)
    Description_Entry = Entry(new_record_frame, width=25)
    Description_Entry.grid(row=1, column=1,pady=3,padx=15)
    Amount_Paid_Entry = Entry(new_record_frame, width=25, textvariable=Amount_Paid)
    Amount_Paid_Entry.grid(row=2, column=1,pady=10,padx=15)
    Paid_To_Entry = Entry(new_record_frame, width=25)
    Paid_To_Entry.grid(row=3, column=1,padx=15,pady=7)
    global mode_of_payment
    mode_of_payment = ttk.Combobox(new_record_frame, values=["CASH","CARD","PAYTM","CHEQUE","ONLINE TRANSACTION"])
    mode_of_payment.current(0)
    mode_of_payment.grid(row=4, column=1,padx=14,pady=12)

    #label corresponding to each entry box...
    date_of_payment_label = Label(new_record_frame,text="Date of Payment\n(MM\DD\YY)", font=("Times New Roman",11))
    date_of_payment_label.grid(row=0,column=0,pady=40,padx=10)
    description_label = Label(new_record_frame, text="Description",font=("Times New Roman",11))
    description_label.grid(row=1, column=0,pady=10)
    amount_paid_label = Label(new_record_frame, text="Amount Paid(In Rs)", font=("Times New Roman",11))
    amount_paid_label.grid(row=2, column=0,pady=10)
    paid_to_label = Label(new_record_frame, text="Payee",font=("Times New Roman",11))
    paid_to_label.grid(row=3, column=0,pady=10)
    mode_of_payment_label = Label(new_record_frame, text="Mode Of Payment\n",font=("Times New Roman",11))
    mode_of_payment_label.grid(row=4, column=0,pady=21)


    _list = [date_of_payment_entry, Description_Entry, Amount_Paid_Entry, Paid_To_Entry,mode_of_payment]
    print(mode_of_payment.get())

    #creating button to add data to database..and calls function submit()...
    submit_btn=Button(new_record_frame, text="Add Expense", command=lambda: submit(_list),bg="light blue",relief=RAISED)
    submit_btn.grid(row=5, column=0,columnspan=2,pady=10, padx=10,ipadx=100)

    exp.mainloop()





my_pic3 = Image.open("expense_img/main3.png")
track_img = ImageTk.PhotoImage(my_pic3.resize((250, 100)))
#my_pic3 = ImageTk.PhotoImage(Image.open("expense_img/main3.png"))
track_lbl_img = Label(frame2, image=track_img, relief="sunken", borderwidth=5)
track_lbl_img.pack(pady=50)
track_lbl_img.bind("<Button-1>", lambda event: open_expense())      #click on left mouse button..
text_lbl = Label(frame2, text="Click on above image..")
text_lbl.pack()


#bt = Button(frame2, text="Track Expense", width=20, command=open_expense)
#bt.grid(row=1, column=0, pady=20,sticky="s")
root.grid_rowconfigure(0, weight=2)
root.grid_columnconfigure(0, weight=2)
root.mainloop()