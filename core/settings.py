import json

def cfg_parser() -> dict:
    try:
        with open('settings.json', "r+") as cfg:
            cfg = json.load(cfg)
    except Exception as e:
        exit("[-] Settings file doesn't exist!")
    else:
        return cfg