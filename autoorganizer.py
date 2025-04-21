import os
import shutil
from datetime import datetime
from exception_handling import is_exception
from model import Config
from type_map import TYPE_MAP


def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    for category, extensions in TYPE_MAP.items():
        if ext in extensions:
            return category
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
    try:
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
                    # print(f"Moved: {file_path} -> {new_path}")
    except Exception as e:
        print(f"Error during file organization: {e}")
