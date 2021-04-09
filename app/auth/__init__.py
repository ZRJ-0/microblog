# 开发者: 朱仁俊
# 开发时间: 2021/4/9  14:32

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes
