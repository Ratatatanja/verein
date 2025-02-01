"""This file is responsible for the UI."""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"

import tkinter as tk
from tkinter import ttk, messagebox
from user_management import UserManager
from database import DatabaseManager
from department_management import DepartmentManager
from finance import Finance

class ApplicationUI:
    """This is the class of the App"""
    def __init__(self, db_name="app_data.db"):
        self.db_name = db_name
        self.db_manager = DatabaseManager()
        self.department_manager = DepartmentManager(self.db_manager)
        self.user_manager = UserManager(self.db_manager)
        self.fin = Finance()
        self.db_manager.setup_database()
        self.user_role = None

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
        """This creates the Tab User Management."""
        def handle_add_user():
            """This handles the process of adding a user."""
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
        role_combobox = ttk.Combobox(parent_tab, state="readonly",
                                     values=["Admin",
                                                         "Kassenwart",
                                                         "Finanz-Viewer"])
        role_combobox.pack(pady=5)

        add_user_button = ttk.Button(parent_tab,
                                     text="Benutzer hinzufügen",
                                     command=handle_add_user)
        add_user_button.pack(pady=10)


    def show_department_balance(self):
        """This function is for the button which shows the balance of the account
        of a particular department"""
        import sqlite3
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            self.department = self.department_combobox.get()
            if self.department == "":
                messagebox.showerror("Info", "Bitte wählen sie erst eine "
                                 "Abteilung aus.")
                return
            cursor.execute("""SELECT balance FROM departments
                                WHERE name = (?)""", (self.department,))
            department_balance = cursor.fetchall()
            # populates the balance_tab with balance of the department
            for balance in department_balance:
                self.department_balance_listbox.insert(tk.END, f"{balance[0]}€")
        except Exception as e:
            messagebox.showerror("Info", "Bitte wählen sie erst eine Abteilung aus.")
            return


    def deposit_money(self):
        """This function deposits money for the account"""
        # saves as variable the department that was clicked on
        try:
            # saves as variable the department that was chosen
            self.department = self.department_combobox.get()
            if self.department == "":
                messagebox.showerror("Info", "Bitte wählen sie erst eine "
                                 "Abteilung aus.")
                return
            self.deposit_window = tk.Toplevel()
            # window title
            self.deposit_window.title("Eingabe")
            # sets the geometry
            self.center_window(self.deposit_window, 600, 200)
            # text of the window
            tk.Label(self.deposit_window, text=f"Geben sie ein wie viel sie "
                f"in die Abteilung {self.department} einzahlen wollen").pack()
            self.amount_entry = ttk.Entry(self.deposit_window)
            self.amount_entry.pack(pady=5)
            deposit_button = ttk.Button(self.deposit_window, text="Geld einzahlen",
                                     command=self.handle_deposit)
            deposit_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Info", "Bitte geben sie einen"
                                 "gültigen Betrag ein.")
            return


    def handle_deposit(self):
        try:
            self.deposit_amount = self.amount_entry.get()
            no_point_amount = self.deposit_amount.replace('.', '', 1)
            print("no point",no_point_amount)
            if no_point_amount.isdigit() == False:
                messagebox.showerror(
                        "Fehler", "Der Betrag muss eine Zahl sein."
                        " Nachkommastellen sollen mit Punkt abgetrennt werden.")
                return
            if float(self.deposit_amount) < 0:
                messagebox.showerror("Info", "Bitte geben sie einen nicht negativen Betrag ein.")
                return
            self.fin.add_balance(self.department, float(self.deposit_amount))
            messagebox.showinfo("Info",
                                f"Sie haben erfolgreich {self.deposit_amount} hinzugefügt.")
            self.deposit_window.destroy()
        except Exception as e:
            messagebox.showerror("Info", "Fehler beim Einzahlen von Geld.")
            return


    def withdraw_money(self):
        """This function withdraws money from the account"""
        try:
            # saves as variable the department that was chosen
            self.department = self.department_combobox.get()
            if self.department == "":
                messagebox.showerror("Info", "Bitte wählen sie erst eine "
                                 "Abteilung aus.")
                return
            self.withdraw_window = tk.Toplevel()
            # window title
            self.withdraw_window.title("Eingabe")
            # sets the geometry
            self.center_window(self.withdraw_window, 600, 200)
            # text of the window
            tk.Label(self.withdraw_window, text=f"Geben sie ein wie viel "
                     "Geld sie von der Abteilung {self.department}"
                     " abheben wollen").pack()
            self.withdraw_entry = ttk.Entry(self.withdraw_window)
            self.withdraw_entry.pack(pady=5)
            withdraw_button = ttk.Button(self.withdraw_window, text="Geld abheben",
                                     command=self.handle_withdraw)
            withdraw_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Info", "Bitte geben sie einen "
                                 "gültigen Betrag ein.")
            return

    def handle_withdraw(self):
        """This function triggers when clicking on the button: "Geld abheben"
        inside the withdraw_money() function.
        It gets the amount of money from the entry box and triggers the
        finance function called reduce_money()."""
        try:
            self.withdraw_amount = self.withdraw_entry.get()
            no_point_amount = self.withdraw_amount.replace('.', '', 1)
            print("no point",no_point_amount)
            if no_point_amount.isdigit() == False:
                messagebox.showerror(
                        "Fehler", "Der Betrag muss eine Zahl sein."
                        " Nachkommastellen sollen mit Punkt abgetrennt werden.")
                return
            if float(self.withdraw_amount) < 0:
                messagebox.showerror("Info", "Bitte geben sie einen nicht negativen Betrag ein.")
                return
            self.fin.reduce_balance(self.department, float(self.withdraw_amount))
            messagebox.showinfo("Info",
                                f"Sie haben erfolgreich {self.withdraw_amount} abgehoben.")
            self.withdraw_window.destroy()
        except Exception as e:
            messagebox.showerror("Info", "Dieser Betrag ist zu hoch. Geben sie kleineren Betrag ein.")
            return

            # Checks if withdraw was a success
            success = self.fin.reduce_balance(self.department,
                                              self.withdraw_amount)
            if success:
                messagebox.showinfo("Info",
                                    f"Sie haben erfolgreich {self.withdraw_amount} abgehoben.")
                self.withdraw_window.destroy()
            else:
                messagebox.showerror("Info",
                                     "Abhebung fehlgeschlagen. Nicht genug Guthaben!")
        except Exception as e:
            messagebox.showerror("Info", "Fehler bei der Abhebung.")

    def transfer_money(self):
        """This function transfers money from one department to another"""
        # importing sqlite and setting it up
        import sqlite3
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # saves as variable the department that was chosen
            self.department = self.department_combobox.get()
            print(self.department)
            if self.department == "":
                messagebox.showerror("Info", "Bitte wählen sie erst eine "
                                 "Abteilung aus.")
                return
            self.transfer_window = tk.Toplevel()
            # window title
            self.transfer_window.title("Eingabe")
            # sets the geometry
            self.center_window(self.transfer_window, 600, 200)
            cursor.execute("""SELECT name FROM departments""")
            department_list = cursor.fetchall()
            ttk.Label(self.transfer_window, text="Wählen sie aus zu welcher "
                      "Abteilungen Sie das Geld überweisen wollen:").pack(pady=5)
            self.department_combobox = ttk.Combobox(self.transfer_window, state="readonly",
                                                    values=department_list)
            self.department_combobox.pack(pady=5)

            # text of the window
            tk.Label(self.transfer_window, text="Geben sie ein wieviel Geld Sie von "
                     f"der Abteilung {self.department} zu einer anderen Abteilung"
                      " überweisen wollen").pack()
            self.transfer_entry = ttk.Entry(self.transfer_window)
            self.transfer_entry.pack(pady=5)
            transfer_button = ttk.Button(self.transfer_window, text="Geld überweisen",
                                     command=self.handle_transfer)
            transfer_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Info", "Diese Operation wurde abgebrochen")
            return

    def handle_transfer(self):
        """Sends money from one departmenmt to another."""
        try:
            self.transfer_amount = self.transfer_entry.get()
            no_point_amount = self.transfer_amount.replace('.', '', 1)
            if no_point_amount.isdigit() == False:
                messagebox.showerror(
                        "Fehler", "Der Betrag muss eine Zahl sein."
                        " Nachkommastellen sollen mit Punkt abgetrennt werden.")
                return
            if float(self.transfer_amount) < 0:
                messagebox.showerror("Info", "Bitte geben sie einen nicht negativen Betrag ein.")
                return
            # the department to which the money is transferred to
            self.end_department = self.department_combobox.get()
            if self.end_department == self.department:
                messagebox.showerror("Info", "Bitte wählen sie eine "
                                     "Abteilung aus, welche nicht identisch "
                                     "mit der Originalabteilung ist.")
                return
            status = self.fin.reduce_balance(self.department, float(self.transfer_amount))
            if status == False:
                messagebox.showerror("Info", "Dieser Betrag ist zu hoch. Geben sie kleineren Betrag ein.")
                return
            self.fin.add_balance(self.end_department, self.transfer_amount)
            messagebox.showinfo("Info",
                                f"Sie haben erfolgreich {self.transfer_amount} überwiesen\
                                    von {self.department} nach {self.end_department}.")
            self.transfer_window.destroy()
        except Exception as e:
            messagebox.showerror("Info", "Bitte geben sie eine Zahl ein als Betrag.")
            return


    def create_finance_tab(self, tab):
        """This builds the UI elements for the table tab."""

        # alle Buttons
        ttk.Button(tab, text='Kontostand der Abteilung anzeigen',
                command=self.show_department_balance).pack(pady=5)
        ttk.Button(tab, text='Geld einzahlen in das Abteilungskonto',
                command=self.deposit_money).pack(pady=5)
        ttk.Button(tab, text='Geld abheben vom Abteilungskonto',
                command=self.withdraw_money).pack(pady=5)
        ttk.Button(tab, text='Geld überweisen vom Abteilungskonto',
                command=self.transfer_money).pack(pady=5)

        # importing sqlite
        import sqlite3
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # creates a dropdown with all the department names
        cursor.execute("""SELECT name FROM departments""")
        department_list = cursor.fetchall()
        ttk.Label(tab, text="Abteilungen:").pack(pady=5)
        self.department_combobox = ttk.Combobox(tab, state="readonly", values=department_list)
        self.department_combobox.pack(pady=5)

        # box with department money
        ttk.Label(tab, text='Kontostand der Abteilung:').pack(pady=5)
        self.department_balance_listbox = tk.Listbox(tab, height=2, width=50)
        self.department_balance_listbox.pack(pady=10)

    def create_transaction_history_tab(self, tab):
        """This creates the UI of the Transactin history tab."""
        ttk.Label(tab, text="Transaktionshistorie", font=("Arial", 14)).pack(
            pady=10)

        self.transaction_tree = ttk.Treeview(tab, columns=(
            "id", "department", "operation", "amount", "balance"),
                                             show="headings")

        self.transaction_tree.heading("id", text="#")
        self.transaction_tree.column("id", width=40, anchor="center")

        self.transaction_tree.heading("department", text="Abteilung")
        self.transaction_tree.heading("operation", text="Operation")
        self.transaction_tree.heading("amount", text="Betrag")
        self.transaction_tree.heading("balance", text="Kontostand")

        self.transaction_tree.pack(pady=10, fill="both", expand=True)

        ttk.Button(tab, text="Historie aktualisieren",
                   command=self.load_transaction_history).pack(pady=5)

        if self.user_role == "Admin":
            ttk.Button(tab, text="CSV exportieren",
                       command=self.export_to_csv).pack(pady=5)

        self.load_transaction_history()

    def load_transaction_history(self):
        """This loads the transactionhistory."""
        records = self.fin.get_transaction_history()

        for row in self.transaction_tree.get_children():
            self.transaction_tree.delete(row)

        for record in records:
            self.transaction_tree.insert("", "end",
                                         values=record)  # Kein timestamp mehr

    def export_to_csv(self):
        """This exports the Transactionhistory as csv."""
        import csv
        filename = "transaction_history.csv"
        records = self.fin.get_transaction_history()

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Abteilung", "Operation", "Betrag", "Kontostand",
                             "Datum/Zeit"])
            writer.writerows(records)

        messagebox.showinfo("Erfolg",
                            f"Transaktionshistorie wurde als {filename} gespeichert.")

    def open_main_window(self, role):
        """This creates and shows the main window."""
        self.user_role = role

        main_window = tk.Tk()
        main_window.title("Vereinskassensystem")
        self.center_window(main_window, 1050, 800)

        tab_control = ttk.Notebook(main_window)

        accessible_tabs = self.get_accessible_tabs(role)
        for tab_name in accessible_tabs:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=tab_name)

            if tab_name == "Abteilungen hinzufügen" and role == "Admin":
                self.add_department_tab(tab)
            elif tab_name == "User Management" and role == "Admin":
                self.create_admin_settings_tab(tab)
            elif tab_name == "Finanzen":
                self.create_finance_tab(tab)
            elif tab_name == "Transaktionshistorie":
                self.create_transaction_history_tab(tab)

        tab_control.pack(expand=1, fill="both")
        main_window.mainloop()

    # In der ApplicationUI-Klasse (UI.py)
    def get_accessible_tabs(self, role):
        """This gives back the tabs based on user role."""
        if role == "Admin":
            return ["Finanzen", "Transaktionshistorie",
                    "Abteilungen hinzufügen", "User Management"]
        elif role == "Kassenwart":
            return ["Finanzen", "Transaktionshistorie"]
        elif role == "Finanz-Viewer":
            return ["Finanzen", "Transaktionshistorie"]
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