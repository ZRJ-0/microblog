# 开发者: 朱仁俊
# 开发时间: 2021/4/1  11:09

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Config import Config   #从config模块导入Config类

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)    # 数据库对象
migrate = Migrate(app, db)  # 迁移数据库对象

login = LoginManager(app)

from app import routes, models #导入一个新模块models，它将定义数据库的结构，目前为止尚未编写
