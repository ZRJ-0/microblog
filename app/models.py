# 开发者: 朱仁俊
# 开发时间: 2021/4/1  9:42
from hashlib import md5
from time import time

import jwt

from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 因为Flask-Login对数据库一无所知，所以在加载用户时需要应用程序的帮助
# 因此，扩展期望应用程序配置一个用户加载函数load_user(id),它可以被调用去加载给定ID的用户
@login.user_loader
def load_user(id):
    # 使用 @login.user_loader装饰器向Flask - Login注册用户加载函数
    # Flask - Login传递给函数的id作为一个参数将是一个字符串，所以需要将字符串类型转换为int型以供数据库使用数字ID。
    return User.query.get(int(id))


# 关注者关联表
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


# UserMixin 包含适用于大多数用户模型类的通用实现
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # index 添加索引    为字段设置索引
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # 每次修改数据库时，都必须生成数据库迁移
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship('User',
                               secondary='followers',
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        # return '<User {}>'.format(self.username)
        return '<User {}, Email {}, Password_Hash {}, Posts {}'.format(self.username, self.email,
                                                                       self.password_hash, self.posts)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # avatar() 返回用户头像的URL 并缩放到请求的大小 (以像素为单位)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('UTF-8')).hexdigest()
        return 'http://cn.gravatar.org/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        # 在你所关注的列表中是否存在这个用户的id  有的话返回1  没有则返回0
        return User.query.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        # join() 第一个参数是关注者关联表 第二个参数是连接条件
        # followers.c.follower_id == self.id 你关注的那个人粉丝的id和你的id一致就被筛选出来
        followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        # 找到当前你的id和Post中对应你id的内容    都保存在own中
        own = Post.query.filter_by(user_id=self.id)
        # 将上下两张表合并  根据时间倒序return
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        # 三个参数如下:  (如果别人记住了你邮箱发送的token, 用他的电脑登录这个网址,就会因为载荷(你app配置文件中的密钥)不一致,而导致解密失败)
        # 1.header(头部):头部用于描述关于该JWT的最基本的信息例如其类型以及签名所用的算法等 JSON内容要经Base64编码生成字符串成为Header。
        # 2. payload(载荷):可以简单的理解为我们自己要传输的数据
        # 3. signature(签名)
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')    # .decode('utf-8')
        # python3中只有unicode str 所以把decode方法去掉了 python3环境中 jwt.encode已经是unicodestr了 不用decode
        # decode要求解码的是Byte字节类型的
    @staticmethod
    def verify_reset_password_token(token):
        try:
            # 若别的服务器用相同的地址访问 由于app.config['SECRET_KEY']不一致而导致id和我们的id不一致，就无法进行更改密码
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
                # 成功的话返回的是一个字典 {'reset_password': 3}
                # ['reset_password']就是对值进行提取
        except:
            return
        return User.query.get(id)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # db.DateTime   是DateTime而不是Datetime
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post: {}>'.format(self.body)
