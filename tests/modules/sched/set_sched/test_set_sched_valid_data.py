'''Module for positive testing'''

from modules.sched import set_sched, get_schedulers

DEVICE = 'sda'

def test_valid_data():
    '''Test for valid data'''

    saved_sched = next(
        (i.strip('[]') for i in get_schedulers()[DEVICE] if '[' in i),
        None  # If element not found
    )


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
