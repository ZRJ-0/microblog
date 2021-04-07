# 开发者: 朱仁俊
# 开发时间: 2021/4/babel.cfg  10:41

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from flask_babel import lazy_gettext as _l

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(label=_l('Username'), validators=[DataRequired()])
    password = PasswordField(label=_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(label=_l('Remember Me'))
    submit = SubmitField(label=_l('Login'))


class RegistrationForm(FlaskForm):
    username = StringField(label=_l('Username'), validators=[DataRequired()])
    # Email() 确保用户在此字段中键入的内容与电子邮件地址的结构相匹配（省了正则去匹配这是否为一个邮箱地址）
    email = StringField(label=_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(label=_l('Password'), validators=[DataRequired()])
    # EqualTo 将确保其值与第一个密码字段的值相同   EqualTo('password')里面一定要加上''
    password2 = PasswordField(label=_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label=_l('Register'))

    # 这俩个方法会发出数据库查询 如果存在查询结果 则通过触发验证错误ValidationError
    # 将在字段傍边显示包含此异常的消息让用户查看
    def validate_username(self, username=None):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username!'))

    def validate_email(self, email=None):
        Email = User.query.filter_by(email=email.data).first()
        if Email is not None:
            raise ValidationError(_l('Please use a different email address!'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(label=_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(label=_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label=_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(label=_l('Repeat password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label=_l('Request Password Reset'))


class EditProfileForm(FlaskForm):
    username = StringField(label=_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(label=_l('About_Me'), validators=[Length(min=0, max=140)])
    submit = SubmitField(label=_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                # 对于以及注册的用户名 不能让没登录的用户修改当亲前用户的个人信息
                raise ValidationError(_l('Please use a different username!'))
            else:
                # 在用户名没有被注册时 不能允许用户用这个用户名进行提交数据
                raise ValidationError(_l('This username has not been registered!'))


class EmptyForm(FlaskForm):
    submit = SubmitField(_l('Submit'))


class PostForm(FlaskForm):
    post = TextAreaField(label=_l('Say Someting'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(label=_l('Submit'))
