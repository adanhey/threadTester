from interface_possible_check import *
from functools import wraps
from Flask_part.sign_compare import *
from http import HTTPStatus
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import DBconfig
from datetime import *

app = Flask(__name__)
ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.json")
app.config.from_object(DBconfig)
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    publishing_office = db.Column(db.String(100), nullable=True)
    price = db.Column(db.String(30), nullable=True)
    isbn = db.Column(db.String(100), nullable=True)
    storage_time = db.Column(db.DateTime, default=datetime.now)


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


@app.route('/createInterface', methods=['POST'])
@permission
def create_interface():
    require_data = ['title']
    full_data = ['title', 'publishing_office', 'price', 'isbn']
    interface_info = request.json
    if isinstance(interface_info, list):
        add_result = []
        for i in range(len(interface_info)):
            a = 0
            for require in require_data:
                if require not in interface_info[i]:
                    add_result.append(f"第{i + 1}条数据缺少{require}")
                    a = 1
                    break
            if a == 1:
                continue
            elif Book.query.filter(Book.title == interface_info[i]['title']).first():
                add_result.append(f"{interface_info[i]['title']}已存在")
            else:
                for data in full_data:
                    if data in interface_info[i]:
                        exec(f"{data} = interface_info[i]['{data}']")
                    else:
                        exec(f"{data} = ''")
                book = eval("Book(title=title, publishing_office=publishing_office,price=price, isbn=isbn)")
                db.session.add(book)
        db.session.commit()
        return {"失败结果": add_result}
    else:
        return {"message": "请求体错误"}, 400


if __name__ == "__main__":
    app.run(host='10.53.3.46')
