"""
This is the UI for the Program.
"""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"



import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class UI:
    def init(self, accessible_tabs = []):
        self.accessible_tabs = accessible_tabs
    
    
    # Setup SQLite Database
    # should be in a separate file (Data and User Management)
    def setup_database():
        # connecting with the file
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Admin', 'Kassenwart', 'Finanz-Viewer'))
            )
        """)
        # Ensure the role column exists (for existing tables without the role column)
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        if "role" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'Finanz-Viewer'")
        # Add a default user for testing (username: admin, password: admin, role: Admin)
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin", "Admin"))
        conn.commit()
        conn.close()

                    
    # Verify Login Credentials
    # this should be in a separate file (Data and User Management)
    def verify_login(username, password):
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]  # Return the role directly
        return None

    # updating the user role
    # this should be in a separate file (Data and User Management)
    def update_user_role(username, new_role):
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        conn.commit()
        conn.close()
        print(f"Updated role for user '{username}' to '{new_role}'")


    # Add New User
    # this should be in a separate file (Data and User Management)
    def add_new_user(username, password, role):
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    # Add New Department
    # this should be in a separate file (Data and User Management)
    def add_department(name, initial_balance):
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                balance REAL NOT NULL
            )""")
            cursor.execute("INSERT INTO departments (name, balance) VALUES (?, ?)", (name, initial_balance))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    # centers the windows
    def center_window(window, width, height):
        window_width = width
        window_height = height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")


    # Main App Window
    # hier raus alle Funktionen rausziehen
    def open_main_window(self, role): ## need to add self to make it work
        print(f"User role detected: {role}")  # Debugging
        main_window = tk.Tk()
        main_window.title("Tabbed Interface App")
        UI.center_window(main_window, 1050, 800) #using center_window for main window

        # Create Tab Control
        tab_control = ttk.Notebook(main_window)

        # Create Tabs Based on Role
        tabs = []
        if role == "Admin":
            self.accessible_tabs = 6
        elif role == "Kassenwart":
            self.accessible_tabs = 3
        elif role == "Finanz-Viewer":
            self.accessible_tabs = 2
        else:
            self.accessible_tabs = 0
        
        if role == "Admin":
            self.accessible_tabs = [
                "Dashboard", 
                "Mitglieder", 
                "Finanzen", 
                "Berichte",
                "Abteilungen hinzufügen", 
                "Admin-Einstellungen"
            ]
        elif role == "Kassenwart":
            self.accessible_tabs = ["Dashboard", "Mitglieder", "Finanzen"]
        elif role == "Finanz-Viewer":
            self.accessible_tabs = ["Dashboard", "Berichte"]
        else:
            self.accessible_tabs = []


        tabs = []
        for tab_name in self.accessible_tabs:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=tab_name)
            ttk.Label(tab, text=f"Dies ist der Bereich: {tab_name}", font=("Arial", 14)).pack(pady=20)
            tabs.append(tab)

        

        """for i in range(1, self.accessible_tabs + 1):
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=f"Tab {i}")
            ttk.Label(tab, text=f"This is Tab {i}", font=("Arial", 14)).pack(pady=20)
            tabs.append(tab)"""
        
        """ # Only Admin role enabled
        if role == "Admin":
            self.accessible_tabs = 5
            tabs = []
            for i in range(1, self.accessible_tabs + 1):
                tab = ttk.Frame(tab_control)
                tab_control.add(tab, text=f"Tab {i}")
                ttk.Label(tab, text=f"This is Tab {i}", font=("Arial", 14)).pack(pady=20)
                tabs.append(tab)"""


        # Add Admin Panel in Tab 6 for Admin Role
        if role == "Admin" and len(tabs) == 6:
            #Tab muss umbenannt werden!!!
            # Tanja: wir sollten auf jeden Fall Funktionen nicht hier deklarieren und muessen es anderswo schieben
            def handle_add_user():
                new_username = username_entry.get()
                new_password = password_entry.get()
                new_role = role_combobox.get()

                if new_username and new_password and new_role:
                    if UI.add_new_user(new_username, new_password, new_role):
                        messagebox.showinfo("Success", f"User '{new_username}' added successfully.")
                        username_entry.delete(0, tk.END)
                        password_entry.delete(0, tk.END)
                        role_combobox.set("")
                    else:
                        messagebox.showerror("Error", f"Username '{new_username}' already exists.")
                else:
                    messagebox.showerror("Error", "All fields are required.")

            ttk.Label(tabs[5], text="Add New User", font=("Arial", 14)).pack(pady=10)
            ttk.Label(tabs[5], text="New Username:").pack(pady=5)
            username_entry = ttk.Entry(tabs[5])
            username_entry.pack(pady=5)

            ttk.Label(tabs[5], text="New Password:").pack(pady=5)
            password_entry = ttk.Entry(tabs[5],) #show'*' entfernt
            password_entry.pack(pady=5)

            ttk.Label(tabs[5], text="Role:").pack(pady=5)
            role_combobox = ttk.Combobox(tabs[5], values=["Admin", "Kassenwart", "Finanz-Viewer"])
            role_combobox.pack(pady=5)

            add_user_button = ttk.Button(tabs[5], text="Add User", command=handle_add_user)
            add_user_button.pack(pady=10)

            # aus der Funktion rausziehen
            def handle_add_department():
                dept_name = dept_name_entry.get()
                initial_balance = dept_balance_entry.get()
                
                if dept_name and initial_balance:
                    try:
                        initial_balance = float(initial_balance)
                        success = UI.add_department(dept_name, initial_balance)
                        if success:
                            messagebox.showinfo("Erfolg", f"Abteilung '{dept_name}' wurde hinzugefügt.")
                        else:
                            messagebox.showerror("Fehler", f"Abteilung '{dept_name}' existiert bereits.")
                    except ValueError:
                        messagebox.showerror("Fehler", "Der Kontostand muss eine Zahl sein.")
                else:
                    messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden.")
            ###
            ttk.Label(tabs[4], text="Abteilung hinzufügen", font=("Arial", 14)).pack(pady=10)
            ttk.Label(tabs[4], text="Abteilungsname:").pack(pady=5)
            dept_name_entry = ttk.Entry(tabs[4])
            dept_name_entry.pack(pady=5)

            ttk.Label(tabs[4], text="Startsaldo:").pack(pady=5)
            dept_balance_entry = ttk.Entry(tabs[4])
            dept_balance_entry.pack(pady=5)

            add_dept_button = ttk.Button(tabs[4], text="Abteilung hinzufügen", command=handle_add_department)
            add_dept_button.pack(pady=10)

        tab_control.pack(expand=1, fill="both")
        main_window.mainloop()

    # for debugging/test
    # this should be in a separate file (Data and User Management)
    def debug_database():
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()

        print("Fetching all users from the database:")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(user)  # Zeigt alle Benutzerdaten an

        conn.close()


    # Login Window
    def open_login_window():
        # rausziehen
        def handle_login():
            UI = UI()
            username = username_entry.get()
            password = password_entry.get()

            user_role = UI.verify_login(username, password)
            if user_role:
                messagebox.showinfo("Login Success", "Welcome!")
                login_window.destroy()
                UI.open_main_window(role=user_role)  # Pass the role to the main window
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        login_window = tk.Tk()
        login_window.title("Login")
        UI.center_window(login_window, 300, 200) #using center_window for main window

        ttk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(login_window)
        username_entry.pack(pady=5)

        ttk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        login_button = ttk.Button(login_window, text="Login", command=handle_login)
        login_button.pack(pady=10)

        login_window.mainloop()

    """
    def generate_departments(self):
        # is supposed to populate an existing box
        # what is table_listbox?
        self.table_listbox.delete(0, tk.END)
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            self.table_listbox.insert(tk.END, f"Tisch {i}")
        # show list


    def populate_finanzen_tab(tabs):
        #This builds the UI elements for the table tab.

        # zeigt an Abteilungen
        #ttk.Button(self.tabs[5], text='Alle Abteilungen anzeigen',
        #        command=generate_departments).pack(pady=5)
        #ttk.Button(self.table_tab, text='Abteilung auswählen',
        #        command=self.select_table).pack(pady=5)

        # show list
        ttk.Label(self.accessible_tabs[1], text='Abteilungen:').pack(pady=5)
        self.department_listbox = tk.Listbox(self.table_tab, height=10, width=50)
        self.department_listbox.pack(pady=10)
    """
# Main Execution
if __name__ == "__main__":
    UI.setup_database()
    UI.open_login_window()
    UI.update_user_role("admin", "Admin")  # Aktualisiere die Rolle für den Admin