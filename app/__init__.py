# 开发者: 朱仁俊
# 开发时间: 2021/4/1  11:09

# 这个文件初始化了你的应用并把所有其它的组件组合在一起
import os, logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# Flask-Login通过在Flask的用户会话中存储其唯一的标识符来跟踪登录用户
# 这个用户会话是分配给连接到应用程序的每个用户的存储空间。
# 每次登录用户导航到新页面时，Flask-Login都会从会话中检索用户的ID，然后将用户加载到内存中。
from flask_login import LoginManager
from Config import Config  # 从config模块导入Config类

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)  # 数据库对象
migrate = Migrate(app, db)  # 迁移数据库对象

login = LoginManager(app)
# 强制用户在查看应用程序的某些页面之前必须登录 如果未登录用户尝试查看受保护的页面
# Flask-Login将自动将用户重定向到登录表单 并且仅在登录过程完成后重定向回用户想要查看的页面
login.login_view = 'login'
mail = Mail(app)
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors  # 导入一个新模块models，它将定义数据库的结构，目前为止尚未编写
