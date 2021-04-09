# 开发者: 朱仁俊
# 开发时间: 2021/4/5  15:01

from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(505)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# 两个函数都在模板后面返回第二个值 即错误代码编号 对于到目前为止 创建的所有视图函数 都不需要添加第二个返回值
# 因为默认值为200(成功响应的状态代码) 在这种情况下 这些是错误页面 所以希望响应的状态代码能够反映出来
# 在数据库错误之后 可以调用500错误的错误处理程序 实际上是上面的用户名重复情况 为确保任何失败的数据库会话
# 不会干扰模板触发的任何数据库访问 发出一个会话回滚(session rollback)将会使得会话重置为干净状态。
