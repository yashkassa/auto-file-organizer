import os
import fnmatch
import re


def is_file_to_be_ignored(path, exceptions):
    filename = os.path.basename(path).lower()
    normalized_path = os.path.normpath(path).lower()

    for pattern in exceptions:
        pattern = pattern.strip().lower()

        # Regex pattern match
        if pattern.startswith("re:"):
            try:
                regex = pattern[3:]
                if re.search(regex, normalized_path) or re.search(regex, filename):
                    return True
            except re.error as e:
                print(f"Invalid regex in pattern '{pattern}': {e}")
                continue

        # Wildcard and exact match
        if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(normalized_path, pattern):
            return True

    return False


# # ----------------------- CORE UTILS ---------------------------
# def is_exception(path, exceptions):
#     for ex in exceptions:
#         if ex in path:
#             return True
#     return False
