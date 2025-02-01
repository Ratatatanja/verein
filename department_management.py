"""This file is responsible for the management of users."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"



import sqlite3
from database import DatabaseManager
db_manager = DatabaseManager(db_name="app_data.db")

class DepartmentManager:
    def __init__(self, db_manager):
        """Initializes department management with database
        manager object."""
        self.db_manager = db_manager


    def add_department(self, name, initial_balance):
        """Adds new department."""
        return self.db_manager.add_department(name, initial_balance)
    

    def get_departments(self):
        """Gets all departments from database."""
        conn = sqlite3.connect(self.db_manager.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        conn.close()
        return departments


    def update_department_balance(self, department_id, new_balance):
        """updates account balance of department."""
        conn = sqlite3.connect(self.db_manager.db_name)
        cursor = conn.cursor()
        cursor.execute("UPDATE departments SET balance = ? WHERE id = ?",
                       (new_balance, department_id))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Beispiel-Tests
    db_manager = DatabaseManager()
    db_manager.setup_database()  # Stelle sicher, dass die Datenbank
    # initialisiert ist

    dept_manager = DepartmentManager(db_manager)

    # Test: Abteilung hinzufügen
    result = dept_manager.add_department("wettessen", 1000.0)
    print("Abteilung hinzugefügt:", result)

    # Test: Abteilungen abrufen
    departments = dept_manager.get_departments()
    print("Abteilungen:", departments)

    # Test: Abteilungssaldo aktualisieren
    if departments:
        dept_manager.update_department_balance(departments[0][0],
                                               2000.0)
        updated_departments = dept_manager.get_departments()
        print("Aktualisierte Abteilungen:", updated_departments)
