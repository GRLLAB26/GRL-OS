import sys
import os
import logging
import argparse
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("grl-os")


def get_version(module_name, attr_names=("__version__", "version")):
	try:
		module = __import__(module_name)
	except Exception:
		return "not installed"
	for attr in attr_names:
		v = getattr(module, attr, None)
		if v:
			return str(v)
	return "unknown"


def run_cli():
	"""Simple CLI runner that prints environment and dependency versions."""
	logger.info("Starting GRL-OS (CLI mode)")
	print("GRL-OS starting (CLI)")
	print(f"Python: {sys.version.splitlines()[0]}")
	print(f"Working dir: {os.getcwd()}")
	print("Environment variables (sample):")
	for k in ("ENV", "GRL_CONFIG", "PATH"):
		print(f"  {k}={os.environ.get(k)!r}")

	# Report a few dependency versions
	deps = {
		"customtkinter": "customtkinter",
		"sqlalchemy": "sqlalchemy",
		"pandas": "pandas",
		"openpyxl": "openpyxl",
		"Pillow": "PIL",
		"selenium": "selenium",
		"webdriver-manager": "webdriver_manager",
		"python-dotenv": "dotenv",
	}
	print("\nDependency versions:")
	for name, mod in deps.items():
		print(f"  {name}: {get_version(mod)}")


def run_gui():
	"""Attempt to start a tiny CustomTkinter window. Falls back to CLI on failure."""
	try:
		import customtkinter as ctk

		ctk.set_appearance_mode("System")
		app = ctk.CTk()
		app.geometry("400x120")
		app.title("GRL-OS")

		label = ctk.CTkLabel(app, text="GRL-OS running (GUI)")
		label.pack(pady=20)

		btn = ctk.CTkButton(app, text="Quit", command=app.destroy)
		btn.pack(pady=6)

		logger.info("Starting GRL-OS (GUI mode)")
		app.mainloop()
	except Exception as e:
		logger.exception("Failed to start GUI - falling back to CLI: %s", e)
		run_cli()


def main(argv=None):
	p = argparse.ArgumentParser(description="GRL-OS launcher")
	p.add_argument("--gui", action="store_true", help="Start GUI instead of CLI")
	args = p.parse_args(argv)

	if args.gui:
		run_gui()
	else:
		run_cli()


if __name__ == "__main__":
	main()

