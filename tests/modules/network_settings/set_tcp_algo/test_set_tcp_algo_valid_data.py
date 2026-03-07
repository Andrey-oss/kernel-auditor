'''Tests for set_tcp_algo function from network_settings'''

import random
from modules.network_settings import set_tcp_algo, get_current_algo, get_tcp_algorithms

def test_valid_data():
    '''Test function for valid data'''

    algo = random.choice(get_tcp_algorithms()) # Get random available algorithm
    saved_algo = get_current_algo()

    try:
        assert set_tcp_algo(algo)['status'] == 'success'
    finally:
        assert set_tcp_algo(saved_algo)['status'] == 'success'
