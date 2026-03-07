'''Module for testing valid data for set_general_tuning from cpu module'''

import random
from modules.cpu import set_general_tuning, general_cpu_info

TEST_PARAM = 'current_governor'
GEN_CPU_INFO = general_cpu_info()
RANDOM_GOVERNOR = random.choice(GEN_CPU_INFO['available_governors'])

def test_with_valid_data():
    '''Test function with valid data'''

    saved_data = {TEST_PARAM: GEN_CPU_INFO[TEST_PARAM]}

    data = {
        TEST_PARAM: RANDOM_GOVERNOR
    }

    try:
        assert set_general_tuning(data)['status'] == 'success'
    finally:
        assert set_general_tuning(saved_data)['status'] == 'success'

    assert GEN_CPU_INFO['current_governor'] == saved_data[TEST_PARAM]

def test_with_cpu_number():
    '''
    Test for certain CPU Number changing
    Note: if cpu numbers information is not the same, test will be failed

    Function have to ignore cpu number
    '''

    saved_data = {TEST_PARAM: GEN_CPU_INFO[TEST_PARAM]}

    data = {
        'cpu': 'cpu0',
        TEST_PARAM: RANDOM_GOVERNOR
    }

    try:
        assert set_general_tuning(data)['status'] == 'success'
        assert 'error' not in GEN_CPU_INFO
    finally:
        assert set_general_tuning(saved_data)['status'] == 'success'
