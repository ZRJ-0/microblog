# microblog
### This is my first program for Flask

#### blueprint 翻译功能密码重置功能无效的话 对env文件中的变量在shell中进行  set 

(venv) D:\microblog>set FLASK_APP=microblog.py

(venv) D:\microblog>set MAIL_SERVER=smtp.qq.com

(venv) D:\microblog>set MAIL_PORT=465

(venv) D:\microblog>set MAIL_USE_SSL=True

(venv) D:\microblog>set MAIL_USERNAME=you-qq@qq.com

(venv) D:\microblog>set MAIL_PASSWORD=授权码

(venv) D:\microblog>set APPID=百度翻译API appid

(venv) D:\microblog>set BD_TRANSLATOR_KEY=百度翻译API secretKey

flask translate update 对标记的语言进行更新
flask translate compile 对语言进行编译 使得网页中的文字得到刷新

AppContext        应用上下文，是对flask一切对象的封装
RequestContext    请求上下文，是对request请求对象的封装
current_app       像全局变量一样工作，但只能在处理请求期间且在处理它的线程中访问 返回的栈顶元素不是应用上下文，而是flask的应用实例对象

(py3) D:\Python Web框架项目实战\microblog>sqlite3 blog.db   进入到sqlite中
SQLite version 3.35.4 2021-04-02 15:20:15
Enter ".help" for usage hints.
sqlite> select * from post;
1|First Message for John!|2021-04-02 07:31:59.183192|1|en
2|Second Message!|2021-04-02 07:31:59.184230|2|en
3|Second Message for u1 too!|2021-04-02 07:31:59.185186|2|en
4|Wise men learn by other men's mistakes; fools by their own.|2021-04-09 04:10:02.423660|3|en
5|Money spent on the brain is never spent in vain. |2021-04-09 04:10:17.114598|3|en
6|ciao, come va oggi?|2021-04-09 04:10:36.105347|3|en
7|?Hola, cómo estás hoy?|2021-04-09 04:10:50.113704|3|en
8|Experience is the mother of wisdom.|2021-04-09 04:11:14.578638|2|en
9|Hello World!|2021-04-09 07:29:28.113768|3|
10|Hello World!|2021-04-09 08:00:52.130992|3|en
11|Experience is the mother of wisdom.|2021-04-09 08:14:31.582341|3|en

sqlite> delete from user where username='jxw';    删除数据
sqlite> insert into post values (12, 'Hello World!', '2021-04-01 07:31:59.183192', 2, 'en');    插入数据
sqlite> .quit   退出sqlite数据库
