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
                    print(value)
                    dic[key] = self.get_from_data(value['data_from']['interface_name'],
                                                  value['data_from']['value_path'])
        if dic['data_type']:
            data_type = dic['data_type']
            del (dic['data_type'])
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

    def prepare_data(self, case_dict, dic=None):
        if dic is None:
            dic = {}
        for key, value in case_dict.items():
            if "is_dict" in value:
                del (value['is_dict'])
                dic_data = self.prepare_data(value)
                dic[key] = dic_data
            elif isinstance(value, list):
                dic[key] = []
                for obj in value:
                    if "is_dict" in obj:
                        del (obj['is_dict'])
                        list_data = self.prepare_data(obj)
                        dic[key].append(list_data)
                    else:
                        v = random_data(obj)
                        dic[key].append(v)
            elif "data_from" in value:
                dic[key] = self.get_from_data(value['data_from']['interface_name'], value['data_from']['value_path'])
            else:
                dic[key] = random_data(value)
        return dic

    def case_run(self, case_num, case_dict, run_type=1, run_title="随机"):
        data = eval(f"self.prepare_data(case_dict[{case_dict['data_type']}])")
        result = eval(f"self.base_request(case_dict['uri'], case_dict['method'], run_title,{case_dict['data_type']}=data)")


a = PossibleCheck("汇服务")
print(a.prepare_data(interfaces['test']['json']))
