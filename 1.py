from tkinter import Tk, Label, Entry, Button, ttk, Scrollbar
from tkinter import VERTICAL, HORIZONTAL, N, S, W, E

import pymysql

root = Tk()
root.title("Job Management System")
root.geometry("900x420")
my_tree = ttk.Treeview(root)
storeName = "Job Management System"


def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


def insert_job(job_type, volume, equipment_type, execution_date, fuel_consumption):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Jobs(JobId INT AUTO_INCREMENT PRIMARY KEY, 
        JobType VARCHAR(50), 
        Volume INT, 
        EquipmentType VARCHAR(50), 
        ExecutionDate DATE, 
        FuelConsumption FLOAT)""")

    query = "INSERT INTO Jobs (JobType, Volume, EquipmentType, ExecutionDate, FuelConsumption) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (job_type, volume, equipment_type, execution_date, fuel_consumption))
    conn.commit()
    conn.close()


def delete_job(job_id):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Jobs(JobId INT AUTO_INCREMENT PRIMARY KEY, 
        JobType VARCHAR(50), 
        Volume INT, 
        EquipmentType VARCHAR(50), 
        ExecutionDate DATE, 
        FuelConsumption FLOAT)""")

    query = "DELETE FROM Jobs WHERE JobId = %s"
    cursor.execute(query, (job_id,))
    conn.commit()
    conn.close()


def update_job(job_id, job_type, volume, equipment_type, execution_date, fuel_consumption):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Jobs(JobId INT AUTO_INCREMENT PRIMARY KEY, 
        JobType VARCHAR(50), 
        Volume INT, 
        EquipmentType VARCHAR(50), 
        ExecutionDate DATE, 
        FuelConsumption FLOAT)""")

    query = "UPDATE Jobs SET JobType = %s, Volume = %s, EquipmentType = %s, ExecutionDate = %s, FuelConsumption = %s WHERE JobId = %s"
    cursor.execute(query, (job_type, volume, equipment_type, execution_date, fuel_consumption, job_id))
    conn.commit()
    conn.close()


def read_jobs():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="3Ey6x+eQ",
        database="farming"
    )
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        Jobs(JobId INT AUTO_INCREMENT PRIMARY KEY, 
        JobType VARCHAR(50), 
        Volume INT, 
        EquipmentType VARCHAR(50), 
        ExecutionDate DATE, 
        FuelConsumption FLOAT)""")

    cursor.execute("SELECT * FROM Jobs")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def insert_data():
    job_type = str(entryJobType.get())
    volume = int(entryVolume.get())
    equipment_type = str(entryEquipmentType.get())
    execution_date = str(entryExecutionDate.get())
    fuel_consumption = float(entryFuelConsumption.get())

    insert_job(job_type, volume, equipment_type, execution_date, fuel_consumption)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read_jobs()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[1:], tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=6, rowspan=5, padx=10, pady=10, sticky=(N, S, W, E))


def delete_data():
    selected_item = my_tree.selection()[0]
    deleteData = my_tree.item(selected_item)['values'][0]
    delete_job(deleteData)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read_jobs()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[1:], tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=6, rowspan=5, padx=10, pady=10, sticky=(N, S, W, E))


def update_data():
    selected_item = my_tree.selection()[0]
    update_job_id = my_tree.item(selected_item)['values'][0]
    job_type = str(entryJobType.get())
    volume = int(entryVolume.get())
    equipment_type = str(entryEquipmentType.get())
    execution_date = str(entryExecutionDate.get())
    fuel_consumption = float(entryFuelConsumption.get())

    update_job(update_job_id, job_type, volume, equipment_type, execution_date, fuel_consumption)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read_jobs()):
        my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[1:], tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')
    my_tree.grid(row=1, column=5, columnspan=6, rowspan=5, padx=10, pady=10, sticky=(N, S, W, E))


titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2)
titleLabel.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

jobTypeLabel = Label(root, text="Job Type", font=('Arial bold', 15))
jobTypeLabel.grid(row=1, column=0, padx=10, pady=10)

entryJobType = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryJobType.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

volumeLabel = Label(root, text="Volume", font=('Arial bold', 15))
volumeLabel.grid(row=2, column=0, padx=10, pady=10)

entryVolume = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryVolume.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

equipmentTypeLabel = Label(root, text="Equipment Type", font=('Arial bold', 15))
equipmentTypeLabel.grid(row=3, column=0, padx=10, pady=10)

entryEquipmentType = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryEquipmentType.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

executionDateLabel = Label(root, text="Execution Date", font=('Arial bold', 15))
executionDateLabel.grid(row=4, column=0, padx=10, pady=10)

entryExecutionDate = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryExecutionDate.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

fuelConsumptionLabel = Label(root, text="Fuel Consumption", font=('Arial bold', 15))
fuelConsumptionLabel.grid(row=5, column=0, padx=10, pady=10)

entryFuelConsumption = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryFuelConsumption.grid(row=5, column=1, columnspan=3, padx=5, pady=5)

buttonEnter = Button(
    root, text="Enter", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#0099ff", command=insert_data)
buttonEnter.grid(row=6, column=1, columnspan=1)

buttonUpdate = Button(
    root, text="Update", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#ffff00", command=update_data)
buttonUpdate.grid(row=6, column=2, columnspan=1)

buttonDelete = Button(
    root, text="Delete", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#e62e00", command=delete_data)
buttonDelete.grid(row=6, column=3, columnspan=1)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial bold', 15))

my_tree['columns'] = ("Job ID", "Job Type", "Volume", "Equipment Type", "Execution Date", "Fuel Consumption")
my_tree.column("#0", width=0, stretch='NO')
my_tree.column("Job ID", anchor='w', width=100)
my_tree.column("Job Type", anchor='w', width=100)
my_tree.column("Volume", anchor='w', width=100)
my_tree.column("Equipment Type", anchor='w', width=150)
my_tree.column("Execution Date", anchor='w', width=150)
my_tree.column("Fuel Consumption", anchor='w', width=150)
my_tree.heading("Job ID", text="Job ID", anchor='w')
my_tree.heading("Job Type", text="Job Type", anchor='w')
my_tree.heading("Volume", text="Volume", anchor='w')
my_tree.heading("Equipment Type", text="Equipment Type", anchor='w')
my_tree.heading("Execution Date", text="Execution Date", anchor='w')
my_tree.heading("Fuel Consumption", text="Fuel Consumption", anchor='w')

my_tree.grid(row=1, column=5, columnspan=6, rowspan=5, padx=10, pady=10, sticky=(N, S, W, E))

scrollbar_y = ttk.Scrollbar(root, orient=VERTICAL, command=my_tree.yview)
my_tree.configure(yscrollcommand=scrollbar_y.set)
scrollbar_y.grid(row=1, column=15, rowspan=5, sticky=N+S)

scrollbar_x = ttk.Scrollbar(root, orient=HORIZONTAL, command=my_tree.xview)
my_tree.configure(xscrollcommand=scrollbar_x.set)
scrollbar_x.grid(row=6, column=5, columnspan=4, sticky=W+E)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)
root.columnconfigure(7, weight=1)
root.columnconfigure(8, weight=1)
root.columnconfigure(9, weight=1)
root.columnconfigure(10, weight=1)
root.columnconfigure(11, weight=1)

for result in reverse(read_jobs()):
    my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[1:], tag="orow")

my_tree.tag_configure('orow', background='#EEEEEE')

root.mainloop()
