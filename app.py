# 导入 Flask 模块和其他所需的模块
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import functools
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = "my_secret_key"

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    # StringField和SubmitField是Flask-WTF中的类，用于生成HTML表单元素
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# 连接数据库
conn = sqlite3.connect('admin.db')
c = conn.cursor()

# 创建管理员表格（如果不存在）
c.execute('''CREATE TABLE IF NOT EXISTS admin
             (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# 添加一个管理员（如果管理员不存在）
c.execute("SELECT * FROM admin WHERE username=?", ("admin",))
if not c.fetchone():
    c.execute("INSERT INTO admin VALUES (?, ?)", ("admin", "password"))
    conn.commit()

# 关闭数据库连接
conn.close()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# 定义登录函数
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('admin.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()
        if admin:
            session['admin'] = admin[0]
            # return redirect(url_for('index'))
            form = NameForm()
            # 回调函数，name字段会在用户填写完表单并点击提交按钮后被赋值
            if form.validate_on_submit():
                name = form.name.data
                form.name.data=''
            return render_template('index.html', name=username,current_time=datetime.utcnow(),form=form)
        else:
            flash('Invalid username or password', 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')

# 定义注销函数
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

# 定义主页函数
@app.route('/')
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data=''
    return render_template('index.html', current_time=datetime.utcnow(),form=form)

# 定义关于页面函数
@app.route('/about')
@login_required
def about():
    return "This is a simple Flask website."

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
