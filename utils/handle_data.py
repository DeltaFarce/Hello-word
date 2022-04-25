from utils.instance_type import handle_params_type


def handle_data1(data):
    """
    将{'Content-Type': 'application/json', 'device_sn': '$device_sn'}
    处理成[{'key':'Content-Type', 'value':'application/json'}, {'key': 'device_sn', 'value': '$device_sn'}]
    """
    data_list = []
    if data is not None:
        for key, value in data.items():
            data_list.append({
                'key': key,
                'value': value
            })
    return data_list


def handle_data2(data):
    """
     将 [{"user_agent": "iOS/10.3"},{"device_sn": "${gen_random_string(15)"},{"os_platform": "ios"}]
     处理成 [{'key':'user_agent', 'value': 'iOS/10.3', 'type': 'string'}, {'key': 'device_sn', 'value': '${gen_random_string(15)', 'type': 'string'}]
    """
    variables_list = []
    if data is not None:
        for data_dict in data:
            key = list(data_dict)[0]
            value = data_dict.get(key)
            ty = handle_params_type(value)
            variables_list.append({
                'key': key,
                'value': value,
                'type': ty
            })
    return variables_list


def handle_data3(data):
    """
    [{'eq': ['status_code', 200]}, {'eq': ['headers.Content-Type', 'application/json']}, {'eq': ['content.sess', True]}]
    转成[{key:'status_code,value:200,comparator:'equals',param_type:'string'}]
    """
    result_list = []
    if data is not None:
        for one_validate_dict in data:
            key = list(one_validate_dict)[0]
            value = one_validate_dict.get(key)[1]
            comparator = one_validate_dict.get(key)[0]
            result_list.append({
                "key": key,
                "value": value,
                "comparator": comparator,
                'param_type': handle_params_type(value)
            })
    return result_list


def handle_data5(data):
    """
    处理第五种类型的数据转化
    将['${setup_hook_prepare_kwargs($request)}','${setup_hook_httpntlmauth($request)}']
    转化为：[{key:'${setup_hook_prepare_kwargs($request)}'}, {key:'${setup_hook_httpntlmauth($request)}'}]
    """
    hooks_list = []
    if data is not None:
        for k in data:
            hooks = {
                'key': k
            }
            hooks_list.append(hooks)
    return hooks_list
