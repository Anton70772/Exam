
import tkinter as tk
from tkinter.ttk import Treeview
import pymysql

class App:
    Con = None

    def SQL_Connect(self):
        try:
            self.Con = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                password="12345678",
                database="db31",
            )
            self.cur = self.Con.cursor()
            self.cur.execute("select * from new_table")
            self.result = self.cur.fetchall()
            self.cur.close()
        except:
            print("error")

    def btns(self):
        self.add_button = tk.Button(self.root, text="Добавить запись", command=self.add)
        self.add_button.place(x=400, y=300)

        self.delete_button = tk.Button(self.root, text="Удалить запись", command=self.delete)
        self.delete_button.place(x=600, y=300)

    def entry(self):
        self.id_label = tk.Label(self.root, text="ID")
        self.id_label.place(x=500, y=400)
        self.id = tk.Entry(self.root)
        self.id.place(x=520, y=400)

        col1_label = tk.Label(self.root, text="col1")
        col1_label.place(x=490, y=430)
        self.col1 = tk.Entry(self.root)
        self.col1.place(x=520, y=430)

        col2_label = tk.Label(self.root, text="col2")
        col2_label.place(x=490, y=460)
        self.col2 = tk.Entry(self.root)
        self.col2.place(x=520, y=460)

        col3_label = tk.Label(self.root, text="col3")
        col3_label.place(x=490, y=490)
        self.col3 = tk.Entry(self.root)
        self.col3.place(x=520, y=490)
    def insert(self):
        self.root = tk.Tk()
        self.root.geometry('1020x600')
        self.root.title("БД")

        self.btns()
        self.entry()

        tree = Treeview(self.root, columns=("id", "col1", "col2", "col3"))
        tree.grid(column=0,row=0)
        tree.heading("id", text="ID")
        tree.heading("col1", text="Колумн1")
        tree.heading("col2", text="Колумн2")
        tree.heading("col3", text="Колумн3")

        tree.insert("", "end", text="Ошибка подключения к базе данных")

        self.SQL_Connect()

    def add(self):
        self.mycursor = self.Con.cursor()

        self.col1_val = self.col1.get()
        self.col2_val = self.col2.get()
        self.col3_val = self.col3.get()

        self.sql = "INSERT INTO new_table (ID, col1, col2, col3) VALUES (%s, %s, %s, %s)"
        self.val = (self.col1_val, self.col2_val, self.col3_val)

        self.mycursor.execute(self.sql, self.val)
        self.Con.commit()
        print("Запись успешно добавлена!")
        self.Con.close()

    def delete(self):
        self.mycursor = self.Con.cursor()

        id_val = self.id.get()

        sql = "DELETE FROM new_table WHERE id = %s"
        val = (id_val,)

        self.mycursor.execute(sql, val)
        self.Con.commit()

        print("Запись успешно удалена!")
        self.Con.close()



if __name__ == "__main__":
    app = App()

    app.insert()

    app.root.mainloop()

# root = tk.Tk()
# app = App()
# app.window = root
# app.main()
# root.mainloop()