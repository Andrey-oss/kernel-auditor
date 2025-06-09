from modules.run import run_cmd
import os

OS_PATH = '/sys/block'

def get_schedulers() -> dict:
    """
    Returns all available schedulers (no argument required):
    """

    scheds = {}

    for device in os.listdir(OS_PATH):
        try:
           scheds[device] = [sched for sched in open(f"{OS_PATH}/{device}/queue/scheduler", encoding='utf-8').read().split()]
        except FileNotFoundError:
           pass

    return scheds

def get_sched_values() -> dict:
    """
    Returns values from available schedulers (no argument required):
    """

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

def set_sched(data: dict) -> dict:
    """
    Set drive scheduler. API usage (example of function call):
    
    {
        'device': 'sda'
        'scheduler': 'none'
    }
    """

    device = data['device']
    scheduler = data['scheduler']
    
    cmd = f'echo "{scheduler}" > /sys/block/{device}/queue/scheduler'
    error = run_cmd(cmd)
    
    if not error:
        return {'status': 'ok', 'message': 'Scheduler has been changed successfully!'}
    
    return {'status': 'error', 'message': error}

def set_tun(data: dict) -> dict:
    """
    Set new settings for scheduler. API usage (example of function call):

    {
        'device': 'sda',
        'nr_requests': '128'
        'read_ahead_kb': '128'
        'max_sectors_kb': '256'
        'io_timeout': '30000'
    }
    """

    errors = {}
    
    for param, value in data.items():    
        if param != 'device':
            cmd = f'echo {value} > /sys/block/{data['device']}/queue/{param}'
            error = run_cmd(cmd)

            if error:
                errors[param] = error
    
    if not errors:
        return {'status': 'ok', 'message': 'New tunning applied with no errors!'}

    return {'status': 'error', 'message': str(errors)}
