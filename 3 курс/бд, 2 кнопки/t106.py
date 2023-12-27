import mysql.connector
from tkinter import *
from mysql import connector

# Подключение к базе данных MySQL
mysql = connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="db31"
)

mycursor = mysql.cursor()

# Создание таблицы в базе данных (если она еще не существует)
mycursor.execute("CREATE TABLE IF NOT EXISTS persons (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT, lname VARCHAR(255))")

# Функция для добавления записи в базу данных
def add_record():
    sql = "INSERT INTO persons (name, age, lname) VALUES (%s, %s, %s)"
    val = (name_entry.get(), age_entry.get(), lname_entry.get())
    mycursor.execute(sql, val)
    mysql.commit()

# Функция для удаления записи из базы данных
def delete_record():
    sql = "DELETE FROM persons WHERE id = %s"
    val = (id_entry.get(),)
    mycursor.execute(sql, val)
    mysql.commit()

# Создание графического интерфейса с использованием tkinter
root = Tk()

id_label = Label(root, text="ID")
id_label.grid(row=0, column=0)
id_entry = Entry(root)
id_entry.grid(row=0, column=1)

name_label = Label(root, text="Name")
name_label.grid(row=1, column=0)
name_entry = Entry(root)
name_entry.grid(row=1, column=1)

age_label = Label(root, text="Age")
age_label.grid(row=2, column=0)
age_entry = Entry(root)
age_entry.grid(row=2, column=1)

lname_label = Label(root, text="Last Name")
lname_label.grid(row=3, column=0)
lname_entry = Entry(root)
lname_entry.grid(row=3, column=1)

add_button = Button(root, text="Add", command=add_record)
add_button.grid(row=4, column=0)

delete_button = Button(root, text="Delete", command=delete_record)
delete_button.grid(row=4, column=1)

root.mainloop()