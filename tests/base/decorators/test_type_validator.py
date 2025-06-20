'''Module for testing validate_data_type decorator'''

from decorators.data_validators import validate_data_type

@validate_data_type(dict) # common used type in the project
def dummy_func(data):
    '''Dummy function for testing'''

    return {'status': 'ok', 'message': data}

def test_with_valid_data_type():
    '''Test with valid data'''

    assert dummy_func({'1': '2'})['status'] == 'ok'

def test_with_semi_valid_data_type():
    '''Test with set/dict type, must be OK'''

    assert dummy_func({})['status'] == 'ok'

def test_with_invalid_data_type():
    '''Test with invalid data type'''

    assert dummy_func('')['status'] != 'ok'
