# pylint: disable=line-too-long
'''Module for hardware information'''

from datetime import datetime
import socket
import time
import platform
from getmac import get_mac_address as gma
import psutil
import GPUtil

def get_cpu_model():
    """Get CPU model name safely"""
    try:
        # Using platform
        model = platform.processor()
        if model and model != '':
            return model

        # Using /proc/cpuinfo (Linux)
        with open('/proc/cpuinfo', 'r', encoding='utf-8') as f:
            for line in f:
                if 'model name' in line:
                    return line.split(':')[1].strip()
    except Exception:
        pass

    return "Unknown CPU"

def get_hardware_info() -> dict:
    """
    Returns hardware info (no argument required)
    """
    try:
        # GPU Information
        gpus = GPUtil.getGPUs()
        gpu_info = gpus[0] if gpus else None

        # Network Information
        net_io = psutil.net_if_addrs()
        net_stats = psutil.net_if_stats()

        # Get main network adapter (first non-loopback)
        main_adapter = "Unknown"
        for adapter in net_io.keys():
            if adapter != 'lo':  # skip loopback
                main_adapter = adapter
                break

        adapter_speed = net_stats[main_adapter].speed if main_adapter in net_stats else "N/A"

        # RAM & Disk
        vmem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # CPU Temperature
        cpu_temp = "N/A"
        try:
            temps = psutil.sensors_temperatures()
            for key in ['coretemp', 'cpu_thermal', 'k10temp', 'Package id 0']:
                if key in temps and temps[key]:
                    cpu_temp = round(getattr(temps[key][0], 'current', 0), 1)
                    break
        except Exception:
            pass

        cpu_freq_current = "N/A"
        cpu_freq_max = "N/A"
        cpu_freq_min = "N/A"

        try:
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                cpu_freq_current = round(cpu_freq.current, 2)
                cpu_freq_max = round(cpu_freq.max, 2) if cpu_freq.max else "N/A"
                cpu_freq_min = round(cpu_freq.min, 2) if cpu_freq.min else "N/A"
        except Exception:
            pass

        # CPU Load
        try:
            cpu_load = psutil.cpu_percent(interval=0.5)
        except Exception:
            cpu_load = 0

        # Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)

        if days > 0:
            uptime_string = f"{days}d {hours}h {minutes}m"
        else:
            uptime_string = f"{hours}h {minutes}m"

        # Get IP address (more reliable method)
        ip_address = "N/A"
        try:
            # Try to get real IP via socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception:
            try:
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
            except Exception:
                pass

        return {
            # CPU
            "cpu_model": get_cpu_model(),
            "cpu_cores": psutil.cpu_count(logical=False) or "N/A",
            "cpu_threads": psutil.cpu_count(logical=True) or "N/A",
            "cpu_freq_current": cpu_freq_current,
            "cpu_freq_max": cpu_freq_max,
            "cpu_freq_min": cpu_freq_min,
            "cpu_load": cpu_load,
            "cpu_temp": cpu_temp,

            # RAM
            "ram_total": round(vmem.total / (1024 ** 3), 2),
            "ram_used": round(vmem.used / (1024 ** 3), 2),
            "ram_available": round(vmem.available / (1024 ** 3), 2),
            "ram_percent": vmem.percent,

            # Disk
            "disk_total": round(disk.total / (1024 ** 3), 2),
            "disk_used": round(disk.used / (1024 ** 3), 2),
            "disk_free": round(disk.free / (1024 ** 3), 2),
            "disk_percent": disk.percent,

            # GPU
            "gpu_model": gpu_info.name if gpu_info else "Not detected",
            "gpu_driver": gpu_info.driver if gpu_info else "N/A",
            "gpu_memory_total": round(gpu_info.memoryTotal, 2) if gpu_info else "N/A",
            "gpu_memory_used": round(gpu_info.memoryUsed, 2) if gpu_info else "N/A",
            "gpu_memory_free": round(gpu_info.memoryFree, 2) if gpu_info else "N/A",
            "gpu_load": round(gpu_info.load * 100, 1) if gpu_info else "N/A",
            "gpu_temp": round(gpu_info.temperature, 1) if gpu_info else "N/A",

            # Network
            "net_adapter": main_adapter,
            "net_speed": adapter_speed,
            "ip_address": ip_address,
            "mac": gma() or "N/A",

            # System
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "os_release": platform.release(),
            "active_processes": len(psutil.pids()),
            "system_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "uptime": uptime_string,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        print(f"Error getting hardware info: {e}")
        return {
            "error": str(e),
            "cpu_model": "Error",
            "cpu_cores": "N/A",
            "cpu_threads": "N/A",
            "cpu_load": 0,
            "ram_total": 0,
            "ram_percent": 0,
            "disk_total": 0,
            "disk_percent": 0
        }
