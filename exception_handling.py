# ----------------------- CORE UTILS ---------------------------
def is_exception(path, exceptions):
    for ex in exceptions:
        if ex in path:
            return True
    return False
