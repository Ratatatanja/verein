import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Setup SQLite Database
def setup_database():
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
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    if "role" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'Finanz-Viewer'")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin", "Admin"))
    conn.commit()
    conn.close()

# Verify Login Credentials
def verify_login(username, password):
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Add New User
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

# Center Window
def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Setup Admin Tabs
def setup_admin_tabs(tabs):
    def handle_add_department():
        dept_name = dept_name_entry.get()
        initial_balance = dept_balance_entry.get()
        
        if dept_name and initial_balance:
            try:
                initial_balance = float(initial_balance)
                success = add_department(dept_name, initial_balance)
                if success:
                    messagebox.showinfo("Erfolg", f"Abteilung '{dept_name}' wurde hinzugefügt.")
                else:
                    messagebox.showerror("Fehler", f"Abteilung '{dept_name}' existiert bereits.")
            except ValueError:
                messagebox.showerror("Fehler", "Der Kontostand muss eine Zahl sein.")
        else:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden.")

    ttk.Label(tabs[0], text="Abteilung hinzufügen", font=("Arial", 14)).pack(pady=10)
    ttk.Label(tabs[0], text="Abteilungsname:").pack(pady=5)
    dept_name_entry = ttk.Entry(tabs[0])
    dept_name_entry.pack(pady=5)

    ttk.Label(tabs[0], text="Startsaldo:").pack(pady=5)
    dept_balance_entry = ttk.Entry(tabs[0])
    dept_balance_entry.pack(pady=5)

    add_dept_button = ttk.Button(tabs[0], text="Abteilung hinzufügen", command=handle_add_department)
    add_dept_button.pack(pady=10)

# Setup Transactions Tab
def setup_transactions_tab(tabs):
    ttk.Label(tabs[1], text="Hier können Ein- und Auszahlungen getätigt werden.", font=("Arial", 14)).pack(pady=20)
    # Weitere Widgets und Funktionen hier hinzufügen

# Setup Overview Tab
def setup_overview_tab(tabs):
    ttk.Label(tabs[2], text="Übersicht der Kontostände.", font=("Arial", 14)).pack(pady=20)
    # Weitere Widgets und Funktionen hier hinzufügen

# Setup Reports Tab
def setup_reports_tab(tabs):
    ttk.Label(tabs[3], text="Berichte und Transaktionsverlauf.", font=("Arial", 14)).pack(pady=20)
    # Weitere Widgets und Funktionen hier hinzufügen

# Main App Window
def open_main_window(role):
    main_window = tk.Tk()
    main_window.title("Tabbed Interface App")
    center_window(main_window, 600, 400)

    tab_control = ttk.Notebook(main_window)

    tabs = []
    if role == "Admin":
        accessible_tabs = ["Abteilungen", "Transaktionen", "Übersicht", "Berichte", "Einstellungen"]
    elif role == "Kassenwart":
        accessible_tabs = ["Transaktionen", "Übersicht", "Berichte"]
    elif role == "Finanz-Viewer":
        accessible_tabs = ["Übersicht", "Berichte"]

    for tab_name in accessible_tabs:
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=tab_name)
        tabs.append(tab)

    # Funktionen je nach Tab hinzufügen
    if role == "Admin":
        setup_admin_tabs(tabs)
    if role in ["Admin", "Kassenwart"]:
        setup_transactions_tab(tabs)
    if role in ["Admin", "Kassenwart", "Finanz-Viewer"]:
        setup_overview_tab(tabs)
        setup_reports_tab(tabs)

    tab_control.pack(expand=1, fill="both")
    main_window.mainloop()

# Login Window
def open_login_window():
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        user_role = verify_login(username, password)
        if user_role:
            messagebox.showinfo("Login Success", "Welcome!")
            login_window.destroy()
            open_main_window(user_role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Login")
    center_window(login_window, 300, 200)

    ttk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = ttk.Entry(login_window)
    username_entry.pack(pady=5)

    ttk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(login_window, text="Login", command=handle_login)
    login_button.pack(pady=10)

    login_window.mainloop()

# Main Execution
if __name__ == "__main__":
    setup_database()
    open_login_window()
