"""This file is responsible for the management of users."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"


import sqlite3
from database import DatabaseManager
db_manager = DatabaseManager(db_name="app_data.db")

class UserManager:
    def __init__(self, db_manager):
        """Initialisiert die Benutzerverwaltung mit einem DatabaseManager-Objekt."""
        self.db_manager = db_manager

    def add_new_user(self, username, password, role):
        """Fügt einen neuen Benutzer hinzu."""
        try:
            conn = sqlite3.connect(self.db_manager.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_user_role(self, username, new_role):
        """Aktualisiert die Rolle eines Benutzers."""
        success = self.db_manager.update_user_role(username, new_role)
        return success

    def verify_login(self, username, password):
        """
        Verifiziert die Anmeldedaten eines Benutzers und gibt die Rolle zurück, falls korrekt.
        """
        return self.db_manager.verify_login(username, password)

if __name__ == "__main__":
    # Beispiel-Tests
    db_manager = DatabaseManager()
    db_manager.setup_database()  # Stelle sicher, dass die Datenbank initialisiert ist

    user_manager = UserManager(db_manager)

    # Test: Benutzer hinzufügen
    result = user_manager.add_new_user("testuser", "password123", "Kassenwart")
    print("Benutzer hinzugefügt:", result)

    # Test: Rolle aktualisieren
    user_manager.update_user_role("testuser", "Admin")

    # Test: Login verifizieren
    role = user_manager.verify_login("testuser", "password123")
    print("Benutzerrolle:", role)
