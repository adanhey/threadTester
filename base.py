import requests
from project_info import *
import hashlib
from log import *


class BaseInterface:
    def __init__(self, project_name, log_clean=1):
        self.logger = TestLogger("test_log", log_clean=log_clean)
        self.project_info = projects[project_name]
        self.host = self.project_info['host']
        self.account = self.project_info['account']
        self.password = self.project_info['password']
        try:
            self.headers = {"Cookie": self.get_cookie()}
        except:
            self.headers = {}

    def get_cookie(self):
        url = '%s/itas-app/userLogin' % self.host
        md5_pd = hashlib.md5(self.password.encode(encoding="utf-8")).hexdigest()
        data = {
            "userName": self.account,
            "password": md5_pd,
            "isRemember": "true",
            "checkCode": None
        }
        login_result = requests.post(url=url, data=data)
        return "sid=%s;uwebJwt=%s" % (login_result.json()['sid'], login_result.json()['uwebJwt'])

    def base_request(self, uri, method='post', log_title=None, headers=None, json=None, data=None, params=None):
        url = f'{self.host}{uri}'
        if headers:
            headers['Cookie'] = self.headers['Cookie']
        else:
            headers = self.headers
        result = eval(f"requests.{method}(url='{url}', headers={headers}, json={json}, data={data},params={params})")
        lap = result.elapsed
        result_text = result.text
        if log_title:
            self.logger.log_event(log_title, f"响应时间：{lap} 状态码：{result.status_code} 响应结果{result_text}")
        print(log_title, lap, result_text)
        return result
