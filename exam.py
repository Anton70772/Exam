import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="234565",
        database="users"
    )

def execute_query(query, params=(), fetch=False):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

def add_note():
    if validate_entries():
        execute_query("INSERT INTO user (name, fullName) VALUES (%s, %s)", (entry_name.get(), entry_full_name.get()))
        clear_entries()
        display_notes()
    else:
        messagebox.showwarning("Input Error", "Both fields must be filled out.")

def update_note():
    if selected_record_id.get() and validate_entries():
        execute_query("UPDATE user SET name = %s, fullName = %s WHERE id = %s",
                      (entry_name.get(), entry_full_name.get(), selected_record_id.get()))
        clear_entries()
        display_notes()
    else:
        messagebox.showwarning("Input Error", "All fields must be filled out.")

def delete_note():
    selected_item = tree.selection()
    if selected_item:
        record_id = tree.item(selected_item[0])['values'][0]
        execute_query("DELETE FROM user WHERE id = %s", (record_id,))
        display_notes()
    else:
        messagebox.showwarning("Selection Error", "No record selected.")

def load_note(event):
    selected_item = tree.selection()
    if selected_item:
        record = tree.item(selected_item[0])['values']
        selected_record_id.set(record[0])
        entry_name.delete(0, tk.END)
        entry_name.insert(0, record[1])
        entry_full_name.delete(0, tk.END)
        entry_full_name.insert(0, record[2])

def display_notes():
    records = execute_query("SELECT * FROM user", fetch=True)
    for item in tree.get_children():
        tree.delete(item)
    for record in records:
        tree.insert("", tk.END, values=record)

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_full_name.delete(0, tk.END)
    selected_record_id.set("")

def validate_entries():
    return entry_name.get() and entry_full_name.get()

root = tk.Tk()
root.title("User Management")
root.geometry("700x400")

selected_record_id = tk.StringVar()

tk.Label(root, text="Имя:").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Фамилия:").grid(row=1, column=0, padx=10, pady=10)
entry_full_name = tk.Entry(root)
entry_full_name.grid(row=1, column=1, padx=10, pady=10)

btn_add = tk.Button(root, text="Добавить", command=add_note)
btn_add.grid(row=2, column=0, pady=10)

btn_update = tk.Button(root, text="Редактировать", command=update_note)
btn_update.grid(row=2, column=1, pady=10)

btn_delete = tk.Button(root, text="Удалить", command=delete_note)
btn_delete.grid(row=2, column=2, pady=10)

columns = ("ID", "Name", "Full Name")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Full Name", text="Full Name")
tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
tree.bind("<Double-1>", load_note)
tree.bind("<ButtonRelease-1>", lambda event: None)

display_notes()

root.mainloop()