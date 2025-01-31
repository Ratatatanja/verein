import sqlite3
import datetime


class Finance:
    def __init__(self, db_name="app_data.db"):
        self.db_name = db_name

    def add_balance(self, department_name, amount, username, role):
        """Erhöht das Guthaben einer Abteilung und speichert die Transaktion."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM departments WHERE name = ?",
                           (department_name,))
            department_balance = cursor.fetchone()

            if department_balance is None:
                return False  # Abteilung existiert nicht

            new_balance = department_balance[0] + float(amount)
            cursor.execute("UPDATE departments SET balance = ? WHERE name = ?",
                           (new_balance, department_name))
            conn.commit()
            conn.close()

            self.record(department_name, "deposit", amount, new_balance,
                        username, role)
            return True
        except sqlite3.IntegrityError:
            return False

    def reduce_balance(self, department_name, amount, username, role):
        """Verringert das Guthaben einer Abteilung und speichert die Transaktion."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM departments WHERE name = ?",
                           (department_name,))
            department_balance = cursor.fetchone()

            if department_balance is None or department_balance[0] < float(
                    amount):
                return False  # Abteilung existiert nicht oder nicht genug Guthaben

            new_balance = department_balance[0] - float(amount)
            cursor.execute("UPDATE departments SET balance = ? WHERE name = ?",
                           (new_balance, department_name))
            conn.commit()
            conn.close()

            self.record(department_name, "withdraw", amount, new_balance,
                        username, role)
            return True
        except sqlite3.IntegrityError:
            return False

    def record(self, department_name, operation, amount, new_balance, username,
               role):
        """Speichert eine Transaktion mit Zeitstempel, Benutzername und Rolle."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                department TEXT NOT NULL,
                operation TEXT NOT NULL,
                amount REAL NOT NULL,
                balance REAL NOT NULL,
                timestamp TEXT NOT NULL,
                username TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO history (department, operation, amount, balance, timestamp, username, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (department_name, operation, amount, new_balance, timestamp,
             username, role))
        conn.commit()
        conn.close()
