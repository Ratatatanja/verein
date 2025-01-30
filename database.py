"""This file is responsible for the database."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"


import sqlite3

class DatabaseManager:
    def __init__(self, db_name="app_data.db"):
        self.db_name = db_name
        # records what kind of finance operation has been done
        #self.operation_type = operation_type

    def setup_database(self):
        """Initializes the databank and creates tables."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Tabelle für Benutzer erstellen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN 
                ('Admin', 'Kassenwart', 'Finanz-Viewer'))
            )
        """)

        # Sicherstellen, dass die Rolle-Spalte existiert
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        if "role" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL"
                           " DEFAULT 'Finanz-Viewer'")

        # Standard-Benutzer hinzufügen
        cursor.execute("INSERT OR IGNORE INTO users "
                       "(username, password, role) VALUES (?, ?, ?)",
                       ("admin", "admin", "Admin"))

        conn.commit()
        conn.close()

    def verify_login(self, username, password):
        """Checks login data of user."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?"
                       " AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def update_user_role(self, username, new_role):
        """Updates user role."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE username = ?",
                       (new_role, username))
        conn.commit()
        conn.close()

    def add_department(self, name, initial_balance):
        """Adds a department."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL
            )""")
            cursor.execute("INSERT INTO departments (name, balance)"
                           " VALUES (?, ?)",
                           (name, initial_balance))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False


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


    def get_department_name(self, department_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""SELECT name FROM departments
                                WHERE id = (?)""", (department_id,))
            department_name = cursor.fetchall()
            return department_name
        except sqlite3.IntegrityError:
            return False


    def record(self, department_name, type, amount, new_balance):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
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

    def debug_database(self):
        """
        Gives back all users in the terminal (for debugging)."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        for user in users:
            print(user)


# Main Execution
if __name__ == "__main__":
    db = DatabaseManager()
    #db.add_balance(1,10)
    db.reduce_balance("wettessen",10)
    #db.record(department_name="Disco", type="deposit", amount="10", new_balance="2010")