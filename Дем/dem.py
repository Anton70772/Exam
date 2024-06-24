import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import mysql.connector

root = tk.Tk()
root.title("Система учета заявок на ремонт оборудования")

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="234565",
        database="techno"
    )

def add_repair_request(equipment_id, requester_name, description, priority, status):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''INSERT INTO RepairRequest (equipment_id, requester_name, description, priority, status)
               VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(query, (equipment_id, requester_name, description, priority, status))
    conn.commit()
    conn.close()

def edit_repair_request(request_id, status, description):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''UPDATE RepairRequest
               SET status = %s, description = %s, update_date = %s
               WHERE request_id = %s'''
    cursor.execute(query, (status, description, datetime.now(), request_id))
    conn.commit()
    conn.close()

def get_all_repair_requests():
    conn = create_connection()
    cursor = conn.cursor()
    query = '''SELECT * FROM RepairRequest'''
    cursor.execute(query)
    requests = cursor.fetchall()
    conn.close()
    return requests

def get_repair_request_by_id(request_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''SELECT * FROM RepairRequest WHERE request_id = %s'''
    cursor.execute(query, (request_id,))
    request = cursor.fetchone()
    conn.close()
    return request

def calculate_statistics():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM RepairRequest WHERE status = 'выполнено' ''')
    completed_requests = cursor.fetchone()[0]

    cursor.execute('''SELECT AVG(TIMESTAMPDIFF(SECOND, creation_date, update_date)) / 3600 FROM RepairRequest WHERE status = 'выполнено' ''')
    avg_completion_time = cursor.fetchone()[0]

    cursor.execute('''SELECT priority, COUNT(*) FROM RepairRequest GROUP BY priority''')
    type_statistics = cursor.fetchall()

    conn.close()
    return {
        "completed_requests": completed_requests,
        "avg_completion_time": avg_completion_time,
        "type_statistics": type_statistics
    }

def equipment_exists(equipment_id):
    conn = create_connection()
    cursor = conn.cursor()
    query = '''SELECT COUNT(*) FROM Equipment WHERE equipment_id = %s'''
    cursor.execute(query, (equipment_id,))
    exists = cursor.fetchone()[0]
    conn.close()
    return exists > 0

def get_all_equipments():
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT equipment_id, type FROM Equipment"
    cursor.execute(query)
    equipments = cursor.fetchall()
    conn.close()
    return equipments

def add_request():
    equipment_id = combo_equipment.get().split(":")[0].strip()
    requester_name = entry_requester_name.get()
    description = entry_description.get()
    priority = combo_priority.get()
    status = combo_status.get()

    if not equipment_exists(equipment_id):
        messagebox.showerror("Ошибка", "Оборудование с указанным ID не существует")
        return

    add_repair_request(equipment_id, requester_name, description, priority, status)
    messagebox.showinfo("Успех", "Заявка добавлена")
    load_requests()

def edit_request():
    request_id = entry_request_id.get()
    status = combo_status_edit.get()
    description = entry_description_edit.get()

    edit_repair_request(request_id, status, description)
    messagebox.showinfo("Успех", "Заявка обновлена")
    load_requests()

def load_requests():
    requests = get_all_repair_requests()
    for row in tree.get_children():
        tree.delete(row)
    for request in requests:
        tree.insert("", "end", values=request)

frame_add = tk.Frame(root)
frame_add.pack(pady=10)

tk.Label(frame_add, text="Добавление заявки").grid(row=0, columnspan=2)

tk.Label(frame_add, text="Оборудование").grid(row=1, column=0)
combo_equipment = ttk.Combobox(frame_add, values=[f"{equip[0]}: {equip[1]}" for equip in get_all_equipments()])
combo_equipment.grid(row=1, column=1)

tk.Label(frame_add, text="Имя заявителя").grid(row=2, column=0)
entry_requester_name = tk.Entry(frame_add)
entry_requester_name.grid(row=2, column=1)

tk.Label(frame_add, text="Описание проблемы").grid(row=3, column=0)
entry_description = tk.Entry(frame_add)
entry_description.grid(row=3, column=1)

tk.Label(frame_add, text="Приоритет").grid(row=4, column=0)
combo_priority = ttk.Combobox(frame_add, values=["низкий", "средний", "высокий"])
combo_priority.grid(row=4, column=1)

tk.Label(frame_add, text="Статус").grid(row=5, column=0)
combo_status = ttk.Combobox(frame_add, values=["в ожидании", "в работе", "выполнено"])
combo_status.grid(row=5, column=1)

btn_add = tk.Button(frame_add, text="Добавить заявку", command=add_request)
btn_add.grid(row=6, columnspan=2, pady=5)

frame_edit = tk.Frame(root)
frame_edit.pack(pady=10)

tk.Label(frame_edit, text="Редактирование заявки").grid(row=0, columnspan=2)

tk.Label(frame_edit, text="Номер заявки").grid(row=1, column=0)
entry_request_id = tk.Entry(frame_edit)
entry_request_id.grid(row=1, column=1)

tk.Label(frame_edit, text="Статус").grid(row=2, column=0)
combo_status_edit = ttk.Combobox(frame_edit, values=["в ожидании", "в работе", "выполнено"])
combo_status_edit.grid(row=2, column=1)

tk.Label(frame_edit, text="Описание проблемы").grid(row=3, column=0)
entry_description_edit = tk.Entry(frame_edit)
entry_description_edit.grid(row=3, column=1)

btn_edit = tk.Button(frame_edit, text="Обновить заявку", command=edit_request)
btn_edit.grid(row=4, columnspan=2, pady=5)

tree = ttk.Treeview(root, columns=(
"ID", "Оборудование", "Заявитель", "Описание", "Приоритет", "Статус", "Дата создания", "Дата обновления"),
                    show="headings")
tree.pack(pady=10)

for col in tree["columns"]:
    tree.heading(col, text=col)

load_requests()

root.mainloop()