'''Tests with valid data for mac_changer function'''

from modules.network_settings import mac_changer

def test_valid_data():
    '''Test function with valid data'''

    data = {
        'iface': 'wlp4s0',
        'mac': 'AA:00:11:22:33:44'
    }

    assert mac_changer(data)['status'] == 'ok' # MAC Cannot be restored due to wifi turn offing
