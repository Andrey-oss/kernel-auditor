from modules.run import run_cmd, run_cmd_with_output

def parse_sysctl() -> dict:
    cmd = 'sysctl -a'
    result = run_cmd_with_output(cmd)
    sysctl_data = {}

    for line in result.stdout.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            sysctl_data[key.strip()] = value.strip()

    return sysctl_data

def set_sysctls(data) -> dict:
    cmd = f'sysctl {data['name']}={data['value']}'
    error = run_cmd(cmd)

    if error:
        return {'status': 'You entered the wrong value of the parameter'}
    
    return {'status': 'ok'}