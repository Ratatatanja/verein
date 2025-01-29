"""This file is responsible for the UI."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"

import tkinter as tk
from tkinter import ttk, messagebox
from user_management import UserManager
from database import DatabaseManager
from department_management import DepartmentManager

class ApplicationUI:
    def __init__(self, db_name="app_data.db"):
        self.db_name = db_name
        self.db_manager = DatabaseManager()
        self.department_manager = DepartmentManager(self.db_manager)
        self.user_manager = UserManager(self.db_manager)
        self.db_manager.setup_database()

    def center_window(self, window, width, height):
        """This centers all windows on screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")


    def add_department_tab(self, tab):
        """This adds the department management funktions to the tab"""
        def handle_add_department():
            dept_name = dept_name_entry.get()
            initial_balance = dept_balance_entry.get()

            if dept_name and initial_balance:
                try:
                    initial_balance = float(initial_balance)
                    success = (self.department_manager.
                               add_department(dept_name,initial_balance))
                    if success:
                        messagebox.showinfo(
                            "Erfolg",f"Abteilung'{dept_name}'"
                                     f"wurde hinzugefügt.")
                    else:
                        messagebox.showerror(
                            "Fehler", f"Abteilung '{dept_name}'"
                                      f" existiert bereits.")
                except ValueError:
                    messagebox.showerror(
                        "Fehler", "Der Kontostand "
                                  "muss eine Zahl sein.")
            else:
                messagebox.showerror("Fehler", "Alle Felder "
                                               "müssen ausgefüllt werden.")

        ttk.Label(tab, text="Abteilung hinzufügen",
                  font=("Arial", 14)).pack(pady=10)
        ttk.Label(tab, text="Abteilungsname:").pack(pady=5)
        dept_name_entry = ttk.Entry(tab)
        dept_name_entry.pack(pady=5)

        ttk.Label(tab, text="Startsaldo:").pack(pady=5)
        dept_balance_entry = ttk.Entry(tab)
        dept_balance_entry.pack(pady=5)

        add_dept_button = ttk.Button(tab, text="Abteilung hinzufügen",
                                     command=handle_add_department)
        add_dept_button.pack(pady=10)


    def create_admin_settings_tab(self, parent_tab):
        """This creates the Tab Admin-Einstellungen."""
        def handle_add_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_combobox.get()

            if username and password and role:
                success = self.user_manager.add_new_user(username,
                                                         password, role)
                if success:
                    messagebox.showinfo("Erfolg",
                                        f"Benutzer '{username}'"
                                        f" wurde hinzugefügt.")
                    username_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    role_combobox.set("")
                else:
                    messagebox.showerror(
                        "Fehler",
                        f"Benutzername '{username}'"
                        f" existiert bereits.")
            else:
                messagebox.showerror("Fehler", "Alle"
                                               " Felder müssen "
                                               "ausgefüllt werden.")

        ttk.Label(parent_tab, text="Benutzerverwaltung",
                  font=("Arial", 14)).pack(pady=10)

        ttk.Label(parent_tab, text="Benutzername:").pack(pady=5)
        username_entry = ttk.Entry(parent_tab)
        username_entry.pack(pady=5)

        ttk.Label(parent_tab, text="Passwort:").pack(pady=5)
        password_entry = ttk.Entry(parent_tab, show="*")
        password_entry.pack(pady=5)

        ttk.Label(parent_tab, text="Rolle:").pack(pady=5)
        role_combobox = ttk.Combobox(parent_tab, values=["Admin",
                                                         "Kassenwart",
                                                         "Finanz-Viewer"])
        role_combobox.pack(pady=5)

        add_user_button = ttk.Button(parent_tab,
                                     text="Benutzer hinzufügen",
                                     command=handle_add_user)
        add_user_button.pack(pady=10)


    def populate_departments(self):
        """This function is for the button which shows all departments"""
        import sqlite3
        self.department_listbox.delete(0, tk.END)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # takes all department names
        cursor.execute("""SELECT name FROM departments""")
        department_list = cursor.fetchall()
        # error message
        if department_list is None:
            messagebox.showinfo("Info", "Keine Abteilungen vorhanden.")
            return
        # populates the finance_tab with department names
        for department in department_list:
            self.department_listbox.insert(tk.END, f"{department}")


    def show_department_balance(self):
        """This function is for the button which shows all departments"""
        import sqlite3
        self.department_balance_listbox.delete(0, tk.END)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # saves as variable the department that was clicked on
        department_selected = self.department_listbox.curselection()
        # converts it to text
        department_txt = ''.join(map(str, department_selected))
        # converts it to int and adds +1, so it equals id of the department
        department_int = int(department_txt)+1
        # gives out the balance of the department
        try:
            cursor.execute("""SELECT balance FROM departments
                                WHERE id = (?)""", (department_int,))
            department_balance = cursor.fetchall()
            # populates the balance_tab with balance of the department
            for balance in department_balance:
                self.department_balance_listbox.insert(tk.END, f"{balance}")
        except Exception as e:
            messagebox.showerror("Info", "Bitte wählen sie erst eine Abteilung aus.")
            return


    def create_finance_tab(self, tab):
        #This builds the UI elements for the table tab.

        # zeigt an Abteilungen
        ttk.Button(tab, text='Alle Abteilungen anzeigen',
                command=self.populate_departments).pack(pady=5)
        ttk.Button(tab, text='Kontostand der Abteilung anzeigen',
                command=self.show_department_balance).pack(pady=5)

        # box with departments
        ttk.Label(tab, text='Abteilungen:').pack(pady=5)
        self.department_listbox = tk.Listbox(tab, height=10, width=50)
        self.department_listbox.pack(pady=10)

        # box with department money
        ttk.Label(tab, text='Kontostand der Abteilung:').pack(pady=5)
        self.department_balance_listbox = tk.Listbox(tab, height=2, width=50)
        self.department_balance_listbox.pack(pady=10)



    def open_main_window(self, role):
        """This creates and shows the main window."""
        main_window = tk.Tk()
        main_window.title("Vereinskassensystem")
        self.center_window(main_window, 1050, 800)

        tab_control = ttk.Notebook(main_window)

        accessible_tabs = self.get_accessible_tabs(role)
        for tab_name in accessible_tabs:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=tab_name)
            ttk.Label(tab, text=f"Dies ist der Bereich: {tab_name}",
                      font=("Arial", 14)).pack(pady=20)

            if tab_name == "Abteilungen hinzufügen" and role == "Admin":
                self.add_department_tab(tab)
            if role == "Admin" and tab_name == "Admin-Einstellungen":
                self.create_admin_settings_tab(tab)
            # populate_finance_tab Aufruf
            if tab_name == "Finanzen":
                if role == "Admin" or "Kassenwart":
                    self.create_finance_tab(tab)

        tab_control.pack(expand=1, fill="both")
        main_window.mainloop()

    def get_accessible_tabs(self, role):
        """Gives back the accessible tabs based on user role."""
        if role == "Admin":
            return ["Dashboard", "Mitglieder", "Finanzen", "Berichte",
                    "Abteilungen hinzufügen", "Admin-Einstellungen"]
        elif role == "Kassenwart":
            return ["Dashboard", "Mitglieder", "Finanzen"]
        elif role == "Finanz-Viewer":
            return ["Dashboard", "Berichte"]
        return []

    def open_login_window(self):
        """Creates the login-window."""
        def handle_login():
            username = username_entry.get()
            password = password_entry.get()

            role = self.user_manager.verify_login(username, password)
            if role:
                messagebox.showinfo("Erfolg",
                                    "Login erfolgreich!")
                login_window.destroy()
                self.open_main_window(role)
            else:
                messagebox.showerror("Fehler",
                                     "Ungültiger Benutzername"
                                     " oder Passwort.")

        login_window = tk.Tk()
        login_window.title("Login")
        self.center_window(login_window, 300, 200)

        ttk.Label(login_window, text="Benutzername:").pack(pady=5)
        username_entry = ttk.Entry(login_window)
        username_entry.pack(pady=5)

        ttk.Label(login_window, text="Passwort:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        login_button = ttk.Button(login_window, text="Login",
                                  command=handle_login)
        login_button.pack(pady=10)

        login_window.mainloop()

# Main Execution
if __name__ == "__main__":
    app = ApplicationUI()
    app.open_login_window()