__author__ = "5158850, Novgorodtseva, 8392145, Reich"

"""This file is responsible for creation of users and divisions"""

class Admin_Management:
    """
    includes functions:
    create_user(name, password, role, division=0)
    create_divisions(division)"""
    import tkinter
    roles = [admin, referent, treasurer]
    self.roles = roles


    def create_user(name, password, role, division=0):
        # name is input from interface
        # password is input from interface
        # role is picked from a list
        import tkinter as tk

        show_entry_fields():
        print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

        master = tk.Tk()
        tk.Label(master, 
                text="First Name").grid(row=0)
        tk.Label(master, 
                text="Last Name").grid(row=1)

        e1 = tk.Entry(master)
        e2 = tk.Entry(master)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)