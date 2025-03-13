from flask import Flask, render_template, request, jsonify
from modules.sysctl import parse_sysctl, set_sysctls
from modules.hardware import get_hardware_info
from modules.os_info import get_system_info
from modules.process import get_processes
from modules.cpu import *
from modules.network import *
from modules.sched import *
from core.settings import cfg_parser
from checkhealth.check import init

app = Flask(__name__)
cfg = cfg_parser()
if cfg['checkhealth']:
    init()

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
                           ip_info=ip_info)

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

@app.route('/full_cpu_settings')
def cpu_settings():
    cpu_data = cpu_info()
    return render_template('full_cpu.html', cpu_data=cpu_data)

## API SECTION

@app.route('/api/set_scheduler', methods=['POST'])
def set_scheduler():
    device = request.json['device']
    scheduler = request.json['scheduler']
    result = set_sched(device, scheduler)
    if result['status'] != 'ok':
        return jsonify({"status": "error", "message": result['status']}), 500
    return jsonify({"status": "ok", 'message': 'Scheduler has been changed successfully!'})

@app.route('/api/set_sched_tunning', methods=['POST'])
def set_sched_tunning():
    result = set_tun(request.json)
    if result['status'] != 'ok':
        return jsonify({"status": "error", "message": result['status']}), 500
    return jsonify({"status": "ok", 'message': 'New tunning applied with no errors!'})

@app.route('/api/set_sysctl', methods=['POST'])
def set_sysctl():
    result = set_sysctls(request.json)
    if result['status'] != 'ok':
        return jsonify({"status": "error", "message": result['status']}), 500
    return jsonify({"status": "ok", 'message': f'Parameter {request.json['name']} was changed successfully!'})

@app.route('/api/set_cpu_governor', methods=['POST'])
def set_cpu_governor():
    cpu = request.json['cpu']
    governor = request.json['governor']
    result = set_governor(cpu, governor)
    if result['status'] != 'ok':
        return jsonify({"status": "error", "message": result['status']}), 500
    return jsonify({"status": "ok", 'message': f'Governor {args['governor']} was changed successfully for CPU {args['cpu']}!'})

@app.route('/api/set_cpu_frequency', methods=['POST'])
def set_cpu_frequency():
    cpu = request.json['cpu']
    min_freq = request.json['min_freq']
    max_freq = request.json['max_freq']
    result = set_frequencies(min_freq, max_freq, cpu)
    if result['status'] != 'ok':
        return jsonify({"status": "error", "message": result['status']}), 500
    return jsonify({"status": "ok", 'message': f'Frequency was changed successfully!'})

@app.route('/api/set_cpu_features', methods=['POST'])
def set_cpu_features():
    result = set_features(request.json)
    if result['status'] != 'ok':
        return jsonify({"status": "error", "message": result['status']}), 500
    return jsonify({"status": "ok", 'message': f'CPU Features were changed successfully!'})

if __name__ == '__main__':
    app.run(debug=cfg['debug'], port=cfg['port'])