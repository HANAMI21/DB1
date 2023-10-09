import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Подключение к базе данных
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="3Ey6x+eQ",
    database="farming"
)

# Создание окна
window = tk.Tk()
window.title("CRUD-запросы для таблицы Position")

# Функция для выполнения CRUD-запросов
def execute_query(query, values=None):
    cursor = db.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        db.commit()
        messagebox.showinfo("Успех", "Запрос успешно выполнен.")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    finally:
        cursor.close()

# Функция для создания таблицы
def create_table():
    query = """CREATE TABLE IF NOT EXISTS Position (
                    PositionId INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                    title VARCHAR(50)
                );"""
    execute_query(query)

# Функция для добавления записи
def add_position():
    title = entry_title.get()
    query = "INSERT INTO Position (title) VALUES (%s);"
    values = (title,)
    execute_query(query, values)

# Функция для обновления записи
def update_position():
    position_id = entry_position_id.get()
    title = entry_title.get()
    query = "UPDATE Position SET title = %s WHERE PositionId = %s;"
    values = (title, position_id)
    execute_query(query, values)

# Функция для удаления записи
def delete_position():
    position_id = entry_position_id.get()
    query = "DELETE FROM Position WHERE PositionId = %s;"
    values = (position_id,)
    execute_query(query, values)

# Функция для чтения записи
def read_positions():
    query = "SELECT * FROM Position;"
    cursor = db.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        messagebox.showinfo("Позиции", rows)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    finally:
        cursor.close()

# Создание таблицы (если она еще не существует)
create_table()

# Создание и размещение элементов интерфейса
label_position_id = tk.Label(window, text="Position ID:")
label_position_id.pack()
entry_position_id = tk.Entry(window)
entry_position_id.pack()

label_title = tk.Label(window, text="Title:")
label_title.pack()
entry_title = tk.Entry(window)
entry_title.pack()

btn_add = tk.Button(window, text="Добавить", command=add_position)
btn_add.pack()

btn_update = tk.Button(window, text="Обновить", command=update_position)
btn_update.pack()

btn_delete = tk.Button(window, text="Удалить", command=delete_position)
btn_delete.pack()

btn_read = tk.Button(window, text="Прочитать все позиции", command=read_positions)
btn_read.pack()

# Запуск главного цикла окна
window.mainloop()
