import re


def process_env_data(data):
    envs_list = []
    for item in data:
        env_data_create_time = re.search(r'(.*)T(.*)\..*', item['create_time'])
        item['create_time'] = env_data_create_time.group(1) + " " + env_data_create_time.group(2)

        env_data_update_time = re.search(r'(.*)T(.*)\..*', item['update_time'])
        item['update_time'] = env_data_update_time.group(1) + " " + env_data_update_time.group(2)

        envs_list.append(item)
    return envs_list

