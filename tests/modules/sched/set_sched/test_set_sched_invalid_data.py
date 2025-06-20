'''Module for negative tests for set_sched function from sched module'''

from modules.sched import set_sched

def test_invalid_device():
    '''Test for invalid device'''

    data = {
        'device': 'test123',
        'scheduler': 'none'
    }

    assert set_sched(data)['status'] != 'ok'

def test_invalid_sched():
    '''Test for invalid scheduler'''

    data = {
        'device': 'sda',
        'scheduler': 'test123_xxf'
    }

    assert set_sched(data)['status'] != 'ok'
