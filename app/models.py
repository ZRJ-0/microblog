# 开发者: 朱仁俊
# 开发时间: 2021/4/1  9:42

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# UserMixin 包含适用于大多数用户模型类的通用实现
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # index 添加索引    为字段设置索引
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Username: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # db.DateTime   是DateTime而不是Datetime
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post: {}>'.format(self.body)
