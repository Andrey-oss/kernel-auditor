from modules.run import run_cmd
from modules.helpers import *
import os
import re

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

def _get_cpus_list() -> list:
    return sorted(filter(regexp.search, os.listdir(OS_PATH)))

def _parse_param(param: str, cpu: str) -> list:
    f = open(f"{OS_PATH}/{cpu}/cpufreq/{param}").read().split()

    return f[0] if len(f) == 1 else f

def _check_param_availabilty(param: str) -> bool:
    file_path = f"{OS_PATH}/cpu1/cpufreq/{param}"

    try:
        value = open(file_path).read().strip()
    except Exception:
        return False
    
    cmd = f'echo "{value}" > {file_path}'
    error = run_cmd(cmd)

    if error:
        return False
    
    return True

def cpu_info() -> dict:
    """
    Returns information from every CPU core (no argument required)
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
        'list_params': [k for k in AVAILABLE_DICT_PARAMS.keys()],
        'str_params': [k for k in VALUE_DICT_PARAMS.keys()],
        'int_params': [k for k in CHECK_DICT_PARAMS.keys()]
    }
        
    for k, v in name_dict_params_with_kv.items():
        for i in v:
            if k == 'list_params':
                general_result[i] = [el for el in list_intersection(result, i)]
            else:
                try:
                    general_result[i] = [el for el in str_intersection(result, i)][0]
                except Exception:
                    return {"status": "error", "message": "CPU Governors/Features are not the same"}

    return general_result

def set_params(data: dict) -> dict:
    """
    Sets params for certain cpu core number. API Usage:
    
    {
        'cpu': 'cpu0',
        'scaling_min_freq': '1400000',
        'scaling_max_freq': '3000000'
    }
    """

    errors = {}
    file_path = f'{OS_PATH}/{data['cpu']}/cpufreq'
    for param, value in data.items():
        if param != 'cpu':

            cmd = f'echo {value} > {file_path}/{param}'

            error = run_cmd(cmd)

            if error:
                errors[param] = error
    
    if not errors:
        return {'status': 'ok', 'message': f'CPU parameters were changed successfully for CPU {data['cpu']}!'}
    
    return {'status': 'ok', 'message': str(errors)}

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
            else:
                arg[param] = value
            
        error = set_params(arg)
        if error['status'] != 'ok':
            errors[cpu] = error
    
    if not errors:
        return {'status': 'ok', 'message': 'CPU settings were changed successfully!'}
    
    return {'status': 'error', 'message': str(errors)}