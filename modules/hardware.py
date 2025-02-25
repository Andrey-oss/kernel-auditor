import psutil
import GPUtil
import time
import socket
from datetime import datetime

def get_hardware_info() -> dict:
    gpus = GPUtil.getGPUs()
    gpu_info = gpus[0] if gpus else None

    net_io = psutil.net_if_addrs()
    net_stats = psutil.net_if_stats()
    main_adapter = list(net_io.keys())[1] if net_io else "Unknown"
    adapter_speed = net_stats[main_adapter].speed if main_adapter in net_stats else "N/A"
    
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_string = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"

    return {
        "cpu_model": psutil.cpu_freq().current,
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "cpu_freq": round(psutil.cpu_freq().max, 2),
        "cpu_load": psutil.cpu_percent(interval=1),
        "cpu_temp": psutil.sensors_temperatures().get('cpu_thermal', [{'current': 'N/A'}])[0]['current'],

        # Measure of RAM/Disk - GB

        "ram_total": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "ram_used": round(psutil.virtual_memory().used / (1024 ** 3), 2),
        "ram_available": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "ram_free": round(psutil.virtual_memory().free / (1024 ** 3), 2),
        "ram_cached": round(psutil.virtual_memory().cached / (1024 ** 3), 2),

        "disk_total": round(psutil.disk_usage('/').total / (1024 ** 3), 2),
        "disk_used": round(psutil.disk_usage('/').used / (1024 ** 3), 2),
        "disk_free": round(psutil.disk_usage('/').free / (1024 ** 3), 2),

        "gpu_model": gpu_info.name if gpu_info else "N/A",
        "gpu_driver": gpu_info.driver if gpu_info else "N/A",
        "gpu_memory": round(gpu_info.memoryTotal / 1024, 2) if gpu_info else "N/A",
        "gpu_load": gpu_info.load if gpu_info else "N/A",
        "gpu_temp": gpu_info.temperature if gpu_info else "N/A",

        "net_adapter": main_adapter,
        "net_speed": adapter_speed,
        "ip_address": socket.gethostbyname(socket.gethostname()),

        "active_processes": len(psutil.pids()),
        "system_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "uptime": uptime_string
    }
