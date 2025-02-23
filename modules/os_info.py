import platform
import psutil
import uptime
from datetime import datetime

def get_system_info() -> dict:
    return {
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.architecture()[0],
        "cpu_count": psutil.cpu_count(logical=True),
        "cpu_freq": round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else "N/A",
        "cpu_percent": psutil.cpu_percent(interval=1),
        "total_memory": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "used_memory": round(psutil.virtual_memory().used / (1024 ** 3), 2),
        "disk_space": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "uptime": str(datetime.now() - uptime.boottime()).split('.')[0],
        "boot_time": uptime.boottime().strftime('%Y-%m-%d %H:%M:%S'),
        "load_avg": [round(val, 2) for val in psutil.getloadavg()] if hasattr(psutil, "getloadavg") else ["N/A"] * 3
    }