'''Module which works with CPU'''

import os
import re
from pathlib import Path
from decorators.data_validators import validate_data_type, validate_data_length
from modules.run import run_cmd
from modules.helpers import list_intersection, str_intersection, get_all_merged_params

OS_PATH = '/sys/devices/system/cpu'
regexp = re.compile('cpu[0-9]')

# Description: param file

AVAILABLE_DICT_PARAMS = {
    'available_governors': 'scaling_available_governors',
    'available_frequencies': 'scaling_available_frequencies'
} # list output

VALUE_DICT_PARAMS = {
    'current_governor': 'scaling_governor',
    'min_freq': 'scaling_min_freq',
    'max_freq': 'scaling_max_freq',
} # str output

CHECK_DICT_PARAMS = {
    'precision_boost': 'boost',
    'cpb': 'cpb'
} # When values must be checked for availabilty

PARAMS_VARS = [AVAILABLE_DICT_PARAMS, VALUE_DICT_PARAMS, CHECK_DICT_PARAMS]

def _get_cpus_list():
    '''Returns available list of cpu cores'''

    return sorted(filter(regexp.search, os.listdir(OS_PATH)))

def _parse_param(param: str, cpu: str) -> list:
    file_path = Path(OS_PATH) / cpu / "cpufreq" / param

    try:
        with open(file_path, encoding='utf-8') as f:
            contents = f.read().split()

        return contents[0] if len(contents) == 1 else contents
    except (FileNotFoundError, PermissionError, OSError):
        return None

def _check_param_availabilty(param: str) -> bool:
    file_path = Path(OS_PATH) / "cpu1" / "cpufreq" / param

    try:
        with open(file_path, encoding='utf-8') as f:
            value = f.read().strip()
    except (FileNotFoundError, PermissionError, OSError):
        return False

    cmd = f'echo "{value}" > {file_path}'
    error = run_cmd(cmd)

    if error:
        return False

    return True

def cpu_info() -> dict:
    """
    Returns information from every CPU core (no argument required)

    Output:

    {
        'cpu0': {
            'available_governors': ['userspace', 'powersave', 'performance', 'schedutil'],
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'schedutil',
            'min_freq': '1400000',
            'max_freq': '3000000',
            'precision_boost': '1',
            'cpb': '1'
        },

        'cpu1': {
            'available_governors': ['userspace', 'powersave', 'performance', 'schedutil'],
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'conservative',
            'min_freq': '1400000',
            'max_freq': '3000000',
            'precision_boost': '1',
            'cpb': '1'
        }
    }

    """

    result = {}

    for cpu in _get_cpus_list():
        result[cpu] = {k: _parse_param(v, cpu) for k, v in AVAILABLE_DICT_PARAMS.items()}
        result[cpu].update({k: _parse_param(v, cpu) for k, v in VALUE_DICT_PARAMS.items()})

        for name, parameter in CHECK_DICT_PARAMS.items():
            if _check_param_availabilty(parameter):
                result[cpu].update({name: _parse_param(parameter, cpu)})

    return result

def general_cpu_info():
    """
    Get general cpu info (no argument required)
    """

    general_result = {} # output
    result = cpu_info()

    name_dict_params_with_kv = {
        'list_params': list(AVAILABLE_DICT_PARAMS),
        'str_params': list(VALUE_DICT_PARAMS),
        'int_params': list(CHECK_DICT_PARAMS)
    }

    for k, v in name_dict_params_with_kv.items():
        for i in v:
            if k == 'list_params':
                general_result[i] = list(list_intersection(result, i))
            else:
                try:
                    general_result[i] = list(str_intersection(result, i))[0]
                except IndexError:
                    return {
                        "status": "error",
                        "message": "CPU Governors/Features are not the same"
                    }

    return general_result

@validate_data_type(dict)
@validate_data_length(2, mode='min')
def set_params(data: dict) -> dict:
    """
    Sets params for certain cpu core number. API Usage:
    
    {
        'cpu': 'cpu0',
        'scaling_min_freq': '1400000',
        'scaling_max_freq': '3000000'
    }
    """

    try:
        cpu = data['cpu']
    except KeyError:
        return {
            'status': 'error',
            'message': 'CPU number expected'
        }

    errors = {}
    for param, value in data.items():
        file_path = Path(OS_PATH) / cpu / "cpufreq" / param
        if param != 'cpu':
            cmd = f'echo {value} > {file_path}'

            error = run_cmd(cmd)

            if error:
                errors[param] = error

    if not errors:
        return {
            'status': 'ok',
            'message': f'CPU parameters were changed successfully for CPU {cpu}!'
        }

    return {
        'status': 'error',
        'message': str(errors)
    }

@validate_data_type(dict)
@validate_data_length(1, mode='min')
def set_general_tuning(data: dict) -> dict:
    """
    Set general params for all cpu cores. API Usage:
    
    {
        'current_governor': 'schedutil',
        'min_freq': '1400000',
        'max_freq': '3000000',
        'precision_boost': '1',
        'cpb': '1'
    }
    """

    arg = {}
    errors = {}

    for cpu in _get_cpus_list():
        arg['cpu'] = cpu
        for param, value in data.items():
            if param != 'cpu':
                arg[get_all_merged_params(PARAMS_VARS)[param]] = value

        error = set_params(arg)
        if error['status'] != 'ok':
            errors[cpu] = error

    if not errors:
        return {
            'status': 'ok',
            'message': 'CPU settings were changed successfully!'
        }

    return {
        'status': 'error',
        'message': str(errors)
    }
