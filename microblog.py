# 开发者: 朱仁俊
# 开发时间: 2021/4/1  9:48

from app import app, db
from app.models import User, Post

# 此装饰器注册了一个作为shell 上下文功能的函数
# 当运行flask shell命令时，它将调用此函数并在shell会话中注册它返回的项。
@app.shell_context_processor
def make_shell_context():
    # 函数返回字典而不是列表的原因是：对于每个项目，我们还须提供一个名称.
    # 在这个名称下，它将在shell中被引用，由字典的键给出。
    return {'db': db, 'User': User, 'Post': Post}
if __name__ == '__main__':
    app.run(debug=True)
