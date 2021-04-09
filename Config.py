# 开发者: 朱仁俊
# 开发时间: 2021/4/babel.cfg  9:50
import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前.py文件的绝对路径
from dotenv import load_dotenv

load_dotenv(os.path.join(basedir, 'microblog.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    # 中文语言代码zh (zh - HK香港 zh - MO澳门 zh - TW台湾 zh - SG新加坡)
    LANGUAGES = ['en','zh']     # 注意: 不要填写zh_CN。有坑！
    # 禁用缓存并强制重新加载模板
    TEMPLATES_AUTO_RELOAD = True
    POSTS_PER_PAGE = 5  # 每页设置显示的帖子数量
    ADMINS = ['1061083419@qq.com']
    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_PORT = 465
    # MAIL_USERNAME = "1061083419@qq.com"
    # MAIL_PASSWORD = "tpfjraqedtvibejj"
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', 'babel.cfg']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    APPID = os.environ.get('APPID')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
