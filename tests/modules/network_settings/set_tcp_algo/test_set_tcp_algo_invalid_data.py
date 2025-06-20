'''Tests for set_tcp_algo function from network_settings'''

from modules.network_settings import set_tcp_algo

def test_invalid_algorithm():
    '''Test with wrong algorithm'''
    algo = 'test123_'

    assert set_tcp_algo(algo)['status'] != 'ok'
