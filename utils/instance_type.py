def handle_params_type(value):
    if isinstance(value, int):
        return 'int'
    elif isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, float):
        return 'float'
    else:
        return 'string'
