from core.settings import cfg_parser
import os

cfg = cfg_parser()

def check_root() -> bool:
    if os.getuid() > 0:
        return False
    return True

def check_os() -> bool:
    if os.uname()[0] != 'Linux':
        return False
    return True