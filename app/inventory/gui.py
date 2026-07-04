"""Inventory dashboard GUI for GRL-OS."""
import re
import tkinter as tk
from tkinter import messagebox as tk_messagebox
import customtkinter as ctk

from app.db import init_db
from .product_repository import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)


def run_inventory_gui():
    init_db()

    ctk.set_appearance_mode("System")
    root = ctk.CTk()
    root.geometry("820x520")
    root.title("GRL-OS — Inventory Dashboard")

    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True, padx=14, pady=14)

    header_frame = ctk.CTkFrame(container)
    header_frame.pack(fill="x", pady=(0, 10))

    title = ctk.CTkLabel(header_frame, text="Inventory Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(side="left")

    summary_label = ctk.CTkLabel(header_frame, text="Cargando...")
    summary_label.pack(side="right")

    toolbar_frame = ctk.CTkFrame(container)
    toolbar_frame.pack(fill="x", pady=(0, 10))

    search_var = tk.StringVar()
    low_stock_filter = tk.BooleanVar(value=False)

    filter_label = ctk.CTkLabel(toolbar_frame, text="Search:")
    filter_entry = ctk.CTkEntry(toolbar_frame, textvariable=search_var, width=220)
    filter_button = ctk.CTkButton(toolbar_frame, text="Filter", width=90)
    clear_button = ctk.CTkButton(toolbar_frame, text="Clear", width=90)
    low_stock_button = ctk.CTkButton(toolbar_frame, text="Low stock", width=90)
    back_button = ctk.CTkButton(toolbar_frame, text="Back", width=90)

    filter_label.pack(side="left", padx=(0, 8))
    filter_entry.pack(side="left", padx=(0, 8))
    filter_button.pack(side="left", padx=(0, 8))
    clear_button.pack(side="left", padx=(0, 8))
    low_stock_button.pack(side="left", padx=(0, 8))
    back_button.pack(side="left")

    body_frame = ctk.CTkFrame(container)
    body_frame.pack(fill="both", expand=True)

    form_frame = ctk.CTkFrame(body_frame)
    form_frame.pack(side="left", fill="y", padx=(0, 12), pady=4)

    sku_var = tk.StringVar()
    name_var = tk.StringVar()
    description_var = tk.StringVar()
    quantity_var = tk.StringVar()
    price_var = tk.StringVar()

    ctk.CTkLabel(form_frame, text="SKU").pack(anchor="w", pady=(4, 0))
    sku_entry = ctk.CTkEntry(form_frame, textvariable=sku_var)
    sku_entry.pack(fill="x", pady=4)

    ctk.CTkLabel(form_frame, text="Name").pack(anchor="w", pady=(4, 0))
    name_entry = ctk.CTkEntry(form_frame, textvariable=name_var)
    name_entry.pack(fill="x", pady=4)

    ctk.CTkLabel(form_frame, text="Description").pack(anchor="w", pady=(4, 0))
    description_entry = ctk.CTkEntry(form_frame, textvariable=description_var)
    description_entry.pack(fill="x", pady=4)

    ctk.CTkLabel(form_frame, text="Quantity").pack(anchor="w", pady=(4, 0))
    quantity_entry = ctk.CTkEntry(form_frame, textvariable=quantity_var)
    quantity_entry.pack(fill="x", pady=4)

    ctk.CTkLabel(form_frame, text="Price").pack(anchor="w", pady=(4, 0))
    price_entry = ctk.CTkEntry(form_frame, textvariable=price_var)
    price_entry.pack(fill="x", pady=4)

    error_label = ctk.CTkLabel(form_frame, text="", text_color="#ff3333")
    error_label.pack(fill="x", pady=(8, 0))

    btn_frame = ctk.CTkFrame(form_frame)
    btn_frame.pack(fill="x", pady=10)

    create_btn = ctk.CTkButton(btn_frame, text="Create", width=90)
    update_btn = ctk.CTkButton(btn_frame, text="Update", width=90)
    delete_btn = ctk.CTkButton(btn_frame, text="Delete", width=90)
    create_btn.pack(side="left", padx=3)
    update_btn.pack(side="left", padx=3)
    delete_btn.pack(side="left", padx=3)

    list_frame = ctk.CTkFrame(body_frame)
    list_frame.pack(side="right", fill="both", expand=True, pady=4)

    listbox = tk.Listbox(list_frame, activestyle="none")
    listbox.pack(side="left", fill="both", expand=True, padx=(0, 4), pady=4)

    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y", pady=4)
    listbox.config(yscrollcommand=scrollbar.set)

    selected_id = None

    def clear_form():
        nonlocal selected_id
        selected_id = None
        sku_var.set("")
        name_var.set("")
        description_var.set("")
        quantity_var.set("")
        price_var.set("")
        error_label.configure(text="")

    filter_var = tk.StringVar()

    def product_status(p):
        if p.quantity <= 5:
            return "LOW"
        if p.quantity <= 20:
            return "MEDIUM"
        return "OK"

    def format_product(p):
        status = product_status(p)
        return f"{p.id}: {p.sku} — {p.name} ({p.quantity} @ ${p.price:.2f}) [{status}]"

    def refresh_products(products=None):
        all_products = list_products() if products is None else products
        listbox.delete(0, tk.END)
        for p in all_products:
            listbox.insert(tk.END, format_product(p))
            if product_status(p) == "LOW":
                listbox.itemconfig(tk.END, {'fg': '#ff5555'})

        low_stock = sum(1 for p in all_products if product_status(p) == "LOW")
        summary_label.configure(
            text=f"{len(all_products)} products · {sum(p.quantity for p in all_products)} units · ${sum(p.quantity * p.price for p in all_products):.2f} · {low_stock} low stock"
        )
        reorder_count = len([p for p in all_products if product_status(p) == "LOW"])
        if reorder_count:
            summary_label.configure(
                text=summary_label.cget("text") + f" · {reorder_count} reorder suggestions"
            )

    def parse_quantity(value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError("Quantity must be a whole number.")

    def parse_price(value: str) -> float:
        try:
            return float(value)
        except ValueError:
            raise ValueError("Price must be a number.")

    def validate_form():
        if not sku_var.get().strip() or not name_var.get().strip():
            raise ValueError("SKU and Name are required.")
        if not quantity_var.get().strip() or not price_var.get().strip():
            raise ValueError("Quantity and Price are required.")
        quantity = parse_quantity(quantity_var.get().strip())
        price = parse_price(price_var.get().strip())
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        return sku_var.get().strip(), name_var.get().strip(), description_var.get().strip(), quantity, price

    def apply_filter():
        query = search_var.get().strip().lower()
        products = list_products()
        if query:
            products = [
                p
                for p in products
                if query in p.sku.lower()
                or query in p.name.lower()
                or query in p.description.lower()
            ]
        if low_stock_filter.get():
            products = [p for p in products if product_status(p) == "LOW"]
        refresh_products(products)

    def clear_filter():
        search_var.set("")
        low_stock_filter.set(False)
        low_stock_button.configure(text="Low stock")
        refresh_products()

    def toggle_low_stock():
        low_stock_filter.set(not low_stock_filter.get())
        low_stock_button.configure(text="All" if low_stock_filter.get() else "Low stock")
        apply_filter()

    def on_back():
        root.destroy()

    filter_button.configure(command=apply_filter)
    clear_button.configure(command=clear_filter)
    low_stock_button.configure(command=toggle_low_stock)
    back_button.configure(command=on_back)

    def on_create():
        try:
            sku, name, description, quantity, price = validate_form()
            p = create_product(sku, name, description, quantity, price)
            tk_messagebox.showinfo("Created", f"Product created: {p.sku}")
            clear_form()
            refresh_products()
        except Exception as exc:
            error_label.configure(text=str(exc))

    def on_update():
        nonlocal selected_id
        if selected_id is None:
            error_label.configure(text="Select a product to update.")
            return
        try:
            sku, name, description, quantity, price = validate_form()
            p = update_product(selected_id, sku, name, description, quantity, price)
            if not p:
                raise ValueError("Product not found.")
            tk_messagebox.showinfo("Updated", f"Product updated: {p.sku}")
            clear_form()
            refresh_products()
        except Exception as exc:
            error_label.configure(text=str(exc))

    def on_delete():
        nonlocal selected_id
        if selected_id is None:
            error_label.configure(text="Select a product to delete.")
            return
        if not tk_messagebox.askyesno("Delete", "Delete selected product?"):
            return
        if delete_product(selected_id):
            tk_messagebox.showinfo("Deleted", "Product deleted.")
            clear_form()
            refresh_products()
        else:
            error_label.configure(text="Product not found.")

    def on_select(event):
        nonlocal selected_id
        selection = listbox.curselection()
        if not selection:
            return
        item = listbox.get(selection[0])
        try:
            selected_id = int(item.split(":", 1)[0])
        except ValueError:
            selected_id = None
            return
        product = get_product(selected_id)
        if product:
            sku_var.set(product.sku)
            name_var.set(product.name)
            description_var.set(product.description)
            quantity_var.set(str(product.quantity))
            price_var.set(str(product.price))
            error_label.configure(text="")

    create_btn.configure(command=on_create)
    update_btn.configure(command=on_update)
    delete_btn.configure(command=on_delete)
    listbox.bind("<<ListboxSelect>>", on_select)

    refresh_products()
    root.mainloop()
