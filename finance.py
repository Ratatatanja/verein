"""This file is responsible for the database data concerning department finances."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"

import sqlite3

class Finance:
    def __init__(self, db_name="app_data.db"):
        self.db_name = db_name

    def add_balance(self, department_name, amount):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""SELECT balance FROM departments
                                WHERE name = (?)""", (department_name,)) # brought back (,)
            department_balance = cursor.fetchall()
            print(department_balance[0][0])
            print(amount)
            print(type(amount))
            new_balance = int(amount)+department_balance[0][0]
            print(new_balance)
            cursor.execute("""UPDATE departments
            SET balance = (?)
            WHERE name = (?)""", (new_balance, department_name))
            conn.commit()
            conn.close()
            # fetches the name of the department using the id
            # records the transaction
            self.record(department_name, type="deposit", amount=amount, new_balance=new_balance)
            return True
        except sqlite3.IntegrityError:
            return False


    def reduce_balance(self, department_name, amount):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""SELECT balance FROM departments
                                WHERE name = (?)""", (department_name,))
            department_balance = cursor.fetchall()
            print(department_balance)
            new_balance = department_balance[0][0]-int(amount)
            # if not enough money, money can't be withdrawn
            if new_balance < 0:
                return False
            cursor.execute("""UPDATE departments
            SET balance = (?)
            WHERE name = (?)""", (new_balance, department_name))
            conn.commit()
            conn.close()
            # records the transaction
            self.record(department_name, type="withdraw", amount=amount, new_balance=new_balance)
            return True
        except sqlite3.IntegrityError:
            return False

    """
    def get_department_name(self, department_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(" ""SELECT name FROM departments
                                WHERE id = (?)" "", (department_id,))
            department_name = cursor.fetchall()
            return department_name
        except sqlite3.IntegrityError:
            return False
    """

    def record(self, department_name, type, amount, new_balance):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department TEXT NOT NULL,
                operation TEXT NOT NULL,
                amount REAL NOT NULL,
                balance REAL NOT NULL)
                """)
            # records what had been done in this department
            cursor.execute("""INSERT INTO history 
                           (department, operation, amount, balance)
                           VALUES (?, ?, ?, ?)""",
                           (department_name, type, amount, new_balance))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False