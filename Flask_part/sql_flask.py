from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import SQLconnect.DBconfig  # 导入配置文件
from datetime import *

app = Flask(__name__)
app.config.from_object(SQLconnect.DBconfig)
db = SQLAlchemy(app)

# 创建表模型类对象
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    publishing_office = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    storage_time = db.Column(db.DateTime, default=datetime.now)


if __name__ == '__main__':
    # 删除数据库下的所有上述定义的表，防止重复创建
    with app.app_context():
        db.drop_all()
        # 将上述定义的所有表对象映射为数据库下的表单（创建表）
        db.create_all()

    # 向表中插入记录：实例化-插入-提交
    #     book1 = Book(title='人工智能导论', publishing_office='高等教育出版社', isbn='9787040479843')
    #     db.session.add(book1)
        db.session.commit()
