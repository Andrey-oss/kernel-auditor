'''Module for checking neccessary requirements for stable work'''

import os

def check_root() -> bool:
    '''Check for root access'''

    return os.getuid() == 0

def check_os() -> bool:
    '''Check for operating system'''

    return os.uname()[0] == 'Linux'
