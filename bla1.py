from tkinter import Tk, ttk, VERTICAL, HORIZONTAL, RIGHT, BOTTOM, Y, X, Button, Entry, Label, W, E, S, N
import tkinter.ttk as ttk
import pymysql

root = Tk()
root.title("Inventory System")
root.geometry("900x420")
my_tree = ttk.Treeview(root)
storeName = "Inventory System"


def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


def insert_position(title):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Positions (title) VALUES (%s)", (title,))
    conn.commit()
    conn.close()


def delete_position(data):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Positions(PositionId INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50))""")

    cursor.execute("DELETE FROM Positions WHERE PositionId = %s", (data,))
    conn.commit()
    conn.close()


def update_position(title, position_id):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Positions(PositionId INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50))""")

    cursor.execute("UPDATE Positions SET title = %s WHERE PositionId = %s", (title, position_id))
    conn.commit()
    conn.close()


def read():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Positions(PositionId INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50))""")

    cursor.execute("SELECT * FROM Positions")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def insert_data():
    title = str(entryTitle.get())
    if title == "" or title == " ":
        print("Error Inserting Title")
    else:
        insert_position(title)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


def delete_data():
    selected_item = my_tree.selection()[0]
    deleteData = my_tree.item(selected_item)['values'][0]
    delete_position(deleteData)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


def update_data():
    selected_item = my_tree.selection()[0]
    update_position_id = my_tree.item(selected_item)['values'][0]
    update_position(entryTitle.get(), update_position_id)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]), tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2)
titleLabel.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

titleInputLabel = Label(root, text="Title", font=('Arial bold', 15))
titleInputLabel.grid(row=1, column=0, padx=10, pady=10)

entryTitle = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryTitle.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

buttonEnter = Button(
    root, text="Enter", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#0099ff", command=insert_data)
buttonEnter.grid(row=2, column=1, columnspan=1)

buttonUpdate = Button(
    root, text="Update", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#ffff00", command=update_data)
buttonUpdate.grid(row=2, column=2, columnspan=1)

buttonDelete = Button(
    root, text="Delete", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#e62e00", command=delete_data)
buttonDelete.grid(row=2, column=3, columnspan=1)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial bold', 15))

my_tree['columns'] = ("ID", "Title")
my_tree.column("#0", width=0, stretch='NO')
my_tree.column("ID", anchor='w', width=100)
my_tree.column("Title", anchor='w', width=500)
my_tree.heading("ID", text="ID", anchor='w')
my_tree.heading("Title", text="Title", anchor='w')

scrollbar_y = ttk.Scrollbar(root, orient=VERTICAL, command=my_tree.yview)
my_tree.configure(yscrollcommand=scrollbar_y.set)
scrollbar_y.grid(row=1, column=9, rowspan=5, sticky=N+S)

scrollbar_x = ttk.Scrollbar(root, orient=HORIZONTAL, command=my_tree.xview)
my_tree.configure(xscrollcommand=scrollbar_x.set)
scrollbar_x.grid(row=6, column=5, columnspan=4, sticky=W+E)

for data in my_tree.get_children():
    my_tree.delete(data)

for result in reverse(read()):
    my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]), tag="orow")

my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

root.mainloop()
