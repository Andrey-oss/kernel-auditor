'''Module for working with scheduler settings'''

from pathlib import Path
import os
from decorators.data_validators import validate_data_type, validate_data_length
from modules.run import run_cmd

OS_PATH = '/sys/block'

def get_schedulers() -> dict:
    """
    Returns all available schedulers (no argument required):
    """

    scheds = {}

    for device in os.listdir(OS_PATH):
        try:
            sched_path = Path(OS_PATH) / device / "queue" / "scheduler"
            with open(sched_path, encoding='utf-8') as f:
                scheds[device] = f.read().split()
        except FileNotFoundError:
            pass

    return scheds

def get_sched_values() -> dict:
    """
    Returns values from available schedulers (no argument required):

    Output (for example): {
        'nvme0n1': {'io_poll_delay': '-1', 'io_timeout': '30000'},
        'sda': {'io_poll_delay': '-1', 'io_timeout': '30000'}
    }
    """

    values = {}

    for device in os.listdir(OS_PATH):
        subvalues = {}
        list_dir = Path(OS_PATH) / device / "queue"

        for key in os.listdir(list_dir):
            if key != "scheduler":
                file_path = Path(OS_PATH) / device / "queue" / key

                if os.path.isfile(file_path):
                    try:
                        with open(file_path, encoding='utf-8') as v:
                            value = v.read().strip()
                    except (PermissionError, OSError):
                        pass
                    else:
                        cmd = f'echo "{value}" > {file_path}'
                        error = run_cmd(cmd)
                        if not error:
                            subvalues[key] = value

        values[device] = subvalues

    return values

@validate_data_type(dict)
@validate_data_length(2, mode='exact')
def set_sched(data: dict) -> dict:
    """
    Set drive scheduler. API usage (example of function call):
    
    {
        'device': 'sda',
        'scheduler': 'none'
    }
    """

    try:
        device = data['device']
        scheduler = data['scheduler']
    except KeyError:
        return {
            'status': 'error',
            'message': 'Device name or scheduler not found!'
        }

    sched_path = Path(OS_PATH) / device / "queue" / "scheduler"

    cmd = f'echo "{scheduler}" > {sched_path}'
    error = run_cmd(cmd)

    if not error:
        return {
            'status': 'success',
            'message': 'Scheduler has been changed successfully!'
        }

    return {
        'status': 'error',
        'message': error
    }

@validate_data_type(dict)
@validate_data_length(2, mode='min')
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

    try:
        device = data['device']
    except KeyError:
        return {
            'status': 'error',
            'message': 'No device specified'
        }

    errors = {}

    for param, value in data.items():
        sched_param = Path(OS_PATH) / device / "queue" / param
        if param != 'device':
            cmd = f'echo {value} > {sched_param}'

            error = run_cmd(cmd)

            if error:
                errors[param] = error

    if not errors:
        return {
            'status': 'success',
            'message': 'New tunning applied with no errors!'
        }

    return {
        'status': 'error',
        'message': str(errors)
    }
