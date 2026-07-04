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
	p = argparse.ArgumentParser(prog="grl-os", description="GRL-OS CLI")
	sub = p.add_subparsers(dest="cmd")

	parser_create = sub.add_parser("create-user", help="Create a new user")
	parser_create.add_argument("--name", required=True)
	parser_create.add_argument("--email", required=True)

	sub.add_parser("list-users", help="List all users")

	parser_delete = sub.add_parser("delete-user", help="Delete a user by id")
	parser_delete.add_argument("--id", type=int, required=True)

	parser_update = sub.add_parser("update-user", help="Update a user by id")
	parser_update.add_argument("--id", type=int, required=True)
	parser_update.add_argument("--name", required=True)
	parser_update.add_argument("--email", required=True)

	args = p.parse_args()

	if args.cmd == "create-user":
		from app.crud import create_user as _create

		u = _create(args.name, args.email)
		print(f"Created user {u.id}: {u.name} <{u.email}>")
	elif args.cmd == "list-users":
		from app.crud import list_users as _list

		for u in _list():
			print(f"{u.id}: {u.name} <{u.email}>")
	elif args.cmd == "delete-user":
		from app.crud import delete_user as _delete

		ok = _delete(args.id)
		print("Deleted" if ok else "User not found")
	elif args.cmd == "update-user":
		from app.crud import update_user as _update

		u = _update(args.id, args.name, args.email)
		print(f"Updated user {u.id}: {u.name} <{u.email}>")
	else:
		# Fallback: print environment and versions
		print("GRL-OS starting (CLI)")
		print(f"Python: {sys.version.splitlines()[0]}")
		print(f"Working dir: {os.getcwd()}")
		print("Environment variables (sample):")
		for k in ("ENV", "GRL_CONFIG", "PATH"):
			print(f"  {k}={os.environ.get(k)!r}")

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
	"""Delegate GUI startup to `app.gui.run_gui()`; fallback to CLI on error."""
	try:
		from app.gui import run_gui as _run_gui

		logger.info("Starting GRL-OS (GUI mode)")
		_run_gui()
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

