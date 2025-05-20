def list_intersection(data: dict, param: str) -> set:
    intersect_data = [set(data[cpu][param]) for cpu in data.keys()]
    
    return set.intersection(*map(set, intersect_data))

def str_intersection(data: dict, param: str) -> set:
    intersect_data = [set([data[cpu][param]]) for cpu in data.keys()]
    
    return set.intersection(*map(set, intersect_data))

def get_all_merged_params(param_list) -> list:
    ALL_PARAMS_DICT = dict()
    
    for name in param_list:
        ALL_PARAMS_DICT.update(name)
    
    return ALL_PARAMS_DICT