import re


def format_report_reponse(data):
    report_list = []
    for report in data:
        report_createtime = report['create_time']
        createtime = re.search(r'(.*)T(.*)\..*', report_createtime)
        report['create_time'] = createtime.group(1) + " " + createtime.group(2)
        report_list.append(report)
    return report_list


def format_report(data):
    report_createtime = data['create_time']
    createtime = re.search(r'(.*)T(.*)\..*', report_createtime)
    data['create_time'] = createtime.group(1) + " " + createtime.group(2)
    return data


def get_file_contents_byte(filename, chunk_size=521):
    with open(filename, encoding='utf-8') as f:
        while True:
            file = f.read(chunk_size)
            if file:
                yield file
            else:
                break