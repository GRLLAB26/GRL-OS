"""Simple GUI to interact with the database (create and list users)."""
import tkinter as tk
import customtkinter as ctk

from .db import init_db, get_session
from .models import User


def run_gui():
    init_db()

    ctk.set_appearance_mode("System")
    root = ctk.CTk()
    root.geometry("600x420")
    root.title("GRL-OS — Users")

    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    form_frame = ctk.CTkFrame(container)
    form_frame.pack(fill="x", pady=(0, 8))

    name_var = tk.StringVar()
    email_var = tk.StringVar()

    name_entry = ctk.CTkEntry(form_frame, textvariable=name_var, placeholder_text="Name")
    email_entry = ctk.CTkEntry(form_frame, textvariable=email_var, placeholder_text="Email")
    name_entry.pack(fill="x", pady=6)
    email_entry.pack(fill="x", pady=6)


    list_frame = ctk.CTkFrame(container)
    list_frame.pack(fill="both", expand=True)

    # Use a tkinter Listbox for simplicity inside the CustomTkinter layout
    listbox = tk.Listbox(list_frame)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)


    def refresh_users():
        listbox.delete(0, tk.END)
        with get_session() as s:
            users = s.query(User).order_by(User.id).all()
            for u in users:
                listbox.insert(tk.END, f"{u.id}: {u.name} <{u.email}>")


    def create_user():
        name = name_var.get().strip()
        email = email_var.get().strip()
        if not name or not email:
            return
        with get_session() as s:
            u = User(name=name, email=email)
            s.add(u)
        name_var.set("")
        email_var.set("")
        refresh_users()


    btn_frame = ctk.CTkFrame(container)
    btn_frame.pack(fill="x", pady=8)

    create_btn = ctk.CTkButton(btn_frame, text="Create User", command=create_user)
    refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=refresh_users)
    create_btn.pack(side="left", padx=(0, 8))
    refresh_btn.pack(side="left")

    refresh_users()

    root.mainloop()
