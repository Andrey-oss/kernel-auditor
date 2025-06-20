'''Module for testing validate_data_length decorator'''
from typing import Any
from decorators.data_validators import validate_data_length

@validate_data_length(2, mode='min')
def dummy_min_func(data: Any) -> dict:
    '''Dummy function for testing min mode from the decorator'''

    return {'status': 'ok', 'message': data}

@validate_data_length(3, mode='max')
def dummy_max_func(data: Any) -> dict:
    '''Dummy function for testing max mode from the decorator'''

    return {'status': 'ok', 'message': data}

@validate_data_length(2, mode='exact')
def dummy_exact_func(data: Any):
    '''Dummy function for testing exact mode from the decorator'''

    return {'status': 'ok', 'message': data}

# dummy_min_func

def test_min_func_with_valid_data():
    '''Test min validator with valid data'''

    assert dummy_min_func('test')['status'] == 'ok'

def test_min_func_with_invalid_data():
    '''Test min validator, where requirements won't be satisfied'''

    assert dummy_min_func('x')['status'] != 'ok'

# dummy_max_func

def test_max_func_with_valid_data():
    '''Test min validator with valid data'''

    assert dummy_max_func('tex')['status'] == 'ok'

def test_max_func_with_invalid_data():
    '''Test min validator, where requirements won't be satisfied'''

    assert dummy_max_func('test') != 'ok'

# dummy_exact_func

def test_exact_func_with_valid_data():
    '''Test exact validator with valid data'''

    assert dummy_exact_func('te')['status'] == 'ok'

def test_exact_func_with_invalid_data():
    '''Test exact validator, where requirements won't be satisfied'''

    assert dummy_exact_func('test')['status'] != 'ok'
