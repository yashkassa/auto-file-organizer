import os
import shutil
import mimetypes
from datetime import datetime

# ----------------------- CONFIG STRUCTURE ---------------------------


class Config:
    def __init__(self, sort_by='type', depth=1, exceptions=None):
        self.sort_by = sort_by
        self.depth = depth
        self.exceptions = exceptions if exceptions else []


# ----------------------- CORE UTILS ---------------------------
def is_exception(path, exceptions):
    for ex in exceptions:
        if ex in path:
            return True
    return False


def get_file_type(file_path):
    type_guess, _ = mimetypes.guess_type(file_path)
    if type_guess:
        return type_guess.split('/')[0].capitalize()
    return "Others"


def get_file_date(file_path):
    try:
        mtime = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(mtime)
        return date.strftime("%Y-%m")  # Year-Month format
    except Exception:
        return "Unknown"


def get_pattern_folder(file_name):
    name = file_name.lower()
    if "invoice" in name:
        return "Invoices"
    elif "resume" in name:
        return "Resumes"
    elif "report" in name:
        return "Reports"
    else:
        return "Misc"

# ----------------------- ORGANIZATION LOGIC ---------------------------


def organize_files(base_dir, config: Config):
    for root, dirs, files in os.walk(base_dir):
        if config.depth == 1 and root != base_dir:
            continue

        if is_exception(root, config.exceptions):
            continue

        for file in files:
            file_path = os.path.join(root, file)

            if is_exception(file_path, config.exceptions):
                continue

            if not os.path.isfile(file_path):
                continue

            if config.sort_by == "type":
                folder_name = get_file_type(file_path)
            elif config.sort_by == "date":
                folder_name = get_file_date(file_path)
            elif config.sort_by == "pattern":
                folder_name = get_pattern_folder(file)
            else:
                folder_name = "Unsorted"

            target_dir = os.path.join(base_dir, folder_name)
            os.makedirs(target_dir, exist_ok=True)

            new_path = os.path.join(target_dir, file)
            if file_path != new_path:
                shutil.move(file_path, new_path)
                print(f"Moved: {file_path} -> {new_path}")

# ----------------------- CLI INTERFACE ---------------------------


def cli():
    base_dir = input("Enter the directory to organize: ").strip()

    print("Choose sorting strategy:")
    print("1. Type")
    print("2. Date")
    print("3. Pattern")
    sort_input = input("Enter number: ").strip()
    sort_by_map = {"1": "type", "2": "date", "3": "pattern"}
    sort_by = sort_by_map.get(sort_input, "type")

    depth_input = input("Enter depth level (default 1): ").strip()
    depth = int(depth_input) if depth_input.isdigit() else 1

    ex_input = input("Enter exceptions (comma-separated): ").strip()
    exceptions = [e.strip() for e in ex_input.split(",") if e.strip()]

    config = Config(sort_by=sort_by, depth=depth, exceptions=exceptions)
    organize_files(base_dir, config)


if __name__ == "__main__":
    cli()
