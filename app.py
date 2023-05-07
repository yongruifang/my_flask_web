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
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir,'admin.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admin'
    name = db.Column(db.String(64),primary_key = True)
    password = db.Column(db.String(64),unique=False)

    def __repr__(self):
        return '<Admin %r>' %self.name



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
             (name TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# 添加一个管理员（如果管理员不存在）
c.execute("SELECT * FROM admin WHERE name=?", ("admin",))
if not c.fetchone():
    c.execute("INSERT INTO admin VALUES (?, ?)", ("admin", "666"))
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
    form = NameForm()
    # 回调函数，name字段会在用户填写完表单并点击提交按钮后被赋值
    if form.validate_on_submit():
        name = form.name.data
        # 验证
        password = form.password.data
        # conn = sqlite3.connect('admin.db')
        # c = conn.cursor()
        # c.execute("SELECT * FROM admin WHERE name=? AND password=?", (name, password))
        # admin = c.fetchone()
        # conn.close()
        admin = Admin.query.filter_by(name=form.name.data,password=form.password.data).first()
        if admin:
            session['name'] = name
            return redirect(url_for('index'))
        return render_template('login.html',form=form, name=session.get('name')) 
    return   render_template('login.html',form=form,name=session.get('name'))

# 定义注销函数
@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('index'))

# 定义主页函数
@app.route('/')
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data=''
    return render_template('index.html', current_time=datetime.utcnow(),form=form,name=session.get('name'))

# 定义关于页面函数
@app.route('/about')
@login_required
def about():
    return "This is a simple Flask website."

# 装饰器函数，用于在启动交互式shell时，自动加载应用程序中的对象
# 返回的字典中的每个键都是在shell中可用的名称，值是要注册的对象
@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Admin=Admin)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
