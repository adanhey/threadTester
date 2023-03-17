import time
from base import BaseInterface
from tools.random_tools import *
from project_data.interface_data import *
from SQLconnect.db_file import *
from tools.mysql_base import ProjectMysql
import threading


class PossibleCheck(BaseInterface):
    def __init__(self, project_id, env_name, log_clean=1, database='flaskdb'):
        super().__init__(project_id, env_name, log_clean=log_clean)
        self.database = database
        self.db = ProjectMysql(self.database)

    def make_interface_dict(self, interface_name):
        re_dic = {}
        sql = f"SELECT id,uri,method,name,data_type FROM interface where name = '{interface_name}' and project_id = {self.project_id}"
        interface_info = self.db.select_data(sql)
        re_dic['uri'] = interface_info[0][1]
        re_dic['method'] = interface_info[0][2]
        re_dic['name'] = interface_info[0][3]
        re_dic['data_type'] = interface_info[0][4]
        if re_dic['data_type']:
            re_dic[re_dic['data_type']] = self.make_field_dict(interface_info[0][0], 0)
        return re_dic

    def make_field_dict(self, interface_id, parent_id, data_type="dict"):
        if data_type == "dict":
            field_dic = {}
        else:
            field_dic = []
        if parent_id == 0:
            field_info = self.db.select_data(
                f"SELECT * FROM interfacefield where interface_id = {interface_id} and parent_field is null")
        else:
            field_info = self.db.select_data(
                f"SELECT * FROM interfacefield where interface_id = {interface_id} and parent_field = {parent_id}")
        if isinstance(field_dic, dict):
            for info in field_info:
                if info[6] == 'data_from':
                    field_dic[info[2]] = {'data_from': {}}
                    field_dic[info[2]]['data_from']['interface_id'] = info[4]
                    field_dic[info[2]]['data_from']['value_path'] = info[5]
                elif info[6] == 'list':
                    result = self.make_field_dict(info[1], info[0], "list")
                    field_dic[info[2]] = result
                    field_dic[info[2]]['data_type'] = 'list'
                elif info[6] == 'dict':
                    result = self.make_field_dict(info[1], info[0], "dict")
                    field_dic[info[2]] = result
                    field_dic[info[2]]['data_type'] = 'dict'
                else:
                    if info[3]:
                        field_dic[info[2]] = info[3]
                    else:
                        field_dic[info[2]] = {'data_type': info[6], 'data_length': info[7], 'data_range': info[8],
                                              'decimal_range': info[9]}
                if info[12] == 1:
                    field_dic[info[2]]['delete_mark'] = 1
        elif isinstance(field_dic, list):
            for info in field_info:
                if info[6] == 'data_from':
                    mid_dic = {'data_from': {}}
                    mid_dic['data_from']['interface_id'] = info[4]
                    mid_dic['data_from']['value_path'] = info[5]
                    field_dic.append(mid_dic)
        return field_dic

    def get_from_data(self, interface_id, value_path):
        sql = f"select * from interface where id = {interface_id}"
        interface_info = self.db.select_data(sql)[0]
        dic = json.loads(interface_info[7])
        for key, value in dic.items():
            if isinstance(value, dict):
                if "data_from" in value:
                    dic[key] = self.get_from_data(value['data_from']['interface_id'],
                                                  value['data_from']['value_path'])
        if dic['data_type']:
            data_type = dic['data_type']
            result = eval(f"self.base_request('{interface_info[2]}', '{interface_info[4]}', {data_type}=dic).json()")
        else:
            result = self.base_request(dic['uri'], dic['method']).json()
        final_result = self.final_result(result, value_path)
        return final_result

    def final_result(self, result, value_path):
        fin_re = result
        for i in value_path:
            fin_re = fin_re[i]
        return fin_re

    def prepare_data(self, case_dict, dic=None, make_none=[], dont_make=[], make_repeat=[],
                     make_over_length=[]):
        if dic is None:
            dic = {}
        for key, value in case_dict.items():
            if key in ['data_type'] or key in dont_make:
                continue
            elif key in make_none:
                dic[key] = None
            elif isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                dic[key] = value
            elif value['data_type'] == 'dict':
                dic_data = self.prepare_data(value, make_none=make_none, dont_make=dont_make,
                                             make_repeat=make_repeat, make_over_length=make_over_length)
                dic[key] = dic_data
            elif isinstance(value, list):
                dic[key] = []
                for obj in value:
                    if obj['datatype'] == 'dict':
                        list_data = self.prepare_data(obj, make_none=make_none, dont_make=dont_make,
                                                      make_repeat=make_repeat, make_over_length=make_over_length)
                        dic[key].append(list_data)
                    else:
                        v = random_data(obj)
                        dic[key].append(v)
            elif "data_from" in value:
                dic[key] = self.get_from_data(value['data_from']['interface_id'], value['data_from']['value_path'])
            else:
                if key in make_over_length:
                    dic[key] = random_data(value, over_length=1)
                elif 'delete_mark' in value:
                    dic[key] = random_data(value, over_length=1, delete_mark=1)
                else:
                    dic[key] = random_data(value)
        return dic

    def make_case(self, case_dict, make_dict):
        case_list = []
        for key, value in make_dict.items():
            if key in ['data_type']:
                continue
            single_case = self.prepare_data(case_dict[case_dict['data_type']], make_none=[key])
            case_list.append(single_case)
            single_case = self.prepare_data(case_dict[case_dict['data_type']], dont_make=[key])
            case_list.append(single_case)
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                continue
            elif value['data_type'] == 'dict':
                cases = self.make_case(case_dict, value)
                while True:
                    if not cases:
                        break
                    case_list.append(cases.pop())
            elif isinstance(value, list):
                for obj in value:
                    if "is_dict" in value:
                        cases = self.make_case(case_dict[case_dict['data_type']], obj)
                        while True:
                            if not cases:
                                break
                            case_list.append(cases.pop())
                    else:
                        single_case = self.prepare_data(case_dict[case_dict['data_type']])
                        case_list.append(single_case)
        return case_list

    def performance_case_maker(self, case_num, case_dict):
        case_list = []
        for i in range(case_num):
            case = self.prepare_data(case_dict[case_dict['data_type']])
            case_list.append(case)
        return case_list

    def run_thread(self, cases, wait_finish=None):
        for i in range(len(cases)):
            case = cases[i]
            interface_info = case['interface_info']
            del (case['interface_info'])
            exec(
                f"th{i} = threading.Thread(target=self.base_request, args=(interface_info['uri'],interface_info["
                f"'method'],interface_info['name'],None,case))")
        for i in range(len(cases)):
            exec(f"th{i}.start()")
        time.sleep(0.1)
        if wait_finish:
            for i in range(len(cases)):
                while True:
                    time.sleep(0.05)
                    if not eval(f"th{i}.is_alive()"):
                        break

    def final_case(self, interface_info, run_type=1, case_num=10):
        # 类型1随机并发
        if run_type == 1:
            cases = self.performance_case_maker(case_num, interface_info)
        # 类型2接口全量验证
        elif run_type == 2:
            cases = self.make_case(interface_info, interface_info['json'])
        else:
            cases = []
        return cases

    def cases_run(self, cases, performance_run=None):
        if performance_run:
            self.run_thread(cases)
        else:
            for i in cases:
                interface_info = i['interface_info']
                del (i['interface_info'])
                result = eval(
                    f"self.base_request(interface_info['uri'],interface_info['method'],interface_info['name'],"
                    f"{interface_info['data_type']}=i)")

    def interface_mid(self, cases_info, rounds=1, round_interval=1):
        for ro in range(rounds):
            run_cases = []
            for i in cases_info:
                case_i = self.final_case(self.make_interface_dict(i['interface_name']), case_num=i['caseNum'])
                for case in case_i:
                    case['interface_info'] = self.make_interface_dict(i['interface_name'])
                while case_i:
                    run_cases.append(case_i.pop())
            self.cases_run(run_cases, performance_run=1)
            time.sleep(round_interval)
