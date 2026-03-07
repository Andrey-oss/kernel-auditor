# pylint: disable=missing-function-docstring
'''Server starts here'''

from flask import Flask, render_template, request, jsonify

from core.database import (
    db,
    TuningProfile,
    AuditLog)
from core.settings import cfg_parser
from checkhealth.check import init_hc

from modules.sysctl import parse_sysctl, set_sysctl_param
from modules.hardware import get_hardware_info
from modules.os_info import get_system_info
from modules.process import get_processes
from modules.network_settings import (
    get_tcp_algorithms,
    get_current_algo,
    set_tcp_algo,
    mac_changer,
    get_network_ifaces,
    parse_resolv,
    set_dns,
    get_socket_buffs,
    set_socket_buffs)
from modules.network import (
    get_network_info,
    get_speed_test,
    get_ip_info
)
from modules.sched import (
    get_schedulers,
    get_sched_values,
    set_sched,
    set_tun
)
from modules.cpu import (
    cpu_info,
    general_cpu_info,
    set_general_tuning,
    set_params,
)

app = Flask(__name__)
cfg = cfg_parser()

app.config['SQLALCHEMY_DATABASE_URI'] = cfg.get('database_uri', 'sqlite:///tuning.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

if cfg['checkhealth']:
    init_hc()

def get_active_profile_id():
    """Return active profile ID or None (WIP Option)"""
    try:
        active = TuningProfile.query.filter_by(is_active=True).first()
        return active.id if active else None
    except Exception:
        return None

## ===== Page section =====

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
    return render_template('network.html')

@app.route('/hardware')
def hardware_info():
    return render_template('hardware.html')

@app.route('/processes')
def process_info():
    return render_template('processes.html')

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
        return jsonify(
            status=general_cpu_data['status'],
            message=general_cpu_data['message']
        ), 500

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

@app.route('/history')
def history_page():
    return render_template('history.html')

@app.route('/profiles')
def profiles_page():
    """Render profiles management page"""
    return render_template('profiles.html')

## ===== API SECTION =====

@app.route('/api/network/data')
def api_network_data():
    """Get network data from API"""
    try:
        data = {
            'network_info': get_network_info(),
            'speed_test': get_speed_test(),
            'ip_info': get_ip_info()
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/network/speedtest')
def api_speedtest():
    """API Speed test (WIP)"""
    try:
        result = get_speed_test()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hardware')
def api_hardware_info():
    """API endpoint for hardware info (for dynamic updates)"""
    try:
        data = get_hardware_info()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system')
def api_system_info():
    """API for system info (for dynamic updates)"""
    try:
        data = get_system_info()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/processes')
def api_processes():
    """API for processes list (for dynamic updates)"""
    try:
        processes = get_processes()
        return jsonify(processes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## ===== Logs =====

@app.route('/api/audit_logs', methods=['GET'])
def get_audit_logs():
    """Get paginated audit logs"""

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', None)
    status = request.args.get('status', None)

    # Build query
    query = AuditLog.query

    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    # Order by timestamp (newest first) and paginate
    paginated = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Prepare response
    result = {
        'items': [log.to_dict() for log in paginated.items],
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev,
            'next_page': paginated.next_num if paginated.has_next else None,
            'prev_page': paginated.prev_num if paginated.has_prev else None
        }
    }

    return jsonify(result)

@app.route('/api/audit_logs/categories', methods=['GET'])
def get_audit_categories():
    """Get all unique categories for filtering"""
    categories = db.session.query(AuditLog.category).distinct().all()
    return jsonify([c[0] for c in categories if c[0]])

## ===== Functional API Section =====

# ========== SCHEDULER API WITH AUDIT ==========

@app.route('/api/set_sched_tunning', methods=['POST'])
def set_sched_tunning():
    data = request.json
    device = data.get('device')

    # Get old values before change
    old_values = {}
    try:
        sched_values = get_sched_values()
        if device in sched_values:
            for param in data:
                if param != 'device' and param in sched_values[device]:
                    old_values[param] = sched_values[device][param]
    except Exception:
        old_values = {}

    # Apply new settings
    result = set_tun(data)

    # Log each changed parameter
    if result['status'] == 'success':
        for param, new_value in data.items():
            if param != 'device':
                old_value = old_values.get(param, 'unknown')
                if str(old_value) != str(new_value):
                    log = AuditLog(
                        action='change_scheduler_tuning',
                        category='scheduler',
                        parameter=f"device:{device}.{param}",
                        old_value=old_value,
                        new_value=new_value,
                        status='success',
                        profile_id=get_active_profile_id()
                    )
                    db.session.add(log)
        db.session.commit()
    else:
        # Log error
        log = AuditLog(
            action='change_scheduler_tuning',
            category='scheduler',
            parameter=f"device:{device}",
            new_value=str(data),
            status='error',
            profile_id=get_active_profile_id()
        )
        db.session.add(log)
        db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)

# ========== CPU API WITH AUDIT ==========

@app.route('/api/set_cpu_params', methods=['POST'])
def set_cpu_params():
    data = request.json
    cpu = data.get('cpu', 'unknown')

    # Get old values before change
    old_values = {}
    try:
        cpu_info_data = cpu_info()
        if cpu in cpu_info_data:
            for param in data:
                if param != 'cpu' and param in cpu_info_data[cpu]:
                    old_values[param] = cpu_info_data[cpu][param]
    except Exception:
        old_values = {}

    # Apply new settings
    result = set_params(data)

    # Log each changed parameter
    if result['status'] == 'success':
        for param, new_value in data.items():
            if param != 'cpu':
                old_value = old_values.get(param, 'unknown')
                if str(old_value) != str(new_value):
                    log = AuditLog(
                        action='change_cpu_params',
                        category='cpu',
                        parameter=f"{cpu}.{param}",
                        old_value=old_value,
                        new_value=new_value,
                        status='success',
                        profile_id=get_active_profile_id()
                    )
                    db.session.add(log)
        db.session.commit()
    else:
        # Log error
        log = AuditLog(
            action='change_cpu_params',
            category='cpu',
            parameter=f"{cpu}",
            new_value=str(data),
            status='error',
            profile_id=get_active_profile_id()
        )
        db.session.add(log)
        db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)

# ========== NETWORK API WITH AUDIT ==========

@app.route('/api/set_tcp_congestion', methods=['POST'])
def set_tcp_algorithm():
    algorithm = request.json.get('algorithm')

    # Get old value
    old_value = get_current_algo()

    # Apply new setting
    result = set_tcp_algo(algorithm)

    # Log
    log = AuditLog(
        action='change_tcp_congestion',
        category='network',
        parameter='tcp_congestion_control',
        old_value=old_value,
        new_value=algorithm,
        status=result['status'],
        profile_id=get_active_profile_id()
    )
    db.session.add(log)
    db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)


@app.route('/api/update_resolv', methods=['POST'])
def update_resolv():
    content = request.json.get('content')

    # Get old content (first few lines for log)
    try:
        with open('/etc/resolv.conf', 'r', encoding='utf-8') as f:
            old_content = f.read()[:200] + '...'  # Truncate for log
    except Exception:
        old_content = None

    # Apply changes
    result = set_dns(content)

    # Log
    log = AuditLog(
        action='update_resolv',
        category='network',
        parameter='resolv.conf',
        old_value=old_content,
        new_value='DNS updated',
        status=result['status'],
        profile_id=get_active_profile_id()
    )
    db.session.add(log)
    db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)


@app.route('/api/change_mac', methods=['POST'])
def change_mac():
    data = request.json
    iface = data.get('iface')
    mac = data.get('mac')

    # Get old MAC (if possible)
    try:
        import subprocess
        result = subprocess.run(['ip', 'link', 'show', iface], capture_output=True, text=True)
        old_mac = 'unknown'
        if 'link/ether' in result.stdout:
            old_mac = result.stdout.split('link/ether')[1].strip().split()[0]
    except Exception:
        old_mac = 'unknown'

    # Apply changes
    result = mac_changer(data)

    # Log
    log = AuditLog(
        action='change_mac',
        category='network',
        parameter=f"interface:{iface}",
        old_value=old_mac,
        new_value=mac,
        status=result['status'],
        profile_id=get_active_profile_id()
    )
    db.session.add(log)
    db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)


@app.route('/api/set_socket_buffers', methods=['POST'])
def set_socket_buffers():
    data = request.json

    # Get old values
    old_values = get_socket_buffs()

    # Apply changes
    result = set_socket_buffs(data)

    # Log each changed buffer
    if result['status'] == 'success':
        for param, new_value in data.items():
            old_value = 'unknown'
            # Try to find old value in socket_buffs structure
            for key, value_dict in old_values.items():
                if key == param:
                    old_value = list(value_dict.values())[0]
                    break

            log = AuditLog(
                action='change_socket_buffer',
                category='network',
                parameter=param,
                old_value=old_value,
                new_value=new_value,
                status='success',
                profile_id=get_active_profile_id()
            )
            db.session.add(log)
        db.session.commit()
    else:
        # Log error
        log = AuditLog(
            action='change_socket_buffer',
            category='network',
            parameter='socket_buffers',
            new_value=str(data),
            status='error',
            profile_id=get_active_profile_id()
        )
        db.session.add(log)
        db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/set_sysctl', methods=['POST'])
def set_sysctl():
    data = request.json

    sysctl_data = parse_sysctl()
    old_value = sysctl_data.get(data['name'], 'unknown')

    result = set_sysctl_param(data)

    log = AuditLog(
        action='change_sysctl',
        category='sysctl',
        parameter=data['name'],
        old_value=old_value,
        new_value=data['value'],
        status=result['status']
    )
    db.session.add(log)
    db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/set_cpu_tuning', methods=['POST'])
def set_cpu_tuning():
    data = request.json

    # Get old params
    old_cpu = general_cpu_info()

    # Setting up new values
    result = set_general_tuning(data)

    # Logging every parameter
    if result['status'] == 'success' and 'error' not in old_cpu:
        for param, value in data.items():
            if param in old_cpu and str(old_cpu[param]) != str(value):
                log = AuditLog(
                    action='change_cpu',
                    category='cpu',
                    parameter=param,
                    old_value=old_cpu[param],
                    new_value=value,
                    status='success'
                )
                db.session.add(log)
        db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/set_scheduler', methods=['POST'])
def set_scheduler_api():
    data = request.json

    # Get old value
    old_schedulers = get_schedulers()
    old_value = None
    if data['device'] in old_schedulers:
        for s in old_schedulers[data['device']]:
            if '[' in s:
                old_value = s.strip('[]')
                break

    # Setting up new value
    result = set_sched(data)

    log = AuditLog(
        action='change_scheduler',
        category='scheduler',
        parameter=f"device:{data['device']}",
        old_value=old_value,
        new_value=data['scheduler'],
        status=result['status']
    )
    db.session.add(log)
    db.session.commit()

    if result['status'] != 'success':
        return jsonify(result), 500
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=cfg['debug'], port=cfg['port'])
