import time

from base import BaseInterface
from tools.random_tools import *
from project_data.interface_data import *


class PossibleCheck(BaseInterface):
    def __init__(self, project_name, log_clean=1):
        super().__init__(project_name, log_clean=log_clean)

    def get_from_data(self, interface_name, value_path):
        inter_dic = interfaces[interface_name]
        dic = inter_dic['be_from_data']
        for key, value in dic.items():
            if isinstance(value, dict):
                if "data_from" in value:
                    dic[key] = self.get_from_data(value['data_from']['interface_name'],
                                                  value['data_from']['value_path'])
        if dic['data_type']:
            data_type = dic['data_type']
            result = eval(f"self.base_request(inter_dic['uri'], inter_dic['method'], {data_type}=dic).json()")
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
            if key in ['is_dict', 'is_list', 'data_type', 'list_mark']:
                continue
            if key in make_none:
                dic[key] = None
            elif key in dont_make:
                continue
            elif isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                dic[key] = value
            elif "is_dict" in value:
                dic_data = self.prepare_data(value, make_none=make_none, dont_make=dont_make,
                                             make_repeat=make_repeat, make_over_length=make_over_length)
                dic[key] = dic_data
            elif isinstance(value, list):
                dic[key] = []
                for obj in value:
                    if obj['list_mark'] in make_none:
                        dic[key].append(None)
                    elif obj['list_mark'] in dont_make:
                        continue
                    elif "is_dict" in obj:
                        list_data = self.prepare_data(obj, make_none=make_none, dont_make=dont_make,
                                                      make_repeat=make_repeat, make_over_length=make_over_length)
                        dic[key].append(list_data)
                    else:
                        v = random_data(obj)
                        dic[key].append(v)
            elif "data_from" in value:
                dic[key] = self.get_from_data(value['data_from']['interface_name'], value['data_from']['value_path'])
            else:
                if key in make_over_length:
                    dic[key] = random_data(value, over_length=1)
                else:
                    dic[key] = random_data(value)
        return dic

    def make_case(self, case_dict, make_dict):
        case_list = []
        for key, value in make_dict.items():
            if key in ['is_dict', 'is_list', 'data_type', 'list_mark']:
                continue
            single_case = self.prepare_data(case_dict[case_dict['data_type']], make_none=[key])
            case_list.append(single_case)
            single_case = self.prepare_data(case_dict[case_dict['data_type']], dont_make=[key])
            case_list.append(single_case)
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                continue
            elif "is_dict" in value:
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
                        single_case = self.prepare_data(case_dict[case_dict['data_type']],
                                                        make_none=[obj['list_mark']])
                        case_list.append(single_case)
                        single_case = self.prepare_data(case_dict[case_dict['data_type']],
                                                        dont_make=[obj['list_mark']])
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
                case_i = self.final_case(interfaces[i['interfaceName']], case_num=i['caseNum'])
                for case in case_i:
                    case['interface_info'] = interfaces[i['interfaceName']]
                while case_i:
                    run_cases.append(case_i.pop())
            self.cases_run(run_cases, performance_run=1)
            time.sleep(round_interval)

# a = PossibleCheck("汇服务测试1")
# a.run_case(interfaces['新增产品类别'], performance_run=1)
