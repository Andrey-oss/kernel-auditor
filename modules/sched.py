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

        for key in os.listdir(f"{OS_PATH}/{device}/queue"):
            if key != "scheduler":
                file_path = f"{OS_PATH}/{device}/queue/{key}"

                if os.path.isfile(file_path):
                    try:
                        value = open(file_path).read().strip()
                    except Exception:
                        pass
                    else:
                        result = subprocess.run(f'echo "{value}" > {file_path}', shell=True, stderr=subprocess.PIPE, text=True)
                        if result.returncode == 0:
                            subvalues[key] = value
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
        return {"status": result.stderr.strip()}
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
                errors[k] = result.stderr.strip()
    
    if len(errors) == 0:
        return {'status': 'ok'}

    return {'status': str(errors)}
