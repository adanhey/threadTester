from Flask_part.sign_compare import *
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import SQLconnect.DBconfig
from datetime import *

app = Flask(__name__)
ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.json")
app.config.from_object(SQLconnect.DBconfig)
db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    host = db.Column(db.String(100), nullable=False)
    account = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    auth_method = db.Column(db.String(100), nullable=True)
    storage_time = db.Column(db.DateTime, default=datetime.now)


class Interface(db.Model):
    __tablename__ = 'interface'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, nullable=False)
    uri = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    method = db.Column(db.String(30), nullable=True)
    data_type = db.Column(db.String(100), nullable=True)
    storage_time = db.Column(db.DateTime, default=datetime.now)


class InterfaceField(db.Model):
    __tablename__ = 'interfaceField'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interface_id = db.Column(db.Integer, nullable=False)
    filed_name = db.Column(db.String(50), nullable=False)
    data_from_interface = db.Column(db.String(50), nullable=True)
    data_from_value_path = db.Column(db.String(100), nullable=True)
    data_type = db.Column(db.String(30), nullable=False)
    data_length = db.Column(db.Integer, nullable=True)
    data_range = db.Column(db.String(1000), nullable=True)
    decimal_range = db.Column(db.String(1000), nullable=True)
    parent_field = db.Column(db.Integer, nullable=True)
    storage_time = db.Column(db.DateTime, default=datetime.now)
