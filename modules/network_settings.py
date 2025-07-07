'''Module for network settings'''

from typing import Any
import psutil
from decorators.data_validators import validate_data_type, validate_data_length
from modules.run import run_cmd_with_output, run_cmd
from modules.sysctl import set_sysctl_param

def get_tcp_algorithms() -> list:
    """
    Returns allowed tcp algorithms for usage (no argument required)
    """

    result = run_cmd_with_output('sysctl -n net.ipv4.tcp_allowed_congestion_control').split()
    return result

def get_current_algo() -> str:
    """
    Returns current TCP congestion algorithm (no argument required)
    """

    result = run_cmd_with_output('sysctl -n net.ipv4.tcp_congestion_control').strip()
    return result

@validate_data_type(str)
def set_tcp_algo(algorithm: str) -> dict:
    """
    Set new TCP congestion algorithm. API usage:

    algorithm = 'bbr'

    """

    if algorithm not in get_tcp_algorithms():
        return {'status': 'error', 'message': 'Enter valid algorithm'}

    result = run_cmd_with_output(f'sysctl net.ipv4.tcp_congestion_control={algorithm}')

    if 'No such file or directory' in result:
        return {'status': 'error', 'message': result}

    return {
        'status': 'ok',
        'message': f'TCP Algorithm to {algorithm} was changed successfully'
    }

@validate_data_type(dict)
@validate_data_length(2, mode='exact')
def mac_changer(data: dict) -> dict:
    """
    Set new MAC Address. API Usage:
    
    {
        'iface': 'wlan0',
        'mac': 'AA:00:11:22:33:44'
    }
    """

    try:
        iface = data['iface']
        mac = data['mac']
    except KeyError:
        return {
            'status': 'error',
            'message': 'Got the wrong data'
        }

    commands = [
        f'ip link set dev {iface} down',
        f'ip link set dev {iface} address {mac}',
        f'ip link set dev {iface} up',
    ]

    for cmd in commands:
        res = run_cmd(cmd)
        if res:
            return {'status': 'error', 'message': res}

    return {
        'status': 'ok',
        'message': 'MAC Address was changed successfully!'
    }

def get_network_ifaces() -> list:
    """
    Returns list of network interfaces (no argument required)
    """

    iface_dict = psutil.net_if_addrs().keys()
    return list(iface_dict)

def parse_resolv() -> list:
    """
    Parses resolv.conf (no argument required)
    """

    with open('/etc/resolv.conf', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def set_dns(data: Any) -> dict:
    """
    Changes DNS settings via resolv.conf. API Usage:

    '''
    nameserver: 1.2.3.4
    nameserver: 5.5.5.5
    '''
    
    """

    try:
        with open('/etc/resolv.conf', 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
    except PermissionError:
        return {
            "status": "error",
            "message": "resolv.conf cannot be updated due to attributes/permissions"
        }
    except IOError:
        return {
            "status": "error",
            "message": "Input/Output error"
        }

    return {
        "status": "ok",
        "message": "resolv.conf was updated successfully!"
    }

def get_socket_buffs() -> dict:
    """
    Returns socket_buffs settings (no argument required)
    """

    output_dict = {}

    rw_params = {
        'net.core.rmem_default': 'Default receiving socket buffer',
        'net.core.wmem_default': 'Default sending socket buffer',

        'net.core.rmem_max': 'Max receiving socket buffer',
        'net.core.wmem_max': 'Max sending buffer',
    }

    # Get dynamically values from rw_params

    for param, desc in rw_params.items():
        output_dict[param] = {desc: run_cmd_with_output(f'sysctl -n {param}').strip()}

    return output_dict

@validate_data_type(dict)
@validate_data_length(1, mode='min')
def set_socket_buffs(data: dict) -> dict:
    """
    Sets socket buffers. API Usage:
    {
        'net.core.wmem_max': '55555'
    }
    """

    for param, value in data.items():
        error = set_sysctl_param({
            'name': param,
            'value': value,
        })

        if error['status'] == 'error':
            return {
                "status": "error",
                "message": error['message']
            }

    return {
        "status": "ok",
        "message": "Socket buffers changed successfully!"
    }
