from interface_possible_check import *
from functools import wraps
from sign_compare import *
from http import HTTPStatus
from flask import Flask, request

app = Flask(__name__)
ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.json")


def permission(func):
    @wraps(func)
    def inner():
        if 'Authorization' not in request.headers:
            return {"message": "headers缺少Authorization", "status_code": 401}, 401
        auth = request.headers['Authorization']
        if not sign_compare(auth):
            return {"message": "签名校验失败", "status_code": HTTPStatus.FORBIDDEN}, 403
        return func()

    return inner


@app.errorhandler(403)
def handle_403_error(err):
    return {"message": "签名校验失败", "status_code": HTTPStatus.FORBIDDEN}


@app.route('/runCase', methods=['POST'])
@permission
def run_case():
    environment = request.json['environment']
    interface_data = request.json['interfaceData']
    rounds, round_interval = 1, 1
    if 'rounds' in request.json:
        rounds = request.json['rounds']
    if 'round_interval' in request.json:
        round_interval = request.json['round_interval']
    a = PossibleCheck(environment)
    interface_th = threading.Thread(target=a.interface_mid, args=(interface_data, rounds, round_interval))
    interface_th.start()
    return {"message": "任务下发成功", "filepath": f"{a.logger.now_time}{a.logger.log_sign}.log"}


@app.route('/getLog', methods=['GET'])
@permission
def get_log():
    path = request.args.get('fileName')
    with open(f"./{path}", 'rb') as request_logs:
        response = request_logs.read()
        request_logs.close()
    return response


if __name__ == "__main__":
    app.run(host='10.53.3.46')
