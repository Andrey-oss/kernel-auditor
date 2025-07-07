'''Module for data decorators'''

from functools import wraps

def validate_data_type(expected_type) -> dict:
    '''Decorator for validating input data type'''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args:
                return {'status': 'error', 'message': 'No arguments were given'}

            if not isinstance(args[0], expected_type):
                return {'status': 'error', 'message': 'Got wrong variable type, expected JSON-type'}

            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_data_length(expected_length: int, mode: str = 'exact'):
    '''Decorator for validating input data length

    modes:
      - 'exact' - == expected_length
      - 'max' - < expected_length
      - 'min' - > expected_length
    '''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args:
                raise ValueError("Missing positional arguments for validation")

            actual_length = len(args[0])

            if mode == 'exact' and actual_length != expected_length:
                return {
                    'status': 'error',
                    'message': f'Expected length {expected_length}, got {actual_length}'
                }

            elif mode == 'max' and actual_length > expected_length:
                return {
                    'status': 'error',
                    'message': f'Max length {expected_length}, got {actual_length}'
                }

            elif mode == 'min' and actual_length < expected_length:
                return {
                    'status': 'error',
                    'message': f'Min length {expected_length}, got {actual_length}'
                }

            return func(*args, **kwargs)
        return wrapper
    return decorator
