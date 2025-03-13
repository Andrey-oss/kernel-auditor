from modules.run import run_cmd
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

def _get_cpus_list() -> list:
    return sorted(filter(regexp.search, os.listdir(OS_PATH)))

def _parse_param(param: str, cpu: str) -> list:
    f = open(f"{OS_PATH}/{cpu}/cpufreq/{param}").read().split()

    if len(f) == 1:
        return f[0]

    return f

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
    result = {}

    for cpu in _get_cpus_list():
        result[cpu] = {k: _parse_param(v, cpu) for k, v in AVAILABLE_DICT_PARAMS.items()}
        result[cpu].update({k: _parse_param(v, cpu) for k, v in VALUE_DICT_PARAMS.items()})
        
        for name, parameter in CHECK_DICT_PARAMS.items():
            if _check_param_availabilty(parameter):
                result[cpu].update({name: _parse_param(parameter, cpu)})

    return result

def set_governor(cpu, governor) -> dict:
    cmd = f'echo {governor} > {OS_PATH}/{cpu}/cpufreq/scaling_governor'
    error = run_cmd(cmd)

    if error:
        return {'status': error}
    
    return {'status': 'ok'}

def set_frequencies(min_freq, max_freq, cpu) -> dict:
    if min_freq > max_freq:
        return {'status': 'Minimum frequency must be lower than maximum frequency'}

    min_freq_cmd = f'echo {min_freq} > {OS_PATH}/{cpu}/cpufreq/scaling_min_freq'
    max_freq_cmd = f'echo {max_freq} > {OS_PATH}/{cpu}/cpufreq/scaling_max_freq'

    min_freq_error = run_cmd(min_freq_cmd)
    max_freq_error = run_cmd(max_freq_cmd)

    if min_freq_error:
        return {'status': min_freq_error}
    
    if max_freq_error:
        return {'status': max_freq_error}
    
    return {'status': 'ok'}

def set_features(data) -> dict:
    errors = {}
    file_path = f'{OS_PATH}/{data['cpu']}/cpufreq'
    for k, v in data.items():
        if k != 'cpu':
            v = 1 if v else 0

            cmd = f'echo {v} > {file_path}/{k}'

            error = run_cmd(cmd)

            if error:
                errors[k] = error
    
    if not errors:
        return {'status': 'ok'}

    return {'status': str(errors)}