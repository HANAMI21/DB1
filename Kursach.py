from tkinter import ttk, messagebox
from tkinter.ttk import Treeview

import pymysql.cursors
from config import host, user, password, db_name
import tkinter as tk
from tkinter import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging
import sys
print("dfd")
print("dfd")
logging.basicConfig(filename='app.log', level=logging.INFO, filemode='w')

def connect_to_database():
    try:
        db_config = get_db_config()
        connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as ex:
        return None, ex


class DatabaseAuthApp:
    def __init__(self):
        self.current_user = ""
        self.root = tk.Tk()
        self.root.title("Авторизація користувача23232 в базі даних")
        self.root.geometry("340x280")
        self.background_image = tk.PhotoImage(file="fon.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)


        # Создание элементов интерфейса
        self.label_username = tk.Label(self.root, text="Ім'я користувача:", font=("Arial", 11))
        self.entry_username = tk.Entry(self.root)
        self.label_password = tk.Label(self.root, text="Пароль:", font=("Arial", 11))
        self.entry_password = tk.Entry(self.root, show="*")
        self.button_login = tk.Button(self.root, text="Увійти", font=("Arial", 11), command=self.login)

        # Размещение элементов интерфейса
        self.label_username.place(x=110, y=50)
        self.entry_username.place(x=110, y=75)
        self.label_password.place(x=140, y=100)
        self.entry_password.place(x=110, y=125)
        self.button_login.place(x=140, y=160)

        self.root.mainloop()

    def login(self):
        username = self.entry_username.get()
        password_user = self.entry_password.get()

        user_role = self.check_user_role(username, password_user)

        if user_role == 'admin':
            self.all_table()
            self.current_user = "Адмін"
            self.show_login_success_message("Ви зайшли як Адмін!")
        elif user_role == 'manager':
            self.choice()
            self.current_user = "Менеджер"
            self.show_login_success_message("Ви зайшли як Менеджер!")
        elif user_role == 'user':
            self.current_user = "User"
            self.show_login_info_message("Ви звичайний користувач, ви не маєте доступу до БД.")

    def check_user_role(self, username, password_user):
        with connection.cursor() as cursor:
            query = "SELECT Role FROM Users WHERE Email = %s AND Passw = %s;"
            cursor.execute(query, (username, password_user))
            result = cursor.fetchone()
            if result:
                return result['Role']
            else:
                return None

    def show_login_success_message(self, message):
        logging.info(message)
        messagebox.showinfo("Message", message)

    def show_login_info_message(self, message):
        messagebox.showinfo("Message", message)

    def choice(self):
        self.root.destroy()
        self.root = Tk()
        self.root.title("Database Viewer")
        self.root.geometry("300x200")

        self.crud = Button(self.root, text="CRUD", command=self.all_table, width=15, height=2)
        self.crud.pack(pady=20)

        self.plain = Button(self.root, text="20 QUERIES", command=self.all_queries, width=15, height=2)
        self.plain.pack()

    def all_table(self):
        logging.info(f"{self.current_user} вибрав all_table")
        self.root.destroy()
        self.root = Tk()
        self.root.title("Database Viewer")
        self.root.geometry("400x600")

        self.label = Label(self.root, text="Вибрати таблицю:", font=('Arial bold', 15))
        self.label.pack(pady=10)

        self.button_positions = Button(self.root, text="Positions", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                       bg="#0099ff", command=self.crud_positions)
        self.button_positions.pack(pady=5)

        self.button_jobs = Button(self.root, text="Jobs", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                  bg="#0099ff", command=self.crud_jobs)
        self.button_jobs.pack(pady=5)

        self.button_employees = Button(self.root, text="Employees", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                       bg="#0099ff", command=self.crud_employees)
        self.button_employees.pack(pady=5)

        self.button_agriculture_cultures = Button(self.root, text="Agriculture Cultures", padx=5, pady=5, width=20,
                                                  bd=3,
                                                  font=('Arial', 12), bg="#0099ff",
                                                  command=self.crud_agriculture_cultures)
        self.button_agriculture_cultures.pack(pady=5)

        self.button_clients = Button(self.root, text="Clients", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                     bg="#0099ff", command=self.crud_clents)
        self.button_clients.pack(pady=5)

        self.button_sales = Button(self.root, text="Sales", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                   bg="#0099ff", command=self.crud_sales)
        self.button_sales.pack(pady=5)

        self.button_products = Button(self.root, text="Products", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                      bg="#0099ff", command=self.crud_products)
        self.button_products.pack(pady=5)

        self.button_suppliers = Button(self.root, text="Suppliers", padx=5, pady=5, width=20, bd=3, font=('Arial', 12),
                                       bg="#0099ff", command=self.crud_suppliers)
        self.button_suppliers.pack(pady=5)

        self.button_supply_fertilizers = Button(self.root, text="Supply Fertilizers", padx=5, pady=5, width=20, bd=3,
                                                font=('Arial', 12), bg="#0099ff", command=self.crud_supply_fertilizers)
        self.button_supply_fertilizers.pack(pady=5)

        self.button_fertilizers = Button(self.root, text="Fertilizers", padx=5, pady=5, width=20, bd=3,
                                         font=('Arial', 12),
                                         bg="#0099ff", command=self.crud_fertilizers)
        self.button_fertilizers.pack(pady=5)

        self.root.mainloop()

    def crud_positions(self):
        logging.info(f"{self.current_user} вибрав Crud Positions")
        self.root = Tk()
        self.root.title("Crud Positions")
        self.root.geometry("900x270")
        self.my_tree = ttk.Treeview(self.root)

        self.titleInputLabel = Label(self.root, text="Title", font=('Arial bold', 15))
        self.titleInputLabel.grid(row=1, column=0, padx=10, pady=10)

        self.entryTitle = Entry(self.root, width=25, bd=5, font=('Arial bold', 15))
        self.entryTitle.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        self.buttonEnter = Button(
            self.root, text="Додати", padx=5, pady=5, width=5,
            bd=3, font=('Arial', 15), bg="#0099ff", command=self.insert_data_position)
        self.buttonEnter.grid(row=2, column=1, columnspan=1)

        self.buttonUpdate = Button(
            self.root, text="Оновити", padx=5, pady=5, width=8,
            bd=3, font=('Arial', 15), bg="#ffff00", command=self.update_data_position)
        self.buttonUpdate.grid(row=2, column=2, columnspan=1)

        self.buttonDelete = Button(
            self.root, text="Видалити", padx=5, pady=5, width=8,
            bd=3, font=('Arial', 15), bg="#e62e00", command=self.delete_data_position)
        self.buttonDelete.grid(row=2, column=3, columnspan=1)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=('Arial bold', 15))

        self.my_tree['columns'] = ("ID", "Title")
        self.my_tree.column("#0", width=0, stretch='NO')
        self.my_tree.column("ID", anchor='w', width=100)
        self.my_tree.column("Title", anchor='w', width=500)
        self.my_tree.heading("ID", text="ID", anchor='w')
        self.my_tree.heading("Title", text="Title", anchor='w')

        self.scrollbar_y = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.my_tree.yview)
        self.my_tree.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.grid(row=1, column=9, rowspan=5, sticky=N + S)

        self.scrollbar_x = ttk.Scrollbar(self.root, orient=HORIZONTAL, command=self.my_tree.xview)
        self.my_tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.grid(row=6, column=5, columnspan=4, sticky=W + E)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read_positions()):
            self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]),
                                tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

        self.root.mainloop()

    def reverse(self, tuples):
        new_tup = tuples[::-1]
        return new_tup

    def update_position(self, title, position_id):

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

    def update_data_position(self):
        logging.info(f"{self.current_user} вибрав update Positions")
        self.selected_item = self.my_tree.selection()[0]
        self.update_position_id = self.my_tree.item(self.selected_item)['values'][0]
        self.update_position(self.entryTitle.get(), self.update_position_id)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read_positions()):
            self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]),
                                tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def read_positions(self):
        # добавляем данные
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

    def insert_position(self, title):
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

    def insert_data_position(self):
        logging.info(f"{self.current_user} вибрав insert Positions")
        title = str(self.entryTitle.get())
        if title == "" or title == " ":
            print("Error Inserting Title")
        else:
            self.insert_position(title)

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read_positions()):
            self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]),
                                tag="orow")

        self.my_tree.tag_configure('orow', background='#EEEEEE')
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def delete_data_position(self):
        logging.info(f"{self.current_user} вибрав delete Positions")
        selected_items = self.my_tree.selection()
        if selected_items:
            self.selected_item = selected_items[0]
            self.deleteData = self.my_tree.item(self.selected_item)['values'][0]
            self.delete_position(self.deleteData)

            for data in self.my_tree.get_children():
                self.my_tree.delete(data)

            for result in self.reverse(self.read_positions()):
                self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=(result[0], result[1]),
                                    tag="orow")

            self.my_tree.tag_configure('orow', background='#EEEEEE')
            self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def delete_position(self, data):
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

    def crud_jobs(self):
        logging.info(f"{self.current_user} вибрав Crud Jobs")
        self.root = Tk()
        self.root.title("Crud Jobs")
        self.root.geometry("900x300")
        self.my_tree = ttk.Treeview(self.root)

        self.jobTypeInputLabel = Label(self.root, text="Job Type", font=('Arial bold', 15))
        self.jobTypeInputLabel.grid(row=1, column=0, padx=10, pady=10)

        self.entryJobType = Entry(self.root, width=25, bd=5, font=('Arial bold', 15))
        self.entryJobType.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        self.volumeInputLabel = Label(self.root, text="Volume", font=('Arial bold', 15))
        self.volumeInputLabel.grid(row=2, column=0, padx=10, pady=10)

        self.entryVolume = Entry(self.root, width=25, bd=5, font=('Arial bold', 15))
        self.entryVolume.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        self.equipmentTypeInputLabel = Label(self.root, text="Equipment Type", font=('Arial bold', 15))
        self.equipmentTypeInputLabel.grid(row=3, column=0, padx=10, pady=10)

        self.entryEquipmentType = Entry(self.root, width=25, bd=5, font=('Arial bold', 15))
        self.entryEquipmentType.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

        self.executionDateInputLabel = Label(self.root, text="Execution Date", font=('Arial bold', 15))
        self.executionDateInputLabel.grid(row=4, column=0, padx=10, pady=10)

        self.entryExecutionDate = Entry(self.root, width=25, bd=5, font=('Arial bold', 15))
        self.entryExecutionDate.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

        self.fuelConsumptionInputLabel = Label(self.root, text="Fuel Consumption", font=('Arial bold', 15))
        self.fuelConsumptionInputLabel.grid(row=5, column=0, padx=10, pady=10)

        self.entryFuelConsumption = Entry(self.root, width=25, bd=5, font=('Arial bold', 15))
        self.entryFuelConsumption.grid(row=5, column=1, columnspan=3, padx=5, pady=5)

        self.buttonEnter = Button(
            self.root, text="Додати", padx=5, pady=5, width=5,
            bd=3, font=('Arial', 15), bg="#0099ff", command=self.insert_data_job)
        self.buttonEnter.grid(row=6, column=1, columnspan=1)

        self.buttonUpdate = Button(
            self.root, text="Оновити", padx=5, pady=5, width=8,
            bd=3, font=('Arial', 15), bg="#ffff00", command=self.update_data_job)
        self.buttonUpdate.grid(row=6, column=2, columnspan=1)

        self.buttonDelete = Button(
            self.root, text="Видалити", padx=5, pady=5, width=8,
            bd=3, font=('Arial', 15), bg="#e62e00", command=self.delete_data_job)
        self.buttonDelete.grid(row=6, column=3, columnspan=1)

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=('Arial bold', 15))

        self.my_tree['columns'] = ("ID", "JobType", "Volume", "EquipmentType", "ExecutionDate", "FuelConsumption")
        self.my_tree.column("#0", width=0, stretch='NO')
        self.my_tree.column("ID", anchor='w', width=100)
        self.my_tree.column("JobType", anchor='w', width=150)
        self.my_tree.column("Volume", anchor='w', width=100)
        self.my_tree.column("EquipmentType", anchor='w', width=150)
        self.my_tree.column("ExecutionDate", anchor='w', width=150)
        self.my_tree.column("FuelConsumption", anchor='w', width=150)
        self.my_tree.heading("ID", text="ID", anchor='w')
        self.my_tree.heading("JobType", text="Job Type", anchor='w')
        self.my_tree.heading("Volume", text="Volume", anchor='w')
        self.my_tree.heading("EquipmentType", text="Equipment Type", anchor='w')
        self.my_tree.heading("ExecutionDate", text="Execution Date", anchor='w')
        self.my_tree.heading("FuelConsumption", text="Fuel Consumption", anchor='w')

        for data in self.my_tree.get_children():
            self.my_tree.delete(data)

        for result in self.reverse(self.read_jobs()):
            self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[0:])

        self.my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
        self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

        # Создание и привязка вертикального скроллбара к таблице
        scrollbar_y = Scrollbar(self.root, orient="vertical", command=self.my_tree.yview)
        scrollbar_y.grid(row=1, column=9, rowspan=5, sticky="ns")
        self.my_tree.configure(yscrollcommand=scrollbar_y.set)

        # Создание и привязка горизонтального скроллбара к таблице
        scrollbar_x = Scrollbar(self.root, orient="horizontal", command=self.my_tree.xview)
        scrollbar_x.grid(row=6, column=5, columnspan=4, sticky="ew")
        self.my_tree.configure(xscrollcommand=scrollbar_x.set)

        self.root.mainloop()

    def update_job(self, job_type, volume, equipment_type, execution_date, fuel_consumption, job_id):
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="3Ey6x+eQ",
            database="farming"
        )
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS 
            Jobs(JobId INT PRIMARY KEY, JobType VARCHAR(50), Volume INT, 
            EquipmentType VARCHAR(50), ExecutionDate DATE, FuelConsumption FLOAT)""")

        cursor.execute(
            "UPDATE Jobs SET JobType = %s, Volume = %s, EquipmentType = %s, ExecutionDate = %s, FuelConsumption = %s WHERE JobId = %s",
            (job_type, volume, equipment_type, execution_date, fuel_consumption, job_id))
        conn.commit()
        conn.close()

    def update_data_job(self):
        logging.info(f"{self.current_user} вибрав update jobs")
        selected_items = self.my_tree.selection()
        if selected_items:
            self.selected_item = selected_items[0]
            self.update_job_id = self.my_tree.item(self.selected_item)['values'][0]
            self.update_job(self.entryJobType.get(), self.entryVolume.get(),
                            self.entryEquipmentType.get(), self.entryExecutionDate.get(),
                            self.entryFuelConsumption.get(), self.update_job_id)

            for data in self.my_tree.get_children():
                self.my_tree.delete(data)

            for result in self.reverse(self.read_jobs()):
                self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[0:])

            self.my_tree.tag_configure('orow', background='#EEEEEE')
            self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def read_jobs(self):
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="3Ey6x+eQ",
            database="farming"
        )
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS 
            Jobs(JobId INT PRIMARY KEY, JobType VARCHAR(50), Volume INT, 
            EquipmentType VARCHAR(50), ExecutionDate DATE, FuelConsumption FLOAT)""")

        cursor.execute("SELECT * FROM Jobs")
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

    def insert_job(self, job_type, volume, equipment_type, execution_date, fuel_consumption):
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="3Ey6x+eQ",
            database="farming"
        )
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Jobs (JobType, Volume, EquipmentType, ExecutionDate, FuelConsumption) VALUES (%s, %s, %s, %s, %s)",
            (job_type, volume, equipment_type, execution_date, fuel_consumption))
        conn.commit()
        conn.close()

    def insert_data_job(self):
        logging.info(f"{self.current_user} вибрав insert jobs")
        job_type = str(self.entryJobType.get())
        volume = int(self.entryVolume.get())
        equipment_type = str(self.entryEquipmentType.get())
        execution_date = str(self.entryExecutionDate.get())
        fuel_consumption = float(self.entryFuelConsumption.get())

        if job_type and volume and equipment_type and execution_date and fuel_consumption:
            self.insert_job(job_type, volume, equipment_type, execution_date, fuel_consumption)

            for data in self.my_tree.get_children():
                self.my_tree.delete(data)

            for result in self.reverse(self.read_jobs()):
                self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[0:])

            self.my_tree.tag_configure('orow', background='#EEEEEE')
            self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

        else:
            pass

    def delete_data_job(self):
        logging.info(f"{self.current_user} вибрав delete jobs")
        selected_items = self.my_tree.selection()
        if selected_items:
            self.selected_item = selected_items[0]
            self.deleteData = self.my_tree.item(self.selected_item)['values'][0]
            self.delete_job(self.deleteData)

            for data in self.my_tree.get_children():
                self.my_tree.delete(data)

            for result in self.reverse(self.read_jobs()):
                self.my_tree.insert(parent='', index='end', iid=result[0], text="", values=result[0:])

            self.my_tree.tag_configure('orow', background='#EEEEEE')
            self.my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)

    def delete_job(self, job_id):
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="3Ey6x+eQ",
            database="farming"
        )
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS 
            Jobs(JobId INT PRIMARY KEY, JobType VARCHAR(50), Volume INT, 
            EquipmentType VARCHAR(50), ExecutionDate DATE, FuelConsumption FLOAT)""")

        cursor.execute("DELETE FROM Jobs WHERE JobId = %s", (job_id,))
        conn.commit()
        conn.close()

    def crud_employees(self):
        logging.info(f"{self.current_user} вибрав Crud Employees")
        self.root = Tk()
        self.root.title("Crud Employees")
        self.root.geometry("600x445")

        self.labelFirstName = Label(self.root, text="First Name:", font=('Arial', 15))
        self.labelFirstName.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryFirstName = Entry(self.root, font=('Arial', 15))
        self.entryFirstName.grid(row=0, column=1, padx=10, pady=10)

        self.labelLastName = Label(self.root, text="Last Name:", font=('Arial', 15))
        self.labelLastName.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryLastName = Entry(self.root, font=('Arial', 15))
        self.entryLastName.grid(row=1, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_employees)
        self.buttonAdd.grid(row=3, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_employees)
        self.buttonUpdate.grid(row=3, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_employees)
        self.buttonDelete.grid(row=3, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root,
                                 columns=('EmployeeId', 'FirstName', 'LastName', 'ExtraInfo', 'PositionId', 'JobId'))
        self.treeview.grid(row=4, column=0, columnspan=3, padx=0, pady=10)  # Изменили значение padx на 0
        self.treeview.heading('EmployeeId', text='Employee ID')
        self.treeview.heading('FirstName', text='First Name')
        self.treeview.heading('LastName', text='Last Name')
        self.treeview.heading('ExtraInfo', text='Extra Info')
        self.treeview.heading('PositionId', text='Position ID')
        self.treeview.heading('JobId', text='Job ID')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('EmployeeId', width=100)
        self.treeview.column('FirstName', width=100)
        self.treeview.column('LastName', width=100)
        self.treeview.column('ExtraInfo', width=100)
        self.treeview.column('PositionId', width=100)
        self.treeview.column('JobId', width=100)

        self.read_employees()

    def read_employees(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute(
            "SELECT Employees.EmployeeId, Employees.FirstName, Employees.LastName, Employees.ExtraInfo, Positions.PositionId, Jobs.JobId FROM Employees LEFT JOIN Positions ON Employees.PositionId = Positions.PositionId LEFT JOIN Jobs ON Employees.JobId = Jobs.JobId")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        cursor.close()
        db.close()

    def insert_employees(self):
        logging.info(f"{self.current_user} вибрав insert employees")
        first_name = self.entryFirstName.get()
        last_name = self.entryLastName.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("INSERT INTO Employees (FirstName, LastName) VALUES (%s, %s)",
                       (first_name, last_name))
        db.commit()
        cursor.close()
        db.close()
        self.read_employees()

    def update_employees(self):
        logging.info(f"{self.current_user} вибрав update employees")
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            employee_id = item_values[0]
            first_name = self.entryFirstName.get()
            last_name = self.entryLastName.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("UPDATE Employees SET FirstName = %s, LastName = %s WHERE EmployeeId = %s",
                           (first_name, last_name, employee_id))
            db.commit()
            cursor.close()
            db.close()
            self.read_employees()

    def delete_employees(self):
        logging.info(f"{self.current_user} вибрав delete employees")
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            employee_id = item_values[0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM Employees WHERE EmployeeId = %s", employee_id)
            db.commit()
            cursor.close()
            db.close()
            self.read_employees()

    def crud_agriculture_cultures(self):
        logging.info(f"{self.current_user} вибрав Crud Agriculture")
        self.root = Tk()
        self.root.title("Crud Agricultures")
        self.root.geometry("800x565")

        self.labelCultureName = Label(self.root, text="Culture Name:", font=('Arial', 15))
        self.labelCultureName.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryCultureName = Entry(self.root, font=('Arial', 15))
        self.entryCultureName.grid(row=0, column=1, padx=10, pady=10)

        self.labelRipeningTime = Label(self.root, text="Ripening Time:", font=('Arial', 15))
        self.labelRipeningTime.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryRipeningTime = Entry(self.root, font=('Arial', 15))
        self.entryRipeningTime.grid(row=1, column=1, padx=10, pady=10)

        self.labelPlantedArea = Label(self.root, text="Planted Area:", font=('Arial', 15))
        self.labelPlantedArea.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryPlantedArea = Entry(self.root, font=('Arial', 15))
        self.entryPlantedArea.grid(row=2, column=1, padx=10, pady=10)

        self.labelPlantingDate = Label(self.root, text="Planting Date:", font=('Arial', 15))
        self.labelPlantingDate.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryPlantingDate = Entry(self.root, font=('Arial', 15))
        self.entryPlantingDate.grid(row=3, column=1, padx=10, pady=10)

        self.labelFieldNumber = Label(self.root, text="Field Number:", font=('Arial', 15))
        self.labelFieldNumber.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        self.entryFieldNumber = Entry(self.root, font=('Arial', 15))
        self.entryFieldNumber.grid(row=4, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_cultures)
        self.buttonAdd.grid(row=6, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_cultures)
        self.buttonUpdate.grid(row=6, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_cultures)
        self.buttonDelete.grid(row=6, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root,
                                 columns=('AgricultureCultureId', 'Name', 'RipeningTime', 'PlantedArea',
                                          'PlantingDate', 'FieldNumber', 'JobId', 'EmployeeId'))
        self.treeview.grid(row=7, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('AgricultureCultureId', text='Culture ID')
        self.treeview.heading('Name', text='Culture Name')
        self.treeview.heading('RipeningTime', text='Ripening Time')
        self.treeview.heading('PlantedArea', text='Planted Area')
        self.treeview.heading('PlantingDate', text='Planting Date')
        self.treeview.heading('FieldNumber', text='Field Number')
        self.treeview.heading('JobId', text='Job ID')
        self.treeview.heading('EmployeeId', text='Employee ID')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('AgricultureCultureId', width=100)
        self.treeview.column('Name', width=100)
        self.treeview.column('RipeningTime', width=100)
        self.treeview.column('PlantedArea', width=100)
        self.treeview.column('PlantingDate', width=100)
        self.treeview.column('FieldNumber', width=100)
        self.treeview.column('JobId', width=100)
        self.treeview.column('EmployeeId', width=100)

        self.read_cultures()

    def read_cultures(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute(
            "SELECT AgricultureCultureId, Name, RipeningTime, PlantedArea, PlantingDate, FieldNumber, JobId, EmployeeId FROM AgricultureCultures")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        cursor.close()
        db.close()

    def insert_cultures(self):
        logging.info(f"{self.current_user} вибрав insert agriculture")
        culture_name = self.entryCultureName.get()
        ripening_time = self.entryRipeningTime.get()
        planted_area = self.entryPlantedArea.get()
        planting_date = self.entryPlantingDate.get()
        field_number = self.entryFieldNumber.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO AgricultureCultures (Name, RipeningTime, PlantedArea, PlantingDate, FieldNumber) VALUES (%s, %s, %s, %s, %s)",
            (culture_name, ripening_time, planted_area, planting_date, field_number))
        db.commit()
        cursor.close()
        db.close()
        self.read_cultures()

    def update_cultures(self):
        logging.info(f"{self.current_user} вибрав update agriculture")
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            culture_id = item_values[0]
            culture_name = self.entryCultureName.get()
            ripening_time = self.entryRipeningTime.get()
            planted_area = self.entryPlantedArea.get()
            planting_date = self.entryPlantingDate.get()
            field_number = self.entryFieldNumber.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute(
                "UPDATE AgricultureCultures SET Name = %s, RipeningTime = %s, PlantedArea = %s, PlantingDate = %s, FieldNumber = %s WHERE AgricultureCultureId = %s",
                (culture_name, ripening_time, planted_area, planting_date, field_number, culture_id))
            db.commit()
            cursor.close()
            db.close()
            self.read_cultures()

    def delete_cultures(self):
        logging.info(f"{self.current_user} вибрав delete agriculture")
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            culture_id = item_values[0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM AgricultureCultures WHERE AgricultureCultureId = %s", culture_id)
            db.commit()
            cursor.close()
            db.close()
            self.read_cultures()

    def crud_clents(self):
        logging.info(f"{self.current_user} вибрав Crud Clients")
        self.root = Tk()
        self.root.title("Crud Clients")
        self.root.geometry("490x420")  # Изменение размера окна

        self.labelFirstName = Label(self.root, text="First Name:", font=('Arial', 15))
        self.labelFirstName.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryFirstName = Entry(self.root, font=('Arial', 15))
        self.entryFirstName.grid(row=0, column=1, padx=10, pady=10)

        self.labelLastName = Label(self.root, text="Last Name:", font=('Arial', 15))
        self.labelLastName.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryLastName = Entry(self.root, font=('Arial', 15))
        self.entryLastName.grid(row=1, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_client)
        self.buttonAdd.grid(row=2, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_client)
        self.buttonUpdate.grid(row=2, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_client)
        self.buttonDelete.grid(row=2, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('ClientId', 'FirstName', 'LastName'))
        self.treeview.grid(row=3, column=0, columnspan=3, padx=10, pady=10,
                           sticky=(N, S, E, W))  # Изменение размеров и положения Treeview

        self.treeview.heading('ClientId', text='Client ID')
        self.treeview.heading('FirstName', text='First Name')
        self.treeview.heading('LastName', text='Last Name')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('ClientId', width=100)
        self.treeview.column('FirstName', width=150)  # Изменение ширины столбца
        self.treeview.column('LastName', width=150)  # Изменение ширины столбца

        self.treeview.grid_rowconfigure(0, weight=1)  # Растягивание строк Treeview
        self.treeview.grid_columnconfigure(0, weight=1)  # Растягивание столбцов Treeview

        self.read_clients()

    def read_clients(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("SELECT ClientId, FirstName, LastName FROM Clients")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        cursor.close()
        db.close()

    def insert_client(self):
        logging.info(f"{self.current_user} вибрав insert client")
        first_name = self.entryFirstName.get()
        last_name = self.entryLastName.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("INSERT INTO Clients (FirstName, LastName) VALUES (%s, %s)", (first_name, last_name))
        db.commit()
        cursor.close()
        db.close()
        self.read_clients()

    def update_client(self):
        logging.info(f"{self.current_user} вибрав update client")
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            client_id = item_values[0]
            first_name = self.entryFirstName.get()
            last_name = self.entryLastName.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("UPDATE Clients SET FirstName = %s, LastName = %s WHERE ClientId = %s",
                           (first_name, last_name, client_id))
            db.commit()
            cursor.close()
            db.close()
            self.read_clients()

    def delete_client(self):
        logging.info(f"{self.current_user} вибрав delete client")
        selected_item = self.treeview.selection()
        if selected_item:
            item_values = self.treeview.item(selected_item)['values']
            client_id = item_values[0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM Clients WHERE ClientId = %s", client_id)
            db.commit()
            cursor.close()
            db.close()
            self.read_clients()

    def crud_sales(self):
        logging.info(f"{self.current_user} вибрав Crud Sales")
        self.root = Tk()
        self.root.title("Crud Sales")
        self.root.geometry("500x465")

        self.labelQuantity = Label(self.root, text="Quantity:", font=('Arial', 15))
        self.labelQuantity.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryQuantity = Entry(self.root, font=('Arial', 15))
        self.entryQuantity.grid(row=0, column=1, padx=10, pady=10)

        self.labelUnitPrice = Label(self.root, text="Unit Price:", font=('Arial', 15))
        self.labelUnitPrice.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryUnitPrice = Entry(self.root, font=('Arial', 15))
        self.entryUnitPrice.grid(row=1, column=1, padx=10, pady=10)

        self.labelSaleDate = Label(self.root, text="Sale Date:", font=('Arial', 15))
        self.labelSaleDate.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entrySaleDate = Entry(self.root, font=('Arial', 15))
        self.entrySaleDate.grid(row=2, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_sale)
        self.buttonAdd.grid(row=5, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_sale)
        self.buttonUpdate.grid(row=5, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_sale)
        self.buttonDelete.grid(row=5, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('SaleId', 'Quantity', 'UnitPrice', 'SaleDate', 'ClientId'))
        self.treeview.grid(row=6, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('SaleId', text='Sale ID')
        self.treeview.heading('Quantity', text='Quantity')
        self.treeview.heading('UnitPrice', text='Unit Price')
        self.treeview.heading('SaleDate', text='Sale Date')
        self.treeview.heading('ClientId', text='Client ID')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('SaleId', width=100)
        self.treeview.column('Quantity', width=100)
        self.treeview.column('UnitPrice', width=100)
        self.treeview.column('SaleDate', width=100)
        self.treeview.column('ClientId', width=100)

        self.read_sales()
        self.root.mainloop()

    def read_sales(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_sale(self):
        logging.info(f"{self.current_user} вибрав insert sale")
        quantity = self.entryQuantity.get()
        unit_price = self.entryUnitPrice.get()
        sale_date = self.entrySaleDate.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("INSERT INTO sales (Quantity, UnitPrice, SaleDate) VALUES (%s, %s, %s)",
                       (quantity, unit_price, sale_date))
        db.commit()
        db.close()
        self.read_sales()

    def update_sale(self):
        logging.info(f"{self.current_user} вибрав update sale")
        selected_item = self.treeview.selection()
        if selected_item:
            sale_id = self.treeview.item(selected_item)["values"][0]
            quantity = self.entryQuantity.get()
            unit_price = self.entryUnitPrice.get()
            sale_date = self.entrySaleDate.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("UPDATE sales SET Quantity=%s, UnitPrice=%s, SaleDate=%s WHERE SaleId=%s",
                           (quantity, unit_price, sale_date, sale_id))
            db.commit()
            db.close()
            self.read_sales()

    def delete_sale(self):
        logging.info(f"{self.current_user} вибрав delete sale")
        selected_item = self.treeview.selection()
        if selected_item:
            sale_id = self.treeview.item(selected_item)["values"][0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM sales WHERE SaleId=%s", sale_id)
            db.commit()
            db.close()
            self.read_sales()

    def crud_products(self):
        logging.info(f"{self.current_user} вибрав Crud Products")
        self.root = Tk()
        self.root.title("Crud Products")
        self.root.geometry("500x365")

        self.labelName = Label(self.root, text="Name:", font=('Arial', 15))
        self.labelName.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryName = Entry(self.root, font=('Arial', 15))
        self.entryName.grid(row=0, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_product)
        self.buttonAdd.grid(row=5, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_product)
        self.buttonUpdate.grid(row=5, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_product)
        self.buttonDelete.grid(row=5, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('ProductId', 'Name', 'SaleId'))
        self.treeview.grid(row=6, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('ProductId', text='Product ID')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('SaleId', text='Sale ID')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('ProductId', width=100)
        self.treeview.column('Name', width=200)
        self.treeview.column('SaleId', width=100)

        self.read_products()
        self.root.mainloop()

    def read_products(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_product(self):
        logging.info(f"{self.current_user} вибрав insert product")
        name = self.entryName.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("INSERT INTO products (Name) VALUES (%s)", (name,))

        db.commit()
        db.close()
        self.read_products()

    def update_product(self):
        logging.info(f"{self.current_user} вибрав update product")
        selected_item = self.treeview.selection()
        if selected_item:
            product_id = self.treeview.item(selected_item)["values"][0]
            name = self.entryName.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()

            # Получить текущее значение SaleId из базы данных
            cursor.execute("SELECT SaleId FROM Products WHERE ProductId=%s", (product_id,))
            result = cursor.fetchone()
            if result:
                sale_id = result[0]

                # Обновить запись в таблице Products
                cursor.execute("UPDATE Products SET Name=%s, SaleId=%s WHERE ProductId=%s",
                               (name, sale_id, product_id))
                db.commit()
            db.close()
            self.read_products()

    def delete_product(self):
        logging.info(f"{self.current_user} вибрав delete product")
        selected_item = self.treeview.selection()
        if selected_item:
            product_id = self.treeview.item(selected_item)["values"][0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM products WHERE ProductId=%s", product_id)
            db.commit()
            db.close()
            self.read_products()

    def crud_suppliers(self):
        logging.info(f"{self.current_user} вибрав Crud Suppliers")
        self.root = Tk()
        self.root.title("Crud Suppliers")
        self.root.geometry("500x415")

        self.labelFirstName = Label(self.root, text="First Name:", font=('Arial', 15))
        self.labelFirstName.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryFirstName = Entry(self.root, font=('Arial', 15))
        self.entryFirstName.grid(row=0, column=1, padx=10, pady=10)

        self.labelLastName = Label(self.root, text="Last Name:", font=('Arial', 15))
        self.labelLastName.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryLastName = Entry(self.root, font=('Arial', 15))
        self.entryLastName.grid(row=1, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_supplier)
        self.buttonAdd.grid(row=5, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_supplier)
        self.buttonUpdate.grid(row=5, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_supplier)
        self.buttonDelete.grid(row=5, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('SupplierId', 'FirstName', 'LastName'))
        self.treeview.grid(row=6, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('SupplierId', text='Supplier ID')
        self.treeview.heading('FirstName', text='First Name')
        self.treeview.heading('LastName', text='Last Name')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('SupplierId', width=100)
        self.treeview.column('FirstName', width=200)
        self.treeview.column('LastName', width=200)

        self.read_suppliers()
        self.root.mainloop()

    def read_suppliers(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Suppliers")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_supplier(self):
        logging.info(f"{self.current_user} вибрав insert supplier")
        first_name = self.entryFirstName.get()
        last_name = self.entryLastName.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("INSERT INTO Suppliers (FirstName, LastName) VALUES (%s, %s)", (first_name, last_name))
        db.commit()
        db.close()
        self.read_suppliers()

    def update_supplier(self):
        logging.info(f"{self.current_user} вибрав update supplier")
        selected_item = self.treeview.selection()
        if selected_item:
            supplier_id = self.treeview.item(selected_item)["values"][0]
            first_name = self.entryFirstName.get()
            last_name = self.entryLastName.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("UPDATE Suppliers SET FirstName=%s, LastName=%s WHERE SupplierId=%s",
                           (first_name, last_name, supplier_id))
            db.commit()
            db.close()
            self.read_suppliers()

    def delete_supplier(self):
        logging.info(f"{self.current_user} вибрав delete supplier")
        selected_item = self.treeview.selection()
        if selected_item:
            supplier_id = self.treeview.item(selected_item)["values"][0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM Suppliers WHERE SupplierId=%s", supplier_id)
            db.commit()
            db.close()
            self.read_suppliers()

    def crud_supply_fertilizers(self):
        logging.info(f"{self.current_user} вибрав Crud Supply Fertilizers")
        self.root = Tk()
        self.root.title("Crud Supply Fertilizers")
        self.root.geometry("850x510")

        self.labelQuantity = Label(self.root, text="Quantity:", font=('Arial', 15))
        self.labelQuantity.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.entryQuantity = Entry(self.root, font=('Arial', 15))
        self.entryQuantity.grid(row=0, column=1, padx=10, pady=10)

        self.labelDeliveryDate = Label(self.root, text="Delivery Date:", font=('Arial', 15))
        self.labelDeliveryDate.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.entryDeliveryDate = Entry(self.root, font=('Arial', 15))
        self.entryDeliveryDate.grid(row=1, column=1, padx=10, pady=10)

        self.labelDeliveryStatus = Label(self.root, text="Delivery Status:", font=('Arial', 15))
        self.labelDeliveryStatus.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.entryDeliveryStatus = Entry(self.root, font=('Arial', 15))
        self.entryDeliveryStatus.grid(row=2, column=1, padx=10, pady=10)

        self.labelPaymentStatus = Label(self.root, text="Payment Status:", font=('Arial', 15))
        self.labelPaymentStatus.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.entryPaymentStatus = Entry(self.root, font=('Arial', 15))
        self.entryPaymentStatus.grid(row=3, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_supply_fertilizer)
        self.buttonAdd.grid(row=7, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_supply_fertilizer)
        self.buttonUpdate.grid(row=7, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_supply_fertilizer)
        self.buttonDelete.grid(row=7, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=(
            'SupplyId', 'Quantity', 'DeliveryDate', 'DeliveryStatus', 'PaymentStatus', 'SupplierId', 'EmployeeId'))
        self.treeview.grid(row=8, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('SupplyId', text='Supply ID')
        self.treeview.heading('Quantity', text='Quantity')
        self.treeview.heading('DeliveryDate', text='Delivery Date')
        self.treeview.heading('DeliveryStatus', text='Delivery Status')
        self.treeview.heading('PaymentStatus', text='Payment Status')
        self.treeview.heading('SupplierId', text='Supplier ID')
        self.treeview.heading('EmployeeId', text='Employee ID')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('SupplyId', width=100)
        self.treeview.column('Quantity', width=100)
        self.treeview.column('DeliveryDate', width=150)
        self.treeview.column('DeliveryStatus', width=150)
        self.treeview.column('PaymentStatus', width=150)
        self.treeview.column('SupplierId', width=100)
        self.treeview.column('EmployeeId', width=100)

        self.read_supply_fertilizers()
        self.root.mainloop()

    def read_supply_fertilizers(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM SupplyFertilizers")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_supply_fertilizer(self):
        logging.info(f"{self.current_user} вибрав insert supply fertilizers")
        quantity = int(self.entryQuantity.get())
        delivery_date = self.entryDeliveryDate.get()
        delivery_status = self.entryDeliveryStatus.get()
        payment_status = self.entryPaymentStatus.get()
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO SupplyFertilizers (Quantity, DeliveryDate, DeliveryStatus, PaymentStatus) VALUES (%s, %s, %s, %s)",
            (quantity, delivery_date, delivery_status, payment_status))
        db.commit()
        db.close()
        self.read_supply_fertilizers()

    def update_supply_fertilizer(self):
        logging.info(f"{self.current_user} вибрав update supply fertilizers")
        selected_item = self.treeview.selection()
        if selected_item:
            supply_id = self.treeview.item(selected_item)["values"][0]
            quantity = int(self.entryQuantity.get())
            delivery_date = self.entryDeliveryDate.get()
            delivery_status = self.entryDeliveryStatus.get()
            payment_status = self.entryPaymentStatus.get()
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute(
                "UPDATE SupplyFertilizers SET Quantity=%s, DeliveryDate=%s, DeliveryStatus=%s, PaymentStatus=%s WHERE SupplyId=%s",
                (quantity, delivery_date, delivery_status, payment_status, supply_id))
            db.commit()
            db.close()
            self.read_supply_fertilizers()

    def delete_supply_fertilizer(self):
        logging.info(f"{self.current_user} вибрав delete supply fertilizers")
        selected_item = self.treeview.selection()
        if selected_item:
            supply_id = self.treeview.item(selected_item)["values"][0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM SupplyFertilizers WHERE SupplyId=%s", supply_id)
            db.commit()
            db.close()
            self.read_supply_fertilizers()

    def crud_fertilizers(self):
        logging.info(f"{self.current_user} вибрав Crud Fertilizers")
        self.root = Tk()
        self.root.title("Crud Fertilizers")
        self.root.geometry("560x420")

        self.labelName = Label(self.root, text="Name:", font=('Arial', 15))
        self.labelName.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.entryName = Entry(self.root, font=('Arial', 15))
        self.entryName.grid(row=0, column=1, padx=10, pady=10)

        self.labelPricePerBag = Label(self.root, text="Price Per Bag:", font=('Arial', 15))
        self.labelPricePerBag.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.entryPricePerBag = Entry(self.root, font=('Arial', 15))
        self.entryPricePerBag.grid(row=1, column=1, padx=10, pady=10)

        self.buttonAdd = Button(self.root, text="Додати", bg="#0099ff", font=('Arial', 15),
                                command=self.insert_fertilizer)
        self.buttonAdd.grid(row=7, column=0, padx=10, pady=10)

        self.buttonUpdate = Button(self.root, text="Оновити", bg="#ffff00", font=('Arial', 15),
                                   command=self.update_fertilizer)
        self.buttonUpdate.grid(row=7, column=1, padx=10, pady=10)

        self.buttonDelete = Button(self.root, text="Видалити", bg="#e62e00", font=('Arial', 15),
                                   command=self.delete_fertilizer)
        self.buttonDelete.grid(row=7, column=2, padx=10, pady=10)

        self.treeview = Treeview(self.root, columns=('FertilizerId', 'Name', 'PricePerBag', 'SupplyId'))
        self.treeview.grid(row=8, column=0, columnspan=3, padx=0, pady=10)
        self.treeview.heading('FertilizerId', text='Fertilizer ID')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('PricePerBag', text='Price Per Bag')
        self.treeview.heading('SupplyId', text='Supply ID')

        self.treeview.column("#0", width=0, stretch='NO')
        self.treeview.column('FertilizerId', width=100)
        self.treeview.column('Name', width=200)
        self.treeview.column('PricePerBag', width=150)
        self.treeview.column('SupplyId', width=100)

        # Создание и привязка вертикального скроллбара к таблице
        scrollbar = Scrollbar(self.root, orient="vertical", command=self.treeview.yview)
        scrollbar.grid(row=8, column=4, sticky="ns")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.read_fertilizers()
        self.root.mainloop()

    def read_fertilizers(self):
        self.treeview.delete(*self.treeview.get_children())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Fertilizers")
        rows = cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        db.close()

    def insert_fertilizer(self):
        logging.info(f"{self.current_user} вибрав insert fertilizers")
        name = self.entryName.get()
        price_per_bag = float(self.entryPricePerBag.get())
        db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Fertilizers (Name, PricePerBag) VALUES (%s, %s)",
            (name, price_per_bag))
        db.commit()
        db.close()
        self.read_fertilizers()

    def update_fertilizer(self):
        logging.info(f"{self.current_user} вибрав update fertilizers")
        selected_item = self.treeview.selection()
        if selected_item:
            fertilizer_id = self.treeview.item(selected_item)["values"][0]
            name = self.entryName.get()
            price_per_bag = float(self.entryPricePerBag.get())
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute(
                "UPDATE Fertilizers SET Name=%s, PricePerBag=%s WHERE FertilizerId=%s",
                (name, price_per_bag, fertilizer_id))
            db.commit()
            db.close()
            self.read_fertilizers()

    def delete_fertilizer(self):
        logging.info(f"{self.current_user} вибрав delete fertilizers")
        selected_item = self.treeview.selection()
        if selected_item:
            fertilizer_id = self.treeview.item(selected_item)["values"][0]
            db = pymysql.connect(host="localhost", user="root", password="3Ey6x+eQ", database="farming")
            cursor = db.cursor()
            cursor.execute("DELETE FROM Fertilizers WHERE FertilizerId=%s", fertilizer_id)
            db.commit()
            db.close()
            self.read_fertilizers()

    def all_queries(self):
        logging.info(f"{self.current_user} вибрав all_queries")
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Авторизация в базе данных")
        self.root.geometry("700x500")
        self.label_title = tk.Label(self.root, text="Запити до БД", font=("Arial", 14))
        self.label_title.place(x=300, y=0)

        self.label_query1 = tk.Label(self.root, text="1) Cписок товарів та кількість,в якій були продані.",
                                     font=("Arial", 9))
        self.label_query1.place(x=0, y=32)
        self.btn_query1 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query1)
        self.btn_query1.place(x=290, y=30)

        self.label_query2 = tk.Label(self.root, text="2) Список клієнтів та кількість їх закупівель.",
                                     font=("Arial", 9))
        self.label_query2.place(x=0, y=72)
        self.btn_query2 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query2)
        self.btn_query2.place(x=290, y=70)

        self.label_query3 = tk.Label(self.root, text="3) Співробітники, чиє прізвище починається\nна певну літеру.",
                                     font=("Arial", 9))
        self.label_query3.place(x=0, y=112)
        self.btn_query3 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query3)
        self.btn_query3.place(x=290, y=110)

        self.label_query4 = tk.Label(self.root,
                                     text="4) Записи з таблиці 'Product', де назва\nпочинається на певну літеру.",
                                     font=("Arial", 9))
        self.label_query4.place(x=0, y=152)
        self.btn_query4 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query4)
        self.btn_query4.place(x=290, y=150)

        self.label_query5 = tk.Label(self.root,
                                     text="5) Записи з таблиці 'Sales', де дата продажу\nзнаходиться між певним періодом.",
                                     font=("Arial", 9))
        self.label_query5.place(x=0, y=192)
        self.btn_query5 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query5)
        self.btn_query5.place(x=290, y=190)

        self.label_query6 = tk.Label(self.root,
                                     text="6) Записи з таблиці 'Job', де обсяг праці\nзнаходиться у певному діапазоні.",
                                     font=("Arial", 9))
        self.label_query6.place(x=0, y=232)
        self.btn_query6 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query6)
        self.btn_query6.place(x=290, y=230)

        self.label_query7 = tk.Label(self.root,
                                     text="7) Загальна кількість продажів клієнтам з таблиці\n'Sale'.",
                                     font=("Arial", 9))
        self.label_query7.place(x=0, y=272)
        self.btn_query7 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query7)
        self.btn_query7.place(x=290, y=270)

        self.label_query8 = tk.Label(self.root,
                                     text="8) Кількість клієнтів, які здійснили покупки у\nпевну дату.",
                                     font=("Arial", 9))
        self.label_query8.place(x=0, y=312)
        self.btn_query8 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query8)
        self.btn_query8.place(x=290, y=310)

        self.label_query9 = tk.Label(self.root,
                                     text="9) Кількість працівників на кожній з посад.",
                                     font=("Arial", 9))
        self.label_query9.place(x=0, y=342)
        self.btn_query9 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query9)
        self.btn_query9.place(x=290, y=340)

        self.label_query10 = tk.Label(self.root,
                                      text="10) Кількість товарів, яка була продана кожному\n клієнту.",
                                      font=("Arial", 9))
        self.label_query10.place(x=0, y=382)
        self.btn_query10 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query10)
        self.btn_query10.place(x=290, y=380)

        self.label_query11 = tk.Label(self.root, text="11) Працівник, який має найбільший об'єм роботи.",
                                      font=("Arial", 9))
        self.label_query11.place(x=350, y=32)
        self.btn_query11 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query11)
        self.btn_query11.place(x=640, y=30)

        self.label_query12 = tk.Label(self.root,
                                      text="12) Хто з постачальників має поставку з\nнайбільшою кількістю товарів?",
                                      font=("Arial", 9))
        self.label_query12.place(x=350, y=72)
        self.btn_query12 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query12)
        self.btn_query12.place(x=640, y=70)

        self.label_query13 = tk.Label(self.root,
                                      text="13) Клієнти, які зробили закупівлю з кількістю\nтовару більше 10.",
                                      font=("Arial", 9))
        self.label_query13.place(x=350, y=112)
        self.btn_query13 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query13)
        self.btn_query13.place(x=640, y=110)

        self.label_query14 = tk.Label(self.root,
                                      text="14) Список посад та кількість співробітників, які\nзаймають ці посади.",
                                      font=("Arial", 9))
        self.label_query14.place(x=350, y=152)
        self.btn_query14 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query14)
        self.btn_query14.place(x=640, y=150)

        self.label_query15 = tk.Label(self.root,
                                      text="15) Список працівників, які не організували жодну\nпоставку.",
                                      font=("Arial", 9))
        self.label_query15.place(x=350, y=192)
        self.btn_query15 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query15)
        self.btn_query15.place(x=640, y=190)

        self.label_query16 = tk.Label(self.root,
                                      text="16) Вибірка постачальників, які не постачали\nдобриво з певною назвою.",
                                      font=("Arial", 9))
        self.label_query16.place(x=350, y=232)
        self.btn_query16 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query16)
        self.btn_query16.place(x=640, y=230)

        self.label_query17 = tk.Label(self.root,
                                      text="17) Список посад з коментарем «Має найбільшу\nкількість працівників», «Має найменшу\nкількість працівників».",
                                      font=("Arial", 9))
        self.label_query17.place(x=350, y=272)
        self.btn_query17 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query17)
        self.btn_query17.place(x=640, y=280)

        self.label_query18 = tk.Label(self.root,
                                      text="18) Список працівників з коментарем «Відповідає\nза найбільшу кількість організованих продажів»,\n«Не відповідає за жоден продаж».",
                                      font=("Arial", 9))
        self.label_query18.place(x=350, y=332)
        self.btn_query18 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query18)
        self.btn_query18.place(x=640, y=345)

        self.label_query19 = tk.Label(self.root,
                                      text="19) У поле ExtraInfo в таблиці Employees,\nзаписати «Зробив найбільшу кількість продажів».",
                                      font=("Arial", 9))
        self.label_query19.place(x=350, y=390)
        self.btn_query19 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query19)
        self.btn_query19.place(x=640, y=400)

        self.label_query20 = tk.Label(self.root,
                                      text="20) У поле ExtraInfo в таблиці Employees,\nзаписати «Зробив найменшу кількість продажів».",
                                      font=("Arial", 9))
        self.label_query20.place(x=350, y=430)
        self.btn_query20 = tk.Button(self.root, text="Запуск", font=("Arial", 9), command=self.query20)
        self.btn_query20.place(x=640, y=440)

        self.root.mainloop()

    def query1(self):
        logging.info(f"{self.current_user} вибрав query1")
        self.query1 = tk.Tk()
        self.query1.title("Запит №1")
        self.query1.geometry("400x300")

        self.label_title_q1 = tk.Label(self.query1,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q1.pack()

        # определяем столбцы
        self.columns = ("Name", "TotalQuantity")

        self.tree = ttk.Treeview(self.query1, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("Name", text="Назва", anchor=W)
        self.tree.heading("TotalQuantity", text="Кількість", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT p.Name, SUM(s.Quantity) AS TotalQuantity FROM Products p JOIN Sales s ON p.SaleId = s.SaleId GROUP BY p.Name ORDER BY TotalQuantity DESC;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["Name"], row["TotalQuantity"]))

        self.query1.mainloop()

    def query2(self):
        logging.info(f"{self.current_user} вибрав query2")
        self.query2 = tk.Tk()
        self.query2.title("Запит №2")
        self.query2.geometry("400x300")

        self.label_title_q2 = tk.Label(self.query2,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q2.pack()

        # определяем столбцы
        self.columns = ("FirstName", "LastName", "OrderCount")

        self.tree = ttk.Treeview(self.query2, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)
        self.tree.heading("OrderCount", text="Кількість закупівель", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)
        self.tree.column("#3", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT c.FirstName, c.LastName, COUNT(s.SaleId) AS OrderCount FROM Clients c " \
                    "LEFT JOIN Sales s ON c.ClientId = s.ClientId GROUP BY c.ClientId ORDER BY OrderCount ASC;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", END, values=(row["FirstName"], row["LastName"], row["OrderCount"]))

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query2, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query2, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query2.mainloop()

    def query3(self):
        logging.info(f"{self.current_user} вибрав query3")
        self.query3 = tk.Tk()
        self.query3.title("Запит №3")
        self.query3.geometry("300x200")

        self.label_title_q3 = tk.Label(self.query3, text="Введіть літеру:", font=("Arial", 13))
        self.label_title_q3.place(x=90, y=30)

        self.entry_sign = tk.Entry(self.query3)
        self.entry_sign.place(x=90, y=60)

        self.button_apply = tk.Button(self.query3, text="Застосувати", command=self.apply_query3)
        self.button_apply.place(x=115, y=90)

        self.query3.mainloop()

    def apply_query3(self):
        sign = self.entry_sign.get()

        self.query3.destroy()

        self.query3_results = tk.Tk()
        self.query3_results.title("Запит №3 - Результати")
        self.query3_results.geometry("400x300")

        # определяем столбцы
        columns = ("EmployeeId", "FirstName", "LastName", "PositionId", "JobId")

        tree = ttk.Treeview(self.query3_results, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        tree.heading("EmployeeId", text="Айді працівника", anchor=W)
        tree.heading("FirstName", text="Ім'я", anchor=W)
        tree.heading("LastName", text="Прізвище", anchor=W)
        tree.heading("PositionId", text="Айді посади", anchor=W)
        tree.heading("JobId", text="Айді праці", anchor=W)

        # настраиваем столбцы
        tree.column("#1", stretch=NO, width=180)
        tree.column("#2", stretch=NO, width=180)
        tree.column("#3", stretch=NO, width=180)
        tree.column("#4", stretch=NO, width=180)
        tree.column("#5", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = f"SELECT * FROM Employees WHERE LastName LIKE '{sign}%'"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (row["EmployeeId"], row["FirstName"], row["LastName"], row["PositionId"], row["JobId"])
            tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query3_results, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query3_results, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query3_results.mainloop()

    def query4(self):
        logging.info(f"{self.current_user} вибрав query4")
        self.query4 = tk.Tk()
        self.query4.title("Запит №4")
        self.query4.geometry("300x200")

        self.label_title_q4 = tk.Label(self.query4, text="Введіть літеру:", font=("Arial", 13))
        self.label_title_q4.place(x=90, y=30)

        self.entry_sign = tk.Entry(self.query4)
        self.entry_sign.place(x=90, y=60)

        self.button_apply = tk.Button(self.query4, text="Застосувати", command=self.apply_query4)
        self.button_apply.place(x=115, y=90)

        self.query4.mainloop()

    def apply_query4(self):
        sign = self.entry_sign.get()

        self.query4.destroy()

        self.query4_results = tk.Tk()
        self.query4_results.title("Запит №4 - Результати")
        self.query4_results.geometry("400x300")

        # определяем столбцы
        columns = ("ProductId", "Name", "SaleId")

        tree = ttk.Treeview(self.query4_results, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        tree.heading("ProductId", text="Айді товару", anchor=W)
        tree.heading("Name", text="Ім'я", anchor=W)
        tree.heading("SaleId", text="Айді продажу", anchor=W)

        # настраиваем столбцы
        tree.column("#1", stretch=NO, width=180)
        tree.column("#2", stretch=NO, width=180)
        tree.column("#3", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = f"SELECT * FROM Products WHERE Name LIKE '{sign}%';"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (row["ProductId"], row["Name"], row["SaleId"])
            tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query4_results, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query4_results, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query4_results.mainloop()

    def query5(self):
        logging.info(f"{self.current_user} вибрав query5")
        self.query5_input = tk.Tk()
        self.query5_input.title("Запит №5 - Введення періоду")
        self.query5_input.geometry("300x200")

        self.label_title_q5 = tk.Label(self.query5_input, text="Введіть період", font=("Arial", 13))
        self.label_title_q5.place(x=90, y=30)

        self.label_from = tk.Label(self.query5_input, text="З:", font=("Arial", 12))
        self.label_from.place(x=50, y=70)
        self.entry_from = tk.Entry(self.query5_input)
        self.entry_from.place(x=90, y=70)

        self.label_to = tk.Label(self.query5_input, text="По:", font=("Arial", 12))
        self.label_to.place(x=50, y=100)
        self.entry_to = tk.Entry(self.query5_input)
        self.entry_to.place(x=90, y=100)

        self.button_apply = tk.Button(self.query5_input, text="Застосувати", command=self.apply_query5)
        self.button_apply.place(x=115, y=130)

        self.query5_input.mainloop()

    def apply_query5(self):
        date_from = self.entry_from.get()
        date_to = self.entry_to.get()

        self.query5_input.destroy()

        self.query5_results = tk.Tk()
        self.query5_results.title("Запит №5 - Результати")
        self.query5_results.geometry("400x300")

        # определяем столбцы
        columns = ("SaleId", "Quantity", "UnitPrice", "SaleDate", "ClientId", "EmployeeId")

        tree = ttk.Treeview(self.query5_results, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        tree.heading("SaleId", text="Айді продажу", anchor=W)
        tree.heading("Quantity", text="Кількість", anchor=W)
        tree.heading("UnitPrice", text="Ціна одиниці товару", anchor=W)
        tree.heading("SaleDate", text="Дата продажу", anchor=W)
        tree.heading("ClientId", text="Айді клієнта", anchor=W)
        tree.heading("EmployeeId", text="Айді працівника", anchor=W)

        # настраиваем столбцы
        tree.column("#1", stretch=NO, width=180)
        tree.column("#2", stretch=NO, width=180)
        tree.column("#3", stretch=NO, width=180)
        tree.column("#4", stretch=NO, width=180)
        tree.column("#5", stretch=NO, width=180)
        tree.column("#6", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = f"SELECT * FROM Sales WHERE SaleDate BETWEEN '{date_from}' AND '{date_to}';"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["SaleId"], row["Quantity"], row["UnitPrice"], row["SaleDate"], row["ClientId"], row["EmployeeId"])
            tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query5_results, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query5_results, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query5_results.mainloop()

    def query6(self):
        logging.info(f"{self.current_user} вибрав query6")
        self.query6_input = tk.Tk()
        self.query6_input.title("Запит №6 - Введення діапазону")
        self.query6_input.geometry("300x200")

        self.label_title_q6 = tk.Label(self.query6_input, text="Введіть діапазон", font=("Arial", 13))
        self.label_title_q6.place(x=90, y=30)

        self.label_from = tk.Label(self.query6_input, text="Від:", font=("Arial", 12))
        self.label_from.place(x=50, y=70)
        self.entry_from = tk.Entry(self.query6_input)
        self.entry_from.place(x=90, y=70)

        self.label_to = tk.Label(self.query6_input, text="До:", font=("Arial", 12))
        self.label_to.place(x=50, y=100)
        self.entry_to = tk.Entry(self.query6_input)
        self.entry_to.place(x=90, y=100)

        self.button_apply = tk.Button(self.query6_input, text="Застосувати", command=self.apply_query6)
        self.button_apply.place(x=115, y=130)

        self.query6_input.mainloop()

    def apply_query6(self):
        range_from = self.entry_from.get()
        range_to = self.entry_to.get()

        self.query6_input.destroy()

        self.query6_results = tk.Tk()
        self.query6_results.title("Запит №6 - Результати")
        self.query6_results.geometry("400x300")

        # определяем столбцы
        columns = ("JobId", "JobType", "Volume", "EquipmentType", "ExecutionDate", "FuelConsumption")

        tree = ttk.Treeview(self.query6_results, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        tree.heading("JobId", text="Айді праці", anchor=W)
        tree.heading("JobType", text="Тип роботи", anchor=W)
        tree.heading("Volume", text="Об'єм праці", anchor=W)
        tree.heading("EquipmentType", text="Тип техніки", anchor=W)
        tree.heading("ExecutionDate", text="Дата виконання", anchor=W)
        tree.heading("FuelConsumption", text="Кількість використаного палива", anchor=W)

        # настраиваем столбцы
        tree.column("#1", stretch=NO, width=180)
        tree.column("#2", stretch=NO, width=180)
        tree.column("#3", stretch=NO, width=180)
        tree.column("#4", stretch=NO, width=180)
        tree.column("#5", stretch=NO, width=180)
        tree.column("#6", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = f"SELECT * FROM Jobs WHERE Volume BETWEEN {range_from} AND {range_to};"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["JobId"], row["JobType"], row["Volume"], row["EquipmentType"], row["ExecutionDate"],
                row["FuelConsumption"])
            tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query6_results, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query6_results, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query6_results.mainloop()

    def query8(self):
        logging.info(f"{self.current_user} вибрав query8")
        self.query8_input = tk.Tk()
        self.query8_input.title("Запит №8 - Введення дати")
        self.query8_input.geometry("300x150")

        self.label_title_q8 = tk.Label(self.query8_input, text="Введіть дату (рік-місяць-день):", font=("Arial", 13))
        self.label_title_q8.place(x=30, y=30)
        self.entry_date = tk.Entry(self.query8_input)
        self.entry_date.place(x=90, y=70)

        self.button_apply = tk.Button(self.query8_input, text="Застосувати", command=self.apply_query8)
        self.button_apply.place(x=115, y=100)

        self.query8_input.mainloop()

    def apply_query8(self):
        date = self.entry_date.get()

        self.query8_input.destroy()

        self.query8_results = tk.Tk()
        self.query8_results.title("Запит №8 - Результати")
        self.query8_results.geometry("400x300")

        # определяем столбцы
        columns = ("TotalClients")

        tree = ttk.Treeview(self.query8_results, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        tree.heading("TotalClients", text="Кількість клієнтів", anchor=W)

        # настраиваем столбцы
        tree.column("#1", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = f"SELECT COUNT(DISTINCT ClientId) AS TotalClients FROM Sales WHERE SaleDate = '{date}';"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (row["TotalClients"])
            tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query8_results, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query8_results, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query8_results.mainloop()

    def query7(self):
        logging.info(f"{self.current_user} вибрав query7")
        self.query7 = tk.Tk()
        self.query7.title("Запит №7")
        self.query7.geometry("400x300")

        self.label_title_q7 = tk.Label(self.query7,
                                       text="Результати запиту",
                                       font=("Arial", 13))
        self.label_title_q7.pack()

        # определяем столбцы
        self.columns = ("TotalSales")

        self.tree = ttk.Treeview(self.query7, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("TotalSales", text="Кількість продажів", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT SUM(Quantity) AS TotalSales FROM Sales;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["TotalSales"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query7, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query7, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query7.mainloop()

    def query9(self):
        logging.info(f"{self.current_user} вибрав query9")
        self.query9 = tk.Tk()
        self.query9.title("Запит №9")
        self.query9.geometry("400x300")

        self.label_title_q9 = tk.Label(self.query9, text="Результати запиту", font=("Arial", 13))
        self.label_title_q9.pack()

        # определяем столбцы
        self.columns = ("PositionId", "TotalEmployees")

        self.tree = ttk.Treeview(self.query9, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("PositionId", text="Айді посади", anchor=W)
        self.tree.heading("TotalEmployees", text="Кількість працівників", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT PositionId, COUNT(*) AS TotalEmployees FROM Employees GROUP BY PositionId;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["PositionId"], row["TotalEmployees"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        self.scrollbar_y = ttk.Scrollbar(self.query9, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        self.scrollbar_x = ttk.Scrollbar(self.query9, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query9, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query9.pdf"))
        self.button_export.pack()
        self.query9.mainloop()

    def query10(self):
        logging.info(f"{self.current_user} вибрав query10")
        self.query10 = tk.Tk()
        self.query10.title("Запит №10")
        self.query10.geometry("400x300")

        self.label_title_q10 = tk.Label(self.query10,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q10.pack()

        # определяем столбцы
        self.columns = ("ClientId", "TotalProductQuantity")

        self.tree = ttk.Treeview(self.query10, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("ClientId", text="Айді клієнта", anchor=W)
        self.tree.heading("TotalProductQuantity", text="Кількість товарів", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT ClientId, SUM(Quantity) AS TotalProductQuantity FROM Sales " \
                    "JOIN Products ON Sales.SaleId = Products.SaleId GROUP BY ClientId;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["ClientId"], row["TotalProductQuantity"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query10, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query10, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query10, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query10.pdf"))
        self.button_export.pack()

        self.query10.mainloop()

    def query11(self):
        logging.info(f"{self.current_user} вибрав query11")
        self.query11 = tk.Tk()
        self.query11.title("Запит №11")
        self.query11.geometry("400x300")

        self.label_title_q11 = tk.Label(self.query11,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q11.pack()

        # определяем столбцы
        self.columns = ("EmployeeId", "FirstName", "LastName")

        self.tree = ttk.Treeview(self.query11, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("EmployeeId", text="Айді працівника", anchor=W)
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)
        self.tree.column("#3", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT e.EmployeeId, e.FirstName, e.LastName FROM Employees e WHERE e.JobId = ALL (SELECT JobId " \
                    "FROM Jobs WHERE Volume = (SELECT MAX(Volume) FROM Jobs));"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["EmployeeId"], row["FirstName"], row["LastName"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query11, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query11, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query11.mainloop()

    def query12(self):
        logging.info(f"{self.current_user} вибрав query12")
        self.query12 = tk.Tk()
        self.query12.title("Запит №12")
        self.query12.geometry("400x300")

        self.label_title_q12 = tk.Label(self.query12,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q12.pack()

        # определяем столбцы
        self.columns = ("SupplierId", "FirstName", "LastName", "Quantity")

        self.tree = ttk.Treeview(self.query12, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("SupplierId", text="Айді постачальника", anchor=W)
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)
        self.tree.heading("Quantity", text="Кількість товарів", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)
        self.tree.column("#3", stretch=NO, width=180)
        self.tree.column("#4", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT s.SupplierId, s.FirstName, s.LastName, sf.Quantity FROM Suppliers s " \
                    "INNER JOIN SupplyFertilizers sf ON s.SupplierId = sf.SupplierId " \
                    "WHERE sf.Quantity >= ALL (SELECT Quantity FROM SupplyFertilizers);"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["SupplierId"], row["FirstName"], row["LastName"], row["Quantity"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query12, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query12, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query12.mainloop()

    def query13(self):
        logging.info(f"{self.current_user} вибрав query13")
        self.query13 = tk.Tk()
        self.query13.title("Запит №13")
        self.query13.geometry("400x300")

        self.label_title_q13 = tk.Label(self.query13,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q13.pack()

        # определяем столбцы
        self.columns = ("FirstName", "LastName")

        self.tree = ttk.Treeview(self.query13, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT c.FirstName, c.LastName FROM Clients c WHERE EXISTS ( SELECT * FROM Sales s " \
                    "WHERE s.ClientId = c.ClientId AND s.Quantity > 5 );"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["FirstName"], row["LastName"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query13, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query13, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query13, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query13.pdf"))
        self.button_export.pack()

        self.query13.mainloop()

    def query14(self):
        logging.info(f"{self.current_user} вибрав query14")
        self.query14 = tk.Tk()
        self.query14.title("Запит №14")
        self.query14.geometry("400x300")

        self.label_title_q14 = tk.Label(self.query14,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q14.pack()

        # определяем столбцы
        self.columns = ("Position", "EmployeeCount")

        self.tree = ttk.Treeview(self.query14, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("Position", text="Посада", anchor=W)
        self.tree.heading("EmployeeCount", text="Кількість працівників", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT p.title AS Position, COUNT(*) AS EmployeeCount FROM Positions p " \
                    "INNER JOIN Employees e ON e.PositionId = p.PositionId GROUP BY p.title;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["Position"], row["EmployeeCount"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query14, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query14, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query14, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query14.pdf"))
        self.button_export.pack()

        self.query14.mainloop()

    def query15(self):
        logging.info(f"{self.current_user} вибрав query15")
        self.query15 = tk.Tk()
        self.query15.title("Запит №15")
        self.query15.geometry("400x300")

        self.label_title_q15 = tk.Label(self.query15,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q15.pack()

        # определяем столбцы
        self.columns = ("FirstName", "LastName")

        self.tree = ttk.Treeview(self.query15, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT e.FirstName, e.LastName FROM Employees e " \
                    "LEFT JOIN SupplyFertilizers sf ON e.EmployeeId = sf.EmployeeId WHERE sf.EmployeeId IS NULL;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["FirstName"], row["LastName"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query15, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query15, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query15.mainloop()

    def query16(self):
        logging.info(f"{self.current_user} вибрав query16")
        self.query16_input = tk.Tk()
        self.query16_input.title("Запит №16 - Введення назви добрива")
        self.query16_input.geometry("300x150")

        self.label_title_q16 = tk.Label(self.query16_input, text="Введіть назву добрива:", font=("Arial", 13))
        self.label_title_q16.place(x=60, y=30)

        self.entry_fertilizer = tk.Entry(self.query16_input)
        self.entry_fertilizer.place(x=90, y=70)

        self.button_apply = tk.Button(self.query16_input, text="Застосувати", command=self.apply_query16)
        self.button_apply.place(x=110, y=100)

        self.query16_input.mainloop()

    def apply_query16(self):
        fertilizer_name = self.entry_fertilizer.get()

        self.query16_input.destroy()

        self.query16_results = tk.Tk()
        self.query16_results.title("Запит №16 - Результати")
        self.query16_results.geometry("400x300")

        # определяем столбцы
        columns = ("SupplierId", "FirstName", "LastName")

        tree = ttk.Treeview(self.query16_results, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        tree.heading("SupplierId", text="Айді постачальника", anchor=W)
        tree.heading("FirstName", text="Ім'я", anchor=W)
        tree.heading("LastName", text="Прізвище", anchor=W)

        # настраиваем столбцы
        tree.column("#1", stretch=NO, width=180)
        tree.column("#2", stretch=NO, width=180)
        tree.column("#3", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = f"SELECT s.SupplierId, s.FirstName, s.LastName FROM Suppliers s " \
                    f"LEFT JOIN SupplyFertilizers sf ON s.SupplierId = sf.SupplierId " \
                    f"LEFT JOIN Fertilizers f ON sf.SupplyId = f.SupplyId " \
                    f"WHERE f.Name <> '{fertilizer_name}' OR f.Name IS NULL;"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (row["SupplierId"], row["FirstName"], row["LastName"])
            tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query16_results, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query16_results, orient=HORIZONTAL, command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query16_results.mainloop()

    def query17(self):
        logging.info(f"{self.current_user} вибрав query17")
        self.query17 = tk.Tk()
        self.query17.title("Запит №17")
        self.query17.geometry("400x300")

        self.label_title_q17 = tk.Label(self.query17,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q17.pack()

        # определяем столбцы
        self.columns = ("title", "comment")

        self.tree = ttk.Treeview(self.query17, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("title", text="Назва", anchor=W)
        self.tree.heading("comment", text="Коментар", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT title, 'Has the largest number of employees' AS comment FROM Positions " \
                    "WHERE PositionId IN ( SELECT PositionId FROM Employees GROUP BY PositionId " \
                    "HAVING COUNT(*) = ( SELECT MAX(emp_count) FROM ( SELECT COUNT(*) AS emp_count FROM Employees " \
                    "GROUP BY PositionId ) AS counts ) ) UNION SELECT title, 'It has the smallest number of employees' " \
                    "AS comment FROM Positions WHERE PositionId IN ( SELECT PositionId FROM Employees " \
                    "GROUP BY PositionId HAVING COUNT(*) = ( SELECT MIN(emp_count) FROM ( SELECT COUNT(*) AS emp_count " \
                    "FROM Employees GROUP BY PositionId ) AS counts ) );"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["title"], row["comment"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query17, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query17, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query17, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query17.pdf"))
        self.button_export.pack()

        self.query17.mainloop()

    def query18(self):
        logging.info(f"{self.current_user} вибрав query18")
        self.query18 = tk.Tk()
        self.query18.title("Запит №18")
        self.query18.geometry("400x300")

        self.label_title_q18 = tk.Label(self.query18,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q18.pack()

        # определяем столбцы
        self.columns = ("EmployeeId", "EmployeeName", "Comment")

        self.tree = ttk.Treeview(self.query18, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("EmployeeId", text="Айді працівника", anchor=W)
        self.tree.heading("EmployeeName", text="Ім'я", anchor=W)
        self.tree.heading("Comment", text="Коментар", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)
        self.tree.column("#3", stretch=NO, width=180)

        # добавляем данные
        with connection.cursor() as cursor:
            query = "SELECT EmployeeId, CONCAT(FirstName, ' ', LastName) " \
                    "AS EmployeeName, 'Responsible for the largest number of organized sales' AS Comment " \
                    "FROM Employees WHERE EmployeeId IN ( SELECT EmployeeId FROM Sales GROUP BY EmployeeId " \
                    "HAVING COUNT(*) = ( SELECT MAX(sale_count) FROM ( SELECT COUNT(*) AS sale_count FROM Sales " \
                    "GROUP BY EmployeeId ) AS counts ) ) UNION SELECT EmployeeId, CONCAT(FirstName, ' ', LastName) " \
                    "AS EmployeeName, 'Not responsible for any sales' AS Comment FROM Employees " \
                    "WHERE EmployeeId NOT IN ( SELECT EmployeeId FROM Sales );"
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["EmployeeId"], row["EmployeeName"], row["Comment"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query18, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query18, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.button_export = tk.Button(self.query18, text="Експорт в PDF",
                                       command=lambda: self.export_to_pdf("query18.pdf"))
        self.button_export.pack()

        self.query18.mainloop()

    def export_to_pdf(self, title):
        logging.info(f"{self.current_user} роздрукував {title}")
        pdf_filename = f"{title}"

        # Определяем ширины столбцов
        column_widths = [100, 180, 250]

        # Создаем PDF-документ
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        # Добавляем заголовки
        self.add_table_headers(c, column_widths)

        # Добавляем данные
        self.add_table_data(c, column_widths)

        # Сохраняем и закрываем PDF-документ
        c.save()
        print(f"Результаты запроса сохранены в файл: {title}")

    def add_table_headers(self, pdf_canvas, column_widths):
        for i, column in enumerate(self.columns):
            pdf_canvas.setFont("Helvetica-Bold", 12)
            pdf_canvas.drawString(sum(column_widths[:i]) + 20, 750, column)

    def add_table_data(self, pdf_canvas, column_widths):
        for row_num, row in enumerate(self.tree.get_children()):
            y = 700 - (row_num + 1) * 20
            values = [self.tree.item(row)["values"][i] for i in range(len(self.columns))]
            for i, value in enumerate(values):
                pdf_canvas.setFont("Helvetica", 12)
                pdf_canvas.drawString(sum(column_widths[:i]) + 20, y, str(value))

    def query19(self):
        logging.info(f"{self.current_user} вибрав query19")
        self.query19 = tk.Tk()
        self.query19.title("Запит №19")
        self.query19.geometry("400x300")

        self.label_title_q19 = tk.Label(self.query19,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q19.pack()

        # определяем столбцы
        self.columns = ("EmployeeId", "FirstName", "LastName", "PositionId", "JobId", "ExtraInfo")

        self.tree = ttk.Treeview(self.query19, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("EmployeeId", text="Айді працівника", anchor=W)
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)
        self.tree.heading("PositionId", text="Айді посади", anchor=W)
        self.tree.heading("JobId", text="Айді праці", anchor=W)
        self.tree.heading("ExtraInfo", text="Додаткова інформація", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)
        self.tree.column("#3", stretch=NO, width=180)
        self.tree.column("#4", stretch=NO, width=180)
        self.tree.column("#5", stretch=NO, width=180)
        self.tree.column("#6", stretch=NO, width=250)

        # добавляем данные
        with connection.cursor() as cursor:
            update_query = "UPDATE Employees SET ExtraInfo = 'Зробив найбільшу кількість продажів' " \
                           "WHERE EmployeeId = ( SELECT EmployeeId FROM ( SELECT EmployeeId, COUNT(*) AS SalesCount " \
                           "FROM Sales GROUP BY EmployeeId HAVING COUNT(*) = ( SELECT MAX(SalesCount) " \
                           "FROM ( SELECT EmployeeId, COUNT(*) AS SalesCount FROM Sales " \
                           "GROUP BY EmployeeId ) AS EmployeeSales ) ) AS MaxSales );"
            cursor.execute(update_query)

        # отримуємо оновлені дані
        with connection.cursor() as cursor:
            select_query = "SELECT EmployeeId, FirstName, LastName, PositionId, JobId, ExtraInfo FROM Employees"
            cursor.execute(select_query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["EmployeeId"], row["FirstName"], row["LastName"], row["PositionId"], row["JobId"], row["ExtraInfo"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query19, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query19, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query19.mainloop()

    def query20(self):
        logging.info(f"{self.current_user} вибрав query20")
        self.query20 = tk.Tk()
        self.query20.title("Запит №19")
        self.query20.geometry("400x300")

        self.label_title_q20 = tk.Label(self.query20,
                                        text="Результати запиту",
                                        font=("Arial", 13))
        self.label_title_q20.pack()

        # определяем столбцы
        self.columns = ("EmployeeId", "FirstName", "LastName", "PositionId", "JobId", "ExtraInfo")

        self.tree = ttk.Treeview(self.query20, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("EmployeeId", text="Айді працівника", anchor=W)
        self.tree.heading("FirstName", text="Ім'я", anchor=W)
        self.tree.heading("LastName", text="Прізвище", anchor=W)
        self.tree.heading("PositionId", text="Айді посади", anchor=W)
        self.tree.heading("JobId", text="Айді праці", anchor=W)
        self.tree.heading("ExtraInfo", text="Додаткова інформація", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=180)
        self.tree.column("#2", stretch=NO, width=180)
        self.tree.column("#3", stretch=NO, width=180)
        self.tree.column("#4", stretch=NO, width=180)
        self.tree.column("#5", stretch=NO, width=180)
        self.tree.column("#6", stretch=NO, width=250)

        # добавляем данные
        with connection.cursor() as cursor:
            update_query = "UPDATE Employees SET ExtraInfo = 'Зробивши найменшу кількість продажів' " \
                           "WHERE EmployeeId = ( SELECT EmployeeId FROM ( SELECT EmployeeId, COUNT(*) AS SalesCount " \
                           "FROM Sales GROUP BY EmployeeId HAVING COUNT(*) = ( SELECT MIN(SalesCount) " \
                           "FROM ( SELECT EmployeeId, COUNT(*) AS SalesCount FROM Sales GROUP BY EmployeeId ) " \
                           "AS EmployeeSales ) ) AS MinSales );"
            cursor.execute(update_query)

        # отримуємо оновлені дані
        with connection.cursor() as cursor:
            select_query = "SELECT EmployeeId, FirstName, LastName, PositionId, JobId, ExtraInfo FROM Employees"
            cursor.execute(select_query)
            rows = cursor.fetchall()

        for row in rows:
            values = (
                row["EmployeeId"], row["FirstName"], row["LastName"], row["PositionId"], row["JobId"], row["ExtraInfo"])
            self.tree.insert("", END, values=values)

        # добавляем полосу прокрутки по вертикали
        scrollbar_y = ttk.Scrollbar(self.query20, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=RIGHT, fill=Y)

        # добавляем полосу прокрутки по горизонтали
        scrollbar_x = ttk.Scrollbar(self.query20, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.query20.mainloop()


if __name__ == '__main__':
    # Создание экземпляра приложения
    app = DatabaseAuthApp()
