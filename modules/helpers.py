'''This module contains some function, which can help to fix/solve some problems'''

def list_intersection(data: dict, param: str) -> set:
    '''Finds intersection of all list params in data dict. For example:
    
    data = {
        'cpu0': {
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'performance',
        },

        'cpu1': {
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'performance',
        },
 
        'cpu2': {
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'performance',
            }
    }

    param = 'available_frequencies'

    Output: {'1700000', '3000000', '1400000'}

    If error will be occurred, you can catch it yourself
    '''

    intersect_data = [set(data[cpu][param]) for cpu in data.keys()]

    return set.intersection(*map(set, intersect_data))

def str_intersection(data: dict, param: str) -> set:
    '''Finds intersection of all str params in data dict. For example:
    data = {
        'cpu0': {
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'performance',
        },

        'cpu1': {
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'performance',
        },
 
        'cpu2': {
            'available_frequencies': ['3000000', '1700000', '1400000'],
            'current_governor': 'performance',
            }
    }

    param = 'current_governor'

    Output: {'performance'}

    If error will be occurred, you can catch it yourself
    '''

    intersect_data = [set([data[cpu][param]]) for cpu in data.keys()]

    return set.intersection(*map(set, intersect_data))

def get_all_merged_params(param_list: list) -> list:
    '''Merge all lists into dict. For example:

    param_list = [
        {   'available_governors': 'scaling_available_governors',
            'available_frequencies': 'scaling_available_frequencies'
        },
        
        {
            'current_governor': 'scaling_governor',
            'min_freq': 'scaling_min_freq',
            'max_freq': 'scaling_max_freq'
        },
        
        {
            'precision_boost': 'boost',
            'cpb': 'cpb'
        }
    ]

    Output: {
        'available_governors': 'scaling_available_governors',
        'available_frequencies': 'scaling_available_frequencies',
        'current_governor': 'scaling_governor',
        'min_freq': 'scaling_min_freq',
        'max_freq': 'scaling_max_freq',
        'precision_boost': 'boost',
        'cpb': 'cpb'
    }
    '''

    result = dict()

    for name in param_list:
        result.update(name)

    return result
