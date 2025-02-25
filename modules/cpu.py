import subprocess
import os
import re

'''cpu_settings = {
    "cpu0": {
        "available_governors": ["performance", "powersave", "ondemand", "schedutil"],
        "current_governor": "performance",
        "min_freq": "800000",  # 800 MHz
        "cur_freq": "sth"
        "max_freq": "3500000",  # 3.5 GHz
        "boost": True,
        "hyper_threading": True,
        "advanced_tuning": {
            "scaling_min_freq": "800000",
            "scaling_max_freq": "3500000",
            "energy_performance_preference": "performance"
        }
    },
    "cpu1": {
        "available_governors": ["performance", "powersave"],
        "current_governor": "powersave",
        "min_freq": "600000",
        "cur_freq": "sth"
        "max_freq": "2500000",
        "boost": False,
        "hyper_threading": True,
        "advanced_tuning": {
            "scaling_min_freq": "600000",
            "scaling_max_freq": "2500000",
            "energy_performance_preference": "balance_performance"
        }
    }
}
'''

OS_PATH = '/sys/devices/system/cpu'
regexp = re.compile('cpu[0-9]')

# Description: file

available_dict = {'available_governors': 'scaling_available_governors', 'available_frequencies': 'scaling_available_frequencies'} # list output
value_dict = {'current_governor': 'scaling_governor', 'min_freq': 'scaling_min_freq', 'max_freq': 'scaling_max_freq'} # str output
check_dict = {'precision_boost': 'boost', 'cpb': 'cpb'} # When values must be checked for availabilty

def _get_cpus() -> list:
    return sorted([cpu for cpu in os.listdir(OS_PATH) if regexp.search(cpu)])

def _available_sth(param: str, cpu: str) -> list:
    return open(f"{OS_PATH}/{cpu}/cpufreq/{param}").read().split()

def _value_sth(param: str, cpu: str):
    return open(f"{OS_PATH}/{cpu}/cpufreq/{param}").read().strip()

def _check_sth(param: str) -> bool:
    file_path = f"{OS_PATH}/cpu1/cpufreq/{param}"
    try:
        value = open(file_path).read().strip()
    except Exception:
        return False

    result = subprocess.run(f'echo "{value}" > {file_path}', shell=True, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return True
    return False

def cpu_info():
    result = {}

    for cpu in _get_cpus():
        result[cpu] = {k: _available_sth(v, cpu) for k, v in available_dict.items()}
        result[cpu].update({k: _value_sth(v, cpu) for k, v in value_dict.items()})
        for name, parameter in check_dict.items():
            if _check_sth(parameter):
                result[cpu].update({name: _value_sth(parameter, cpu)})

    return result

def set_governor(cpu, governor):
    cmd = f'echo {governor} > {OS_PATH}/{cpu}/cpufreq/scaling_governor'
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0 or result.stderr:
        return {'status': result.stderr.strip()}
    
    return {'status': 'ok'}

def set_frequencies(min_freq, max_freq, cpu):
    if min_freq > max_freq:
        return {'status': 'Minimum frequency must be lower than maximum frequency'}

    min_freq_cmd = f'echo {min_freq} > {OS_PATH}/{cpu}/cpufreq/scaling_min_freq'
    max_freq_cmd = f'echo {max_freq} > {OS_PATH}/{cpu}/cpufreq/scaling_max_freq'

    min_result = subprocess.run(min_freq_cmd, shell=True, stderr=subprocess.PIPE, text=True)
    max_result = subprocess.run(max_freq_cmd, shell=True, stderr=subprocess.PIPE, text=True)

    if min_result.returncode != 0 or min_result.stderr:
        return {'status': min_result.stderr.strip()}
    
    if max_result.returncode != 0 or max_result.stderr:
        return {'status': max_result.stderr.strip()}
    
    return {'status': 'ok'}

def set_features(data):
    errors = {}
    file_path = f'{OS_PATH}/{data['cpu']}/cpufreq'
    for k, v in data.items():
        if k != 'cpu':
            if v:
                v = 1
            else:
                v = 0

            cmd = f'echo {v} > {file_path}/{k}'

            result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0 or result.stderr:
                errors[k] = result.stderr.strip()
    
    if len(errors) == 0:
        return {'status': 'ok'}

    return {'status': str(errors)}