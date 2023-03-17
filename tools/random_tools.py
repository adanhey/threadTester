from project_data.random_data import *
import random


def random_data(data_dic, over_length=None, delete_mark=None):
    data = []
    if data_dic["data_type"] == 'str':
        if over_length:
            data_dic['data_length'] += 1
        elif delete_mark:
            data_dic['data_length'] -= 3
        for i in range(data_dic['data_length']):
            s = random.randint(0, len(random_str) - 1)
            data.append(str(random_str[s]))
        re_data = "".join(data)
        if delete_mark:
            re_data = f"可删除{re_data}"
    elif data_dic["data_type"] == 'int':
        if over_length:
            data_dic['data_range'][0] = data_dic['data_range'][1] + 1
            data_dic['data_range'][1] = data_dic['data_range'][1] + 2
        re_data = random.randint(data_dic['data_range'][0], data_dic['data_range'][1])
    else:
        if over_length:
            data_dic['data_range'][0] = data_dic['data_range'][1] + 1
            data_dic['data_range'][1] = data_dic['data_range'][1] + 2
        re_data_part1 = random.randint(data_dic['data_range'][0], data_dic['data_range'][1] - 1)
        re_data_part2 = random.randint(data_dic['decimal_range'][0], data_dic['decimal_range'][1])
        re_data = float(f"{re_data_part1}.{re_data_part2}")
    return re_data
