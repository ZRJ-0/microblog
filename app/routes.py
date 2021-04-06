# 开发者: 朱仁俊
# 开发时间: 2021/4/1  10:57
from datetime import datetime, timedelta

from flask import render_template, flash, url_for, session, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, db
from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.models import User, Post


# 在用户向服务器发送请求时 为给定用户写入此字段的当前时间
@app.before_request
def before_request():
    if current_user.is_authenticated:
        # 加上8小时就是北京时间
        current_user.last_seen = datetime.utcnow() + timedelta(hours=8)
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# 将这个装饰器添加到来自Flask的@app.route的装饰器下方时 这个函数将被收到保护 并且不允许未经过身份验证的用户
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post is now live!')
        return redirect('index')
    # posts = [  # 创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    # user = session.get('user')
    # followed_posts()方法 它返回给定用户想看的帖子的查询  页面上存在您的言论和你关注者的言论
    # 没有指定页码就是 1 指定了就是对应的页码
    page = request.args.get('page', 1, type=int)
    # paginate的三个参数: 1、页码 从1开始 2、每页的项目数 3、错误标志
    # 若为True 当请求超出范围的页面时 404 错误将自动返回给客户端 若为False 超出范围的页面将返回一个空列表
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    # posts.items type:list -->[<Post: 333>, <Post: 测试中！ >, <Post: 2222222>]
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    # has_next 如果当前页面后面至少还有一页 则为True    next_num 下一页的页码
    # has_prev 如果当前页面之前至少还有一页 则为True    prev_num 上一页的页码
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
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
        # 第三种情况 如果登录URL包含next设置为包含域名的完整URL的参数(netloc(域名服务器))
        # 则将用户重定向到/index页面 比如访问百度(www.baidu.com(完整的URL))就算是.netloc != ''
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

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # 获取email和保存在User表中相等的那个user对象
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your Password has been reset!')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    # 有结果的情况下它与first()完全一样 不过在没有结果的情况下 会自动将404 error发送回客户端
    user = User.query.filter_by(username=username).first_or_404()
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', title='user', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # 如果validate_on_submit()返回True 将表单中的数据复制到用户对象中 然后将对象写入数据库
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your Changes Have Been Saved!')
        # 也可以不重定向   在html加一个可以返回的链接
        # return redirect(url_for('edit_profile'))
    # 对初始化请求这将是GET 并对验证失败的提交将是POST 返回到edit_profile.html 页面
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
