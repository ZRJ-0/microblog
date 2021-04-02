# 开发者: 朱仁俊
# 开发时间: 2021/4/1  10:57

from flask import render_template, flash, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
# 将这个装饰器添加到来自Flask的@app.route的装饰器下方时 这个函数将被收到保护 并且不允许未经过身份验证的用户
@login_required
def index():
    posts = [  # 创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
    ]
    # user = session.get('user')
    return render_template('index.html', title='Home', posts=posts)



@app.route('/login',methods=['GET','POST'])
def login():
    # is_authenticated 检查用户是否登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # login_user()函数。这个函数将在登录时注册用户,这意味着用户导航的任何未来页面都将current_user变量设置为该用户
        # 重定向到 next 页面  如果第一次 访问其他页面的时候是需要登录的 会被强制到登录界面 当结束的时候，会回到之前操作的页面
        # 但是当开始访问的就是首页时，返回的next_page 会是空的   所以会是 next_page = url_for('index')重定向到首页
        # 第三种情况 如果登录URL包含next设置为包含域名的完整URL的参数，则将用户重定向到/index页面 比如访问百度州二中完整的URL参数
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        print(user.username)
        print(user.email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

