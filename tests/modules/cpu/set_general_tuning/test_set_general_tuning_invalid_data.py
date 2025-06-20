'''Module for testing set_general_tuning with invalid data'''

from modules.cpu import set_general_tuning

def test_invalid_governor():
    '''Testing function output with wrong governor'''

    data = {
        'current_governor': 'gov123test_x1',
    }

    assert set_general_tuning(data)['status'] != 'ok'

def test_wrong_check_dict_params():
    '''
    Test for wrong CHECK_DICT_PARAMS, where must be 0 or 1 (turn on/off)
    Note: You may change data parameters or ignore this test if you haven't AMD Ryzen processor
    '''

    data = {
        'cpb': 'test'
    }

    assert set_general_tuning(data)['status'] != 'ok'

def test_with_only_cpu_number_in_data():
    '''Test if only cpu number will be in data'''

    data = {
        'cpu': 'cpu0'
    }

    assert set_general_tuning(data)['status'] != 'ok'
