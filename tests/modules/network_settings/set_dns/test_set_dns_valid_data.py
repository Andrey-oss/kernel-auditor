'''Tests for set_tcp_algo function from network_settings'''

from modules.network_settings import set_dns, parse_resolv

def test_valid_data():
    '''Test with valid data'''

    data = '''
    nameserver: 1.1.1.1
    '''

    saved_data = ''.join(parse_resolv())

    try:
        assert set_dns(data)['status'] == 'success'
    finally:
        assert set_dns(saved_data)['status'] == 'success'
