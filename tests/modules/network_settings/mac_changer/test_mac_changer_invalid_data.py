'''Tests with valid data for mac_changer function

There is not test with wrong MAC Specification due to unvailablity of internet
Test causes unexpected behaviour of wifi adapter due to some linux rules
Also some tests will be failed'''

from modules.network_settings import mac_changer

def test_wrong_mac_address():
    '''Test with wrong MAC address'''

    mac = 'macaddress'

    data = {
        'iface': 'wlp4s0',
        'mac': mac
    }

    assert mac_changer(data)['status'] != 'ok'

def test_wrong_data():
    '''Test with wrong data'''

    data = {
        'interface': 'lo',
        'macaddress': '123'
    }

    assert mac_changer(data)['status'] != 'ok'
