'''Module for sysctl settings'''

from decorators.data_validators import validate_data_type, validate_data_length
from modules.run import run_cmd, run_cmd_with_output

def parse_sysctl() -> dict:
    '''Parse all sysctl params'''

    cmd = 'sysctl -a'
    result = run_cmd_with_output(cmd)
    sysctl_data = {}

    for line in result.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            sysctl_data[key.strip()] = value.strip()

    return sysctl_data

@validate_data_type(dict)
@validate_data_length(2, mode='exact')
def set_sysctl_param(data: dict) -> dict:
    """
    Sets sysctl param:
    
    {
        'name': 'abi.vsyscall32',
        'value': '1'
    }
    """

    try:
        cmd = f'sysctl {data['name']}={data['value']}'
    except KeyError:
        return {'status': 'error', 'message': 'Sysctl param name or value not found in request!'}

    error_msg = run_cmd(cmd) # I don't know how to fix sysctl output into the console, but let it be

    if error_msg:
        return {'status': 'error', 'message': error_msg}

    return {'status': 'ok', 'message': f'Parameter {data['name']} was changed successfully!'}
