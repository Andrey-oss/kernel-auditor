'''Module for positive testing'''

from modules.sched import set_sched, get_schedulers

DEVICE = 'sda'

def test_valid_data():
    '''Test for valid data'''

    saved_sched = [i for i in get_schedulers()[DEVICE] if '[' in i][0].replace('[', '').replace(']', '')

    saved_data = {
        'device': DEVICE,
        'scheduler': saved_sched
    }

    data = {
        'device': DEVICE,
        'scheduler': 'none'
    }

    try:
        assert set_sched(data)['status'] == 'ok'
    finally:
        assert set_sched(saved_data)['status'] == 'ok'
