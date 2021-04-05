# 开发者: 朱仁俊
# 开发时间: 2021/4/1  9:50
import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.getcwd()+'/blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    # 禁用缓存并强制重新加载模板
    TEMPLATES_AUTO_RELOAD = True
