'''Get process list with PID, name etc'''

from datetime import datetime
import psutil

def get_processes():
    '''Get processes via psutil'''
    proc_attrs = ['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'create_time']

    processes = []
    for proc in psutil.process_iter(attrs=proc_attrs):
        try:
            process_info = proc.info
            processes.append({
                "pid": process_info["pid"],
                "name": process_info["name"],
                "cpu_percent": process_info["cpu_percent"],
                "memory": round(process_info["memory_info"].rss / 1024 / 1024, 2),
                "status": process_info["status"],
                "started": datetime.fromtimestamp(
                    process_info["create_time"]
                ).strftime('%Y-%m-%d %H:%M:%S')
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes
