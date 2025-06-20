'''Sysctl module testing'''

from modules.sysctl import set_sysctl_param, parse_sysctl

PARAM_NAME = 'net.ipv4.icmp_ratemask'

def test_valid_data():
    """Test response status with valid params"""

    saved_data = {
        'name': PARAM_NAME,
        'value': parse_sysctl()[PARAM_NAME]
    }

    data = {
        'name': PARAM_NAME,
        'value': '6169'
    } # Rarely used param

    try:
        assert set_sysctl_param(data)['status'] == 'ok'
    finally:
        assert set_sysctl_param(saved_data)['status'] == 'ok'

def test_valid_data_response():
    """Test response data with valid params"""

    saved_data = {
        'name': PARAM_NAME,
        'value': parse_sysctl()[PARAM_NAME]
    }

    data = {
        'name': PARAM_NAME,
        'value': '6169'
    }

    set_sysctl_param(data)

    try:
        assert data['value'] == parse_sysctl()[data['name']]
    finally:
        set_sysctl_param(saved_data)
