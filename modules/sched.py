import os
import subprocess

OS_PATH = '/sys/block'

def get_schedulers() -> dict:
    scheds = {}

    for device in os.listdir(OS_PATH):
        scheds[device] = [sched for sched in open(f"{OS_PATH}/{device}/queue/scheduler").read().split()]

    return scheds

def def_values() -> dict:
    values = {}

    for device in os.listdir(OS_PATH):
        subvalues = {}
        for value in os.listdir(f"{OS_PATH}/{device}/queue"):
            if value != "scheduler":
                if os.path.isfile(f"{OS_PATH}/{device}/queue/{value}"):
                    try:
                        subvalues[value] = open(f"{OS_PATH}/{device}/queue/{value}").read().splitlines()[0]
                    except Exception:
                        continue
                values[device] = subvalues

    return values

def set_sched(data):
    try:
        device = data['device']
        scheduler = data['scheduler']
    except Exception as e:
        return {"status": e}

    cmd = f'echo "{scheduler}" > /sys/block/{device}/queue/scheduler'
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0 or result.stderr:
        return {"status": "Permission denied! Make your sure that webservice has root access"}
    else:
        return {"status": "ok"}

def set_tun(data):
    errors = {}
    
    for k, v in data.items():    
        if k == 'device':
            pass
        else:
            result = subprocess.run(f'echo {v} > /sys/block/{data['device']}/queue/{k}', shell=True, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0 or result.stderr:
                errors[k] = result.stderr.splitlines()
    
    if len(errors) == 0:
        return {'status': 'ok'}

    return {'status': str(errors)}
