# pylint: disable=line-too-long
'''Module for hardware information'''

from datetime import datetime
import socket
import time
from getmac import get_mac_address as gma
import psutil
import GPUtil

def get_hardware_info() -> dict:
    """
    Returns hardware info (no argument required)
    """

    gpus = GPUtil.getGPUs()
    gpu_info = gpus[0] if gpus else None

    net_io = psutil.net_if_addrs()
    main_adapter = list(net_io.keys())[1] if len(net_io) > 1 else (list(net_io.keys())[0] if net_io else "Unknown")
    net_stats = psutil.net_if_stats()
    adapter_speed = net_stats[main_adapter].speed if main_adapter in net_stats else "N/A"

    # RAM & Disk
    vmem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # CPU Temp
    temps = psutil.sensors_temperatures()
    cpu_temp = "N/A"
    for key in ['coretemp', 'cpu_thermal', 'Package id 0']:
        if key in temps and temps[key]:
            cpu_temp = getattr(temps[key][0], 'current', 'N/A')
            break

    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"

    return {
        "cpu_model": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_freq": round(psutil.cpu_freq().max, 2) if psutil.cpu_freq() else "N/A",
        "cpu_load": psutil.cpu_percent(interval=1),
        "cpu_temp": cpu_temp,

        # RAM
        "ram_total": round(vmem.total / (1024 ** 3), 2),
        "ram_used": round(vmem.used / (1024 ** 3), 2),
        "ram_available": round(vmem.available / (1024 ** 3), 2),
        "ram_free": round(vmem.free / (1024 ** 3), 2),
        "ram_cached": round(getattr(vmem, 'cached', 0) / (1024 ** 3), 2),

        # Disk
        "disk_total": round(disk.total / (1024 ** 3), 2),
        "disk_used": round(disk.used / (1024 ** 3), 2),
        "disk_free": round(disk.free / (1024 ** 3), 2),

        # GPU
        "gpu_model": gpu_info.name if gpu_info else "N/A",
        "gpu_driver": gpu_info.driver if gpu_info else "N/A",
        "gpu_memory": round(gpu_info.memoryTotal / 1024, 2) if gpu_info else "N/A",
        "gpu_load": gpu_info.load if gpu_info else "N/A",
        "gpu_temp": gpu_info.temperature if gpu_info else "N/A",

        # Network
        "net_adapter": main_adapter,
        "net_speed": adapter_speed,
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "mac": gma() or "N/A",

        # Other
        "active_processes": len(psutil.pids()),
        "system_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "uptime": uptime_string
    }
