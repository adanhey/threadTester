import threading
import time
from interface_list import *
from base import *


class ThreadMaker(BaseInterface):
    def __init__(self, project_name, rounds, case_list):
        super().__init__(project_name)
        self.logger.log_event("并发数", len(case_list))

    def run_thread(self):
        run_time = 0
        while True:
            self.logger.log_event("并发轮次", run_time + 1)
            run_num = 0
            for interface in interface_list:
                if interface['run_time'] > run_time:
                    cookie = self.get_cookie(login=1)
                    headers = {'Cookie': cookie}
                    url = '%s%s' % (host, interface['uri'])
                    th = threading.Thread(target=self.base_request, args=(
                        url, interface['method'], interface['name'], headers, interface['json'], interface['data']))
                    exec(f"%s = th" % interface['name'])
                    run_num += 1
            for interface in interface_list:
                if interface['run_time'] > run_time:
                    exec(f"%s.start()" % interface['name'])
            time.sleep(0.5)
            if run_num == 0:
                break
            else:
                run_time += 1
