import subprocess

def parse_sysctl():
    result = subprocess.run(['sysctl', '-a'], capture_output=True, text=True)
    sysctl_data = {}

    for line in result.stdout.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            sysctl_data[key.strip()] = value.strip()

    return sysctl_data

def set_sysctls(data):
    try:
        result = subprocess.run(['sudo', 'sysctl', f"{data['name']}={data['value']}"], stderr=subprocess.PIPE, check=True)
    except Exception as e:
        return {'status': 'You entered the wrong value of the parameter'}

    if result.returncode != 0 or result.stderr:
        return {'status': str({data['name']: result.stderr})}
    
    return {'status': 'ok'}