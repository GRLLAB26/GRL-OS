"""
GRL-OS Configuration
Gadgets Repair Lab Operating System
"""

from pathlib import Path

# =========================
# Información de la aplicación
# =========================

APP_NAME = "GRL-OS"
APP_DESCRIPTION = "Gadgets Repair Lab Operating System"

VERSION = "0.9.0 Alpha"
AUTHOR = "Jorge Flores"
COMPANY = "Gadgets Repair Lab"

# =========================
# Directorios
# =========================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
BACKUP_DIR = BASE_DIR / "backups"
LOG_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"

# =========================
# Base de datos
# =========================

DATABASE_NAME = "data.db"
DATABASE_PATH = BASE_DIR / DATABASE_NAME

# =========================
# Inventario
# =========================

LOW_STOCK_LIMIT = 5

# =========================
# Interfaz
# =========================

THEME = "dark"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# =========================
# Logs
# =========================

LOG_LEVEL = "INFO"

# =========================
# Próxima versión
# =========================

NEXT_VERSION = "1.0.0 Beta"