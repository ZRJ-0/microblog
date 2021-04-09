# 开发者: 朱仁俊
# 开发时间: 2021/4/9  14:16

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
