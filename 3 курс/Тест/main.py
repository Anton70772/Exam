import tkinter as tk
from tkinter import ttk
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="studen"
)

cursor = db.cursor()


def update_user_list():
    user_list.delete(0, tk.END)


    query = "SELECT username, phone_number FROM new_table"
    cursor.execute(query)

    for user in cursor.fetchall():
        user_list.insert(tk.END, f"{user[0]} - {user[1]}")

def add_user():
    username = entry_name.get()
    phone_number = entry_phone.get()

    if username and phone_number:
        query = "INSERT INTO new_table (username, phone_number) VALUES (%s, %s)"
        values = (username, phone_number)
        cursor.execute(query, values)
        db.commit()
        status_var.set("Пользователь добавлен успешно!")
        update_user_list()
    else:
        status_var.set("Заполните все поля")

def delete_user():
    selected_user = user_list.get(tk.ACTIVE)
    if selected_user:
        username = selected_user.split(" - ")[0]
        query = "DELETE FROM new_table WHERE username = %s"
        value = (username,)
        cursor.execute(query, value)
        db.commit()
        status_var.set("Пользователь удален успешно!")
        update_user_list()
    else:
        status_var.set("Выберите пользователя для удаления")

root = tk.Tk()
root.title("Управление пользователями")

label_name = tk.Label(root, text="Имя пользователя:")
entry_name = tk.Entry(root)

label_phone = tk.Label(root, text="Номер телефона:")
entry_phone = tk.Entry(root)

btn_add = tk.Button(root, text="Добавить пользователя", command=add_user)
btn_delete = tk.Button(root, text="Удалить пользователя", command=delete_user)

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var)

user_list = tk.Listbox(root)
user_list.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

label_name.grid(row=0, column=0, padx=10, pady=10)
entry_name.grid(row=0, column=1, padx=10, pady=10)

label_phone.grid(row=1, column=0, padx=10, pady=10)
entry_phone.grid(row=1, column=1, padx=10, pady=10)

btn_add.grid(row=2, column=0, columnspan=2, pady=10)
btn_delete.grid(row=3, column=0, columnspan=2, pady=10)

status_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()

db.close()