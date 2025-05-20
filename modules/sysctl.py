from modules.run import run_cmd, run_cmd_with_output

def parse_sysctl() -> dict:
    cmd = 'sysctl -a'
    result = run_cmd_with_output(cmd)
    sysctl_data = {}

    for line in result.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            sysctl_data[key.strip()] = value.strip()

    return sysctl_data

def set_sysctl_param(data) -> dict:
    cmd = f'sysctl {data['name']}={data['value']}'
    error_msg = run_cmd(cmd) # I don't know how to fix sysctl output into the console, but let it be

    if error_msg:
        return {'status': 'error', 'message': error_msg}
    
    return {'status': 'ok', 'message': f'Parameter {data['name']} was changed successfully!'}