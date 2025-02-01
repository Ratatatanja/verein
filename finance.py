"""This file is responsible for the database data concerning department finances."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"

import sqlite3

class Finance:
    def __init__(self, db_name="app_data.db"):
        """Initialises the name of the data base."""
        self.db_name = db_name

    def add_balance(self, department_name, amount):
        """Add money to existing balance of a department"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""SELECT balance FROM departments
                                WHERE name = (?)""", (department_name,))
            department_balance = cursor.fetchall()
            new_balance = round(float(amount)+department_balance[0][0],2)
            cursor.execute("""UPDATE departments
            SET balance = (?)
            WHERE name = (?)""", (new_balance, department_name))
            conn.commit()
            conn.close()
            # fetches the name of the department using the id
            # records the transaction
            self.record(department_name, type="deposit", amount=amount,
                         new_balance=new_balance)
            return True
        except sqlite3.IntegrityError:
            return False


    def reduce_balance(self, department_name, amount):
        """Reduces the amount of money in the account of a department."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Aktuelles Guthaben abrufen
            cursor.execute("SELECT balance FROM departments WHERE name = ?",
                           (department_name,))
            department_balance = cursor.fetchone()

            if department_balance is None:
                messagebox.showerror("Fehler",
                                     f"Abteilung '{department_name}' nicht gefunden.")
                return False

            current_balance = department_balance[0]
            amount = float(amount)

            # Checks if there is enough money
            if current_balance - amount < 0:
                messagebox.showerror("Fehler",
                                     f"Nicht genug Guthaben auf dem Konto von '{department_name}'!")
                return False

            # Guthaben aktualisieren
            new_balance = round(current_balance - amount,2)
            cursor.execute("UPDATE departments SET balance = ? WHERE name = ?",
                           (new_balance, department_name))
            conn.commit()
            conn.close()

            # Transaktion aufzeichnen
            self.record(department_name, "withdraw", amount, new_balance)
            return True

        except sqlite3.IntegrityError:
            return False


    def record(self, department_name, type, amount, new_balance):
        """Saves the information on transactions in a history table."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department TEXT NOT NULL,
                operation TEXT NOT NULL,
                amount REAL NOT NULL,
                balance REAL NOT NULL
            )
            """)
            cursor.execute("""INSERT INTO history 
                               (department, operation, amount, balance)
                               VALUES (?, ?, ?, ?)""",
                           (department_name, type, amount, new_balance))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False


    def get_transaction_history(self):
        """Gives back the whole transaction history."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, department, operation, amount, balance FROM history")  # Ohne timestamp
        records = cursor.fetchall()
        conn.close()
        return records
