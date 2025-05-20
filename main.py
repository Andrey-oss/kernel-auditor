from flask import Flask, render_template, request, jsonify
from modules.sysctl import parse_sysctl, set_sysctl_param
from modules.hardware import get_hardware_info
from modules.os_info import get_system_info
from modules.process import get_processes
from modules.network_settings import *
from core.settings import cfg_parser
from checkhealth.check import init
from modules.network import *
from modules.sched import *
from modules.cpu import *

app = Flask(__name__)
cfg = cfg_parser()

if cfg['checkhealth']:
    init()

# Page section

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/usage')
def usage():
    return render_template('usage.html')

@app.route('/os')
def os_info():
    info = get_system_info()

    return render_template('os.html', system_info=info)

@app.route('/network')
def network():
    network_info = get_network_info()
    speed_test = get_speed_test()
    ip_info = get_ip_info()
    
    return render_template('network.html', 
                           network_info=network_info, 
                           speed_test=speed_test,
                           ip_info=ip_info
                           )

@app.route('/hardware')
def hardware_info():
    hardware_info = get_hardware_info()

    return render_template('hardware.html', hardware_info=hardware_info)

@app.route('/processes')
def process_info():
    processes = get_processes()
    return render_template('processes.html', processes=processes)

@app.route('/schedulers')
def schedulers():
    io_schedulers = get_schedulers()
    scheduler_values = get_sched_values()

    return render_template('sched.html',
                            io_schedulers=io_schedulers,
                            scheduler_values=scheduler_values)

@app.route('/full_schedulers')
def full_schedulers():
    io_schedulers = get_schedulers()
    scheduler_values = get_sched_values()

    return render_template('full_schedulers.html',
                            io_schedulers=io_schedulers,
                            scheduler_values=scheduler_values)

@app.route('/sysctl_settings')
def sysctl_settings():
    sysctl_data = parse_sysctl()

    return render_template('sysctl.html', sysctl_data=sysctl_data)

@app.route('/cpu_settings')
def cpu_settings():
    general_cpu_data = general_cpu_info()

    if 'error' in general_cpu_data.values():
        return jsonify({"status": general_cpu_data['status'], "message": general_cpu_data['message']}), 500

    return render_template('cpu.html', cpu_settings=general_cpu_data)

@app.route('/full_cpu_settings')
def full_cpu_settings():
    cpu_data = cpu_info()

    return render_template('full_cpu.html', cpu_data=cpu_data)

@app.route('/network_settings')
def network_settings():
    network_data = {
        'tcp_algorithms': get_tcp_algorithms(),
        'current_algorithm': get_current_algo(),
        'parsed_resolv_conf': parse_resolv(),
        'network_ifaces': get_network_ifaces(),
        'socket_buff': get_socket_buffs(),
    }

    return render_template('network_settings.html', network_data=network_data)

## API SECTION

# Sched Settings

@app.route('/api/set_scheduler', methods=['POST'])
def set_scheduler():
    data = request.json
    result = set_sched(data)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/api/set_sched_tunning', methods=['POST'])
def set_sched_tunning():
    result = set_tun(request.json)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

# Sysctl Settings

@app.route('/api/set_sysctl', methods=['POST'])
def set_sysctl():
    result = set_sysctl_param(request.json)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

# CPU Settings

@app.route('/api/set_cpu_params', methods=['POST'])
def set_cpu_params():
    data = request.json
    result = set_params(data)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/api/set_cpu_tuning', methods=['POST'])
def set_cpu_tuning():
    data = request.json
    result = set_general_tuning(data)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

# Network Settings

@app.route('/api/set_tcp_congestion', methods=['POST'])
def set_tcp_algorithm():
    algorithm = request.json['algorithm']
    result = set_tcp_algo(algorithm)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/api/update_resolv', methods=['POST'])
def update_resolv():
    data = request.json['content']
    result = set_dns(data)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/api/change_mac', methods=['POST'])
def change_mac():
    data = request.json
    result = mac_changer(data)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

@app.route('/api/set_socket_buffers', methods=['POST'])
def set_socket_buffers():
    data = request.json
    result = set_socket_buffs(data)

    if result['status'] != 'ok':
        return jsonify(result), 500
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=cfg['debug'], port=cfg['port'])