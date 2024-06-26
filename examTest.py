import unittest
import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from unittest.mock import patch

import exam

class TestUserManagementApp(unittest.TestCase):

    def setUp(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="234565",
            database="users"
        )
        self.cursor = self.db_connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), fullName VARCHAR(255))")

        self.root = tk.Tk()
        self.root.title("User Management")
        self.root.geometry("700x400")

        self.selected_record_id = tk.StringVar()
        self.entry_name = tk.Entry(self.root)
        self.entry_full_name = tk.Entry(self.root)

        tk.Label(self.root, text="Имя:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.root, text="Фамилия:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_full_name.grid(row=1, column=1, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Full Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.tree.bind("<Double-1>", lambda event: exam.load_note(event))
        self.tree.bind("<ButtonRelease-1>", lambda event: None)
        self.root.mainloop()

    def tearDown(self):
        """Очистка после тестов."""
        self.cursor.execute("DROP TABLE IF EXISTS user")
        self.db_connection.close()

    def test_create_connection(self):
        conn = exam.create_connection()
        self.assertTrue(conn.is_connected())
        conn.close()

    def test_execute_query(self):
        exam.execute_query("INSERT INTO user (name, fullName) VALUES (%s, %s)", ("Alice", "Smith"))
        self.cursor.execute("SELECT * FROM user WHERE name=%s AND fullName=%s", ("Alice", "Smith"))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Alice")
        self.assertEqual(result[2], "Smith")

        results = exam.execute_query("SELECT * FROM user", fetch=True)
        self.assertGreater(len(results), 0)

        exam.execute_query("UPDATE user SET name=%s WHERE name=%s", ("Bob", "Alice"))
        self.cursor.execute("SELECT * FROM user WHERE name=%s", ("Bob",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Bob")

        exam.execute_query("DELETE FROM user WHERE name=%s", ("Bob",))
        self.cursor.execute("SELECT * FROM user WHERE name=%s", ("Bob",))
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_add_note(self):
        exam.entry_name.insert(0, "John")
        exam.entry_full_name.insert(0, "Doe")
        exam.add_note()
        self.cursor.execute("SELECT * FROM user WHERE name=%s AND fullName=%s", ("John", "Doe"))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "John")
        self.assertEqual(result[2], "Doe")

    def test_update_note(self):
        exam.execute_query("INSERT INTO user (name, fullName) VALUES (%s, %s)", ("Alice", "Smith"))
        self.cursor.execute("SELECT id FROM user WHERE name=%s AND fullName=%s", ("Alice", "Smith"))
        record_id = self.cursor.fetchone()[0]
        exam.selected_record_id.set(record_id)
        exam.entry_name.insert(0, "Alice Updated")
        exam.entry_full_name.insert(0, "Smith Updated")
        exam.update_note()
        self.cursor.execute("SELECT * FROM user WHERE id=%s", (record_id,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Alice Updated")
        self.assertEqual(result[2], "Smith Updated")

    def test_delete_note(self):
        exam.execute_query("INSERT INTO user (name, fullName) VALUES (%s, %s)", ("Charlie", "Brown"))
        self.cursor.execute("SELECT id FROM user WHERE name=%s AND fullName=%s", ("Charlie", "Brown"))
        record_id = self.cursor.fetchone()[0]
        exam.tree.insert("", tk.END, values=(record_id, "Charlie", "Brown"))
        exam.tree.selection_set(exam.tree.get_children()[0])
        exam.delete_note()
        self.cursor.execute("SELECT * FROM user WHERE id=%s", (record_id,))
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_load_note(self):
        exam.execute_query("INSERT INTO user (name, fullName) VALUES (%s, %s)", ("David", "Smith"))
        exam.display_notes()
        exam.tree.selection_set(exam.tree.get_children()[0])
        exam.load_note(None)
        self.assertEqual(exam.entry_name.get(), "David")
        self.assertEqual(exam.entry_full_name.get(), "Smith")

    def test_display_notes(self):
        exam.execute_query("INSERT INTO user (name, fullName) VALUES (%s, %s)", ("Eve", "Adams"))
        exam.display_notes()
        records = exam.tree.get_children()
        self.assertGreater(len(records), 0)

    def test_clear_entries(self):
        exam.entry_name.insert(0, "Frank")
        exam.entry_full_name.insert(0, "Miller")
        exam.clear_entries()
        self.assertEqual(exam.entry_name.get(), "")
        self.assertEqual(exam.entry_full_name.get(), "")

    def test_validate_entries(self):
        exam.entry_name.insert(0, "George")
        exam.entry_full_name.insert(0, "Washington")
        self.assertTrue(exam.validate_entries())
        exam.clear_entries()
        self.assertFalse(exam.validate_entries())

if __name__ == '__main__':
    unittest.main()
