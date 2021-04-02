# 开发者: 朱仁俊
# 开发时间: 2021/4/1  10:57

from flask import render_template, flash, url_for, session
from werkzeug.utils import redirect

from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
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
    user = session.get('user')
    return render_template('index.html', title='Home', user=user, posts=posts)



@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
        session['user'] = form.username.data
        # return redirect('/index')
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)

