# 开发者: 朱仁俊
# 开发时间: 2021/4/5  22:19
from threading import Thread

from flask import render_template
from flask_mail import Message
from app import mail, app
from flask_babel import _

def send_async_email(app, msg):
    # with app.app_context()调用创建的应用程序上下文
    # 使得应用程序实例可以通过 来自Flask的current_app变量 可访问
    with app.app_context():
        mail.send(msg)

# 将发送电子邮件到recipients参数的电子邮件地址列表
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
