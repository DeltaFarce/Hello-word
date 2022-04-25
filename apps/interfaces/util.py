import re


def process_interfaces_data(data):
    process_list = []
    for item in data:
        process_data = re.search(r'(.*)T(.*)\..*', item['create_time'])
        item['create_time'] = process_data.group(1) + " " + process_data.group(2)
        process_list.append(item)
    return process_list
