'''Module of negative tests for sysctl'''

from modules.sysctl import set_sysctl_param, parse_sysctl

def test_invalid_param_with_valid_value():
    '''Test with invalid param name'''

    data = {
        'name': 'abc.abc.abc',
        'value': '123'
    }

    assert set_sysctl_param(data)['status'] != 'success'

def test_valid_param_with_invalid_value():
    '''Test with invalid data value '''

    data = {
        'name': 'net.ipv4.icmp_ratemask',
        'value': '6169a'
    }

    set_sysctl_param(data)

    assert data['value'] != parse_sysctl()[data['name']]

def test_invalid_value_name():
    '''Test with wrong data value key'''

    data = {
        'name': 'net.ipv4.icmp_ratemask',
        'valu': '6169a'
    }

    assert set_sysctl_param(data)['status'] != 'success'

def test_invalid_param_name():
    '''Test with invalid param key'''

    data = {
        'nam': 'net.ipv4.icmp_ratemask',
        'value': '6169a'
    }

    assert set_sysctl_param(data)['status'] != 'success'
