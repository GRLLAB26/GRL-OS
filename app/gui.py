"""Simple GUI to interact with the database (create and list users)."""
import re
import tkinter as tk
from tkinter import messagebox as tk_messagebox
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

    # Inline error label for validation messages
    error_label = ctk.CTkLabel(form_frame, text="", text_color="#ff3333")
    error_label.pack(fill="x", pady=(4, 0))

    def is_mx_validation_available() -> bool:
        try:
            import dns.resolver  # type: ignore
            return True
        except Exception:
            return False

    mx_validation_enabled = is_mx_validation_available()
    mx_status_label = ctk.CTkLabel(
        form_frame,
        text=f"MX validation: {'enabled' if mx_validation_enabled else 'disabled'}",
        text_color="#888888",
        anchor="w",
    )
    mx_status_label.pack(fill="x", pady=(4, 10))

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
        users = []
        from .crud import list_users as _list_users

        users = _list_users()
        for u in users:
            listbox.insert(tk.END, f"{u.id}: {u.name} <{u.email}>")


    selected_id = None


    def on_select(evt):
        nonlocal selected_id
        if not listbox.curselection():
            selected_id = None
            return
        idx = listbox.curselection()[0]
        text = listbox.get(idx)
        # text format: "{id}: {name} <{email}>"
        try:
            id_part = text.split(":", 1)[0]
            uid = int(id_part.strip())
            selected_id = uid
            # populate fields
            from .crud import get_user as _get_user

            u = _get_user(uid)
            if u:
                name_var.set(u.name)
                email_var.set(u.email)
                error_label.configure(text="")
        except Exception:
            selected_id = None


    def create_user():
        name = name_var.get().strip()
        email = email_var.get().strip()
        if not name or not email:
            return
        # validation
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            error_label.configure(text="Please enter a valid email address.")
            return

        # optional MX validation using dnspython if available
        domain = email.split("@", 1)[1]
        mx_checked = None
        try:
            import dns.resolver

            try:
                answers = dns.resolver.resolve(domain, "MX")
                mx_checked = len(answers) > 0
            except Exception:
                mx_checked = False
        except Exception:
            mx_checked = None

        if mx_checked is False:
            error_label.configure(text="Email domain has no MX records.")
            return
        if mx_checked is None:
            # dnspython not installed or lookup failed; inform but allow creation
            tk_messagebox.showinfo(
                "MX check skipped",
                "MX validation is unavailable (optional dnspython not installed). Proceeding with basic validation.",
            )

        from .crud import create_user as _create_user
        try:
            _create_user(name, email)
            error_label.configure(text="")
            tk_messagebox.showinfo("Success", "User created successfully.")
        except Exception as e:
            tk_messagebox.showerror("Error", f"Failed to create user: {e}")
        name_var.set("")
        email_var.set("")
        refresh_users()


    def update_user_cmd():
        nonlocal selected_id
        if not selected_id:
            return
        name = name_var.get().strip()
        email = email_var.get().strip()
        if not name or not email:
            return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            error_label.configure(text="Please enter a valid email address.")
            return

        domain = email.split("@", 1)[1]
        mx_checked = None
        try:
            import dns.resolver

            try:
                answers = dns.resolver.resolve(domain, "MX")
                mx_checked = len(answers) > 0
            except Exception:
                mx_checked = False
        except Exception:
            mx_checked = None

        if mx_checked is False:
            error_label.configure(text="Email domain has no MX records.")
            return
        if mx_checked is None:
            tk_messagebox.showinfo(
                "MX check skipped",
                "MX validation is unavailable (optional dnspython not installed). Proceeding with basic validation.",
            )

        from .crud import update_user as _update_user
        try:
            _update_user(selected_id, name, email)
            error_label.configure(text="")
            tk_messagebox.showinfo("Success", "User updated successfully.")
        except Exception as e:
            tk_messagebox.showerror("Error", f"Failed to update user: {e}")
        name_var.set("")
        email_var.set("")
        selected_id = None
        refresh_users()


    def delete_user_cmd():
        nonlocal selected_id
        if not selected_id:
            return
        # confirmation dialog
        resp = tk_messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected user?")
        if not resp:
            return
        from .crud import delete_user as _delete_user
        try:
            _delete_user(selected_id)
            tk_messagebox.showinfo("Success", "User deleted.")
        except Exception as e:
            tk_messagebox.showerror("Error", f"Failed to delete user: {e}")
        selected_id = None
        name_var.set("")
        email_var.set("")
        refresh_users()


    btn_frame = ctk.CTkFrame(container)
    btn_frame.pack(fill="x", pady=8)

    create_btn = ctk.CTkButton(btn_frame, text="Create User", command=create_user)
    update_btn = ctk.CTkButton(btn_frame, text="Update User", command=update_user_cmd)
    delete_btn = ctk.CTkButton(btn_frame, text="Delete User", command=delete_user_cmd)
    refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=refresh_users)
    inventory_btn = ctk.CTkButton(btn_frame, text="Open Inventory", fg_color="#1f6aa5", hover_color="#16629c")

    create_btn.pack(side="left", padx=(0, 8))
    update_btn.pack(side="left", padx=(0, 8))
    delete_btn.pack(side="left", padx=(0, 8))
    refresh_btn.pack(side="left", padx=(0, 8))
    inventory_btn.pack(side="left")

    def open_inventory():
        try:
            from .inventory.gui import run_inventory_gui as _run_inventory_gui
            root.destroy()
            _run_inventory_gui()
        except Exception as e:
            tk_messagebox.showerror("Error", f"Unable to open inventory dashboard: {e}")

    inventory_btn.configure(command=open_inventory)
    listbox.bind("<<ListboxSelect>>", on_select)

    refresh_users()

    root.mainloop()
