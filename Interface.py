"""
This is the UI for the Program.
"""

__author__ = "5158850, Novgorodtseva, 8392145, Reich"



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
def update_user_role(username, new_role):
    conn = sqlite3.connect("app_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
    conn.commit()
    conn.close()
    print(f"Updated role for user '{username}' to '{new_role}'")



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

# Main App Window
def open_main_window(role):
    print(f"User role detected: {role}")  # Debugging
    main_window = tk.Tk()
    main_window.title("Tabbed Interface App")
    main_window.geometry("1050x800")

    # Create Tab Control
    tab_control = ttk.Notebook(main_window)

    # Create Tabs Based on Role
    tabs = []
    if role == "Admin":
        accessible_tabs = 5
    elif role == "Kassenwart":
        accessible_tabs = 3
    elif role == "Finanz-Viewer":
        accessible_tabs = 2
    else:
        accessible_tabs = 0
    

    for i in range(1, accessible_tabs + 1):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=f"Tab {i}")
        ttk.Label(tab, text=f"This is Tab {i}", font=("Arial", 14)).pack(pady=20)
        tabs.append(tab)
    
    """ # Only Admin role enabled
    if role == "Admin":
        accessible_tabs = 5
        tabs = []
        for i in range(1, accessible_tabs + 1):
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=f"Tab {i}")
            ttk.Label(tab, text=f"This is Tab {i}", font=("Arial", 14)).pack(pady=20)
            tabs.append(tab)"""


    # Add Admin Panel in Tab 5 for Admin Role
    if role == "Admin" and len(tabs) == 5:
        def handle_add_user():
            new_username = username_entry.get()
            new_password = password_entry.get()
            new_role = role_combobox.get()

            if new_username and new_password and new_role:
                if add_new_user(new_username, new_password, new_role):
                    messagebox.showinfo("Success", f"User '{new_username}' added successfully.")
                    username_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    role_combobox.set("")
                else:
                    messagebox.showerror("Error", f"Username '{new_username}' already exists.")
            else:
                messagebox.showerror("Error", "All fields are required.")

        ttk.Label(tabs[4], text="Add New User", font=("Arial", 14)).pack(pady=10)
        ttk.Label(tabs[4], text="New Username:").pack(pady=5)
        username_entry = ttk.Entry(tabs[4])
        username_entry.pack(pady=5)

        ttk.Label(tabs[4], text="New Password:").pack(pady=5)
        password_entry = ttk.Entry(tabs[4],) #show'*' entfernt
        password_entry.pack(pady=5)

        ttk.Label(tabs[4], text="Role:").pack(pady=5)
        role_combobox = ttk.Combobox(tabs[4], values=["Admin", "Kassenwart", "Finanz-Viewer"])
        role_combobox.pack(pady=5)

        add_user_button = ttk.Button(tabs[4], text="Add User", command=handle_add_user)
        add_user_button.pack(pady=10)

    tab_control.pack(expand=1, fill="both")
    main_window.mainloop()

# for debugging/test
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
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        user_role = verify_login(username, password)
        if user_role:
            messagebox.showinfo("Login Success", "Welcome!")
            login_window.destroy()
            open_main_window(user_role)  # Pass the role to the main window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

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
    update_user_role("admin", "Admin")  # Aktualisiere die Rolle für den Admin
