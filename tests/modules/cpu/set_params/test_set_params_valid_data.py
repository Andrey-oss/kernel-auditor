'''Module of positive tests for set_params function from cpu module'''

from modules.cpu import set_params, cpu_info

def test_valid_data():
    '''Test function for valid data'''

    cpu_number = 'cpu0'
    saved_data = {'cpu': cpu_number}

    saved_data.update({'scaling_governor': cpu_info()[cpu_number]['current_governor']})

    data = {
        'cpu': 'cpu0',
        'scaling_governor': 'ondemand',
    }

    try:
        assert set_params(data)['status'] == 'success'
    finally:
        assert set_params(saved_data)['status'] == 'success'
