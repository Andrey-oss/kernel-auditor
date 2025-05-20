import os

def check_root() -> bool:
    return os.getuid() == 0

def check_os() -> bool:
    return os.uname()[0] == 'Linux'