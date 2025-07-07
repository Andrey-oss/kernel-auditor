'''Module for config parsing'''

import sys
import json

def cfg_parser() -> dict:
    '''Parse settings.file'''

    try:
        with open('settings.json', "r+", encoding='utf-8') as cfg:
            cfg = json.load(cfg)
    except FileNotFoundError:
        sys.exit("[-] Settings file doesn't exist!")
    except PermissionError:
        sys.exit("[-] Settings file cannot be read due to permissions!")
    except IsADirectoryError:
        # Maybe useless, but let it be
        sys.exit("[-] Settings file is directory?")
    except IOError:
        sys.exit("[-] Input/Output error while reading settings file")

    return cfg
