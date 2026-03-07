'''Module for negative tests for set_tun function from sched module'''

from modules.sched import set_tun

def test_invalid_device():
    '''Test with negative device'''

    data = {
        'device': 'test123',
        'nr_requests': '128',
        'read_ahead_kb': '128'
    }

    assert set_tun(data)['status'] != 'success'

def test_no_device_specified():
    '''Test for no device specified'''

    data = {
        'nr_requests': '128',
        'read_ahead_kb': '128'
    }

    assert set_tun(data)['status'] != 'success'
