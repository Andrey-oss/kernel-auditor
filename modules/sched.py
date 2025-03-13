from modules.run import run_cmd
import os

OS_PATH = '/sys/block'

def get_schedulers() -> dict:
    scheds = {}

    for device in os.listdir(OS_PATH):
        scheds[device] = [sched for sched in open(f"{OS_PATH}/{device}/queue/scheduler").read().split()]

    return scheds

def get_sched_values() -> dict:
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
                        cmd = f'echo "{value}" > {file_path}'
                        error = run_cmd(cmd)
                        if not error:
                            subvalues[key] = value

        values[device] = subvalues

    return values

def set_sched(device, scheduler) -> dict:
    '''try:
        device = data['device']
        scheduler = data['scheduler']
    except Exception as e:
        return {"status": e}'''

    cmd = f'echo "{scheduler}" > /sys/block/{device}/queue/scheduler'
    error = run_cmd(cmd)
    
    if error:
        return {"status": error}
    
    return {"status": "ok"}

def set_tun(data) -> dict:
    errors = {}
    
    for k, v in data.items():    
        if k != 'device':
            cmd = f'echo {v} > /sys/block/{data['device']}/queue/{k}'
            error = run_cmd(cmd)

            if error:
                errors[k] = error
    
    if not errors:
        return {'status': 'ok'}

    return {'status': str(errors)}
