# 开发者: 朱仁俊
# 开发时间: 2021/4/9  14:38

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes
