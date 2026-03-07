'''Module of negative tests for set_params function from cpu module'''

from modules.cpu import set_params

CPU_NUM = 'cpu0'

def test_invalid_cpu_num():
    '''Test invalid cpu number'''

    data = {
        'cpu': 'test37',
        'scaling_min_freq': '1400000',
        'scaling_max_freq': '3000000'
    }

    assert set_params(data)['status'] != 'success'

def test_invalid_governor():
    '''Test invalid cpu governor'''

    data = {
        'cpu': CPU_NUM,
        'current_governor': 'schedutil'
    }

    assert set_params(data)['status'] != 'success'

def test_data_without_cpu():
    '''Test data without cpu number'''

    data = {
        'scaling_min_freq': '1400000',
        'scaling_max_freq': '3000000'
    }

    assert set_params(data)['status'] != 'success'

def test_wrong_param():
    '''Test function logic with unknown param'''

    data = {
        'cpu': CPU_NUM,
        'some_non-existent_param': 21
    }

    assert set_params(data)['status'] != 'success'
