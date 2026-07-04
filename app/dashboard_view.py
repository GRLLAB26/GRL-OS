import customtkinter as ctk
from tkinter import messagebox

from app.dashboard import get_inventory_summary


class DashboardApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🚀 GRL-OS")
        self.geometry("1200x700")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.build_ui()

    def build_ui(self):

        # ===== Sidebar =====

        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            sidebar,
            text="🚀 GRL-OS",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            sidebar,
            text="Gadgets Repair Lab",
            font=("Arial", 12)
        ).pack(pady=(0, 25))

        ctk.CTkButton(
            sidebar,
            text="🏠 Dashboard",
            width=180,
            command=self.show_dashboard
        ).pack(pady=5)

        ctk.CTkButton(
            sidebar,
            text="📦 Inventario",
            width=180,
            command=self.open_inventory
        ).pack(pady=5)

        ctk.CTkButton(
            sidebar,
            text="👥 Usuarios",
            width=180,
            command=self.open_users
        ).pack(pady=5)

        ctk.CTkButton(
            sidebar,
            text="🔧 Reparaciones",
            width=180,
            command=self.not_available
        ).pack(pady=5)

        ctk.CTkButton(
            sidebar,
            text="🛒 Ventas",
            width=180,
            command=self.not_available
        ).pack(pady=5)

        ctk.CTkButton(
            sidebar,
            text="📈 Reportes",
            width=180,
            command=self.not_available
        ).pack(pady=5)

        ctk.CTkButton(
            sidebar,
            text="⚙ Configuración",
            width=180,
            command=self.not_available
        ).pack(pady=5)

        # ===== Contenido =====

        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Arial", 28, "bold")
        ).pack(anchor="w", pady=15)

        try:
            summary = get_inventory_summary()

            ctk.CTkLabel(
                self.content,
                text=f"📦 Productos: {summary.product_count}",
                font=("Arial", 18)
            ).pack(anchor="w", pady=4)

            ctk.CTkLabel(
                self.content,
                text=f"📦 Existencias: {summary.total_quantity}",
                font=("Arial", 18)
            ).pack(anchor="w", pady=4)

            ctk.CTkLabel(
                self.content,
                text=f"💰 Valor Inventario: ${summary.total_value:,.2f}",
                font=("Arial", 18)
            ).pack(anchor="w", pady=4)

            ctk.CTkLabel(
                self.content,
                text=f"⚠ Bajo Stock: {len(summary.low_stock_products)}",
                font=("Arial", 18)
            ).pack(anchor="w", pady=4)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_inventory(self):

        try:
            from app.inventory.gui import run_inventory_gui

            self.destroy()
            run_inventory_gui()

        except Exception as e:
            messagebox.showerror("Inventario", str(e))

    def open_users(self):

        messagebox.showinfo(
            "Usuarios",
            "El módulo de Usuarios será integrado en el siguiente sprint."
        )

    def not_available(self):

        messagebox.showinfo(
            "GRL-OS",
            "Este módulo estará disponible próximamente."
        )


def run_dashboard():
    app = DashboardApp()
    app.mainloop()