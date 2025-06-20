'''Module for valid tests for set_tun function from sched module'''

from modules.sched import set_tun, get_sched_values

def test_with_valid_data():
    '''Test function with valid data'''

    device = 'sda'
    saved_data = {'device': device}

    # Save current data and restore it after the test

    saved_data.update(get_sched_values()[device])

    data = {
        'device': device,
        'io_timeout': '10000'
    }

    try:
        assert set_tun(data)['status'] == 'ok'
    finally:
        assert set_tun(saved_data)['status'] == 'ok'
