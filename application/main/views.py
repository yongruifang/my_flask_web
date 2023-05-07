# 导入 Flask 模块和其他所需的模块
from flask import render_template, session, redirect, url_for
import functools
from datetime import datetime
from ..models import Admin
from . import main
from .forms import NameForm

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('.login'))
        return view(**kwargs)
    return wrapped_view

# 定义登录函数
@main.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('.index'))
        return render_template('login.html',form=form, name=session.get('name')) 
    return   render_template('login.html',form=form,name=session.get('name'))

# 定义注销函数
@main.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('.index'))

# 定义主页函数
@main.route('/')
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data=''
    return render_template('index.html', current_time=datetime.utcnow(),form=form,name=session.get('name'))

# 定义关于页面函数
@main.route('/about')
@login_required
def about():
    return "This is a simple Flask website."