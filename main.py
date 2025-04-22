import os
from autoorganizer import organize_files
from model import Config
from pathlib import Path


# ----------------------- CLI INTERFACE ---------------------------
def cli():
    base_dir = os.getcwd()

    print("Choose sorting strategy:")
    print("1. Type")
    print("2. Date")
    print("3. Pattern")
    sort_input = input("Enter number: ").strip()
    sort_by_map = {"1": "type", "2": "date", "3": "pattern"}
    sort_by = sort_by_map.get(sort_input, "type")

    # depth_input = input("Enter depth level (default 1): ").strip()
    # depth = int(depth_input) if depth_input.isdigit() else 1

    ex_input = input("Enter exceptions (comma-separated): ").strip()
    exceptions = [e.strip() for e in ex_input.split(",") if e.strip()]

    config = Config(sort_by=sort_by, depth=1, exceptions=exceptions)
    organize_files(base_dir, config)


if __name__ == "__main__":
    cli()
