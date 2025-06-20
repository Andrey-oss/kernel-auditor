'''Module for network information'''

import socket
import psutil
import requests
from core.settings import cfg_parser

cfg = cfg_parser() # It is not dynamic variable, it won't be updated after some changes in settings

try:
    import speedtest
except ImportError:
    if cfg['speed_test']:
        exit("[FATAL] Speedtest doesn't installed, check your installation")

def get_network_info() -> dict:
    """
    Returns network info (no argument required)
    """

    network_info = {}
    addrs = psutil.net_if_addrs()
    io_counters = psutil.net_io_counters(pernic=True)

    for interface, addresses in addrs.items():
        ip_address = None
        for addr in addresses:
            if addr.family == socket.AF_INET:
                ip_address = addr.address
                break

        if ip_address:
            network_info[interface] = {
                'ip': ip_address,
                'received': io_counters.get(interface, None).bytes_recv if interface in io_counters else 0,
                'sent': io_counters.get(interface, None).bytes_sent if interface in io_counters else 0,
                'speed': io_counters.get(interface, None).bytes_recv + io_counters.get(interface, None).bytes_sent if interface in io_counters else 0,
            }

    return network_info

def get_speed_test() -> dict:
    """
    Returns speed test, which includes ping, UP/DL speed (no argument required)
    """

    if cfg['speed_test']:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
        except Exception:
            return {'download': False, 'upload': False, 'ping': False}
        else:
            download_speed = st.download() / 1_000_000  # MBps
            upload_speed = st.upload() / 1_000_000  # MBps
            ping = st.results.ping
            return {'download': f'{round(download_speed, 2)} MBps', 'upload': f'{round(upload_speed, 2)} MBps', 'ping': f'{ping} ms'}
    return {'download': False, 'upload': False, 'ping': False}

def get_ip_info() -> dict:
    """
    Returns IP Information (no argument requiredd)
    """

    try:
        r = requests.get("https://ifconfig.co/json", timeout=5).json()
    except Exception:
        return {"Internet": "disabled"}
    return {k.capitalize().replace("_", " "): v for k, v in r.items() if k != 'user_agent'} # I attempted to retrieve and display the name and related information from a dictionary
