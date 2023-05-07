from flask import render_template,flash
from . import auth
from ..models import Admin
from .forms import LoginForm,RegistrationForm
from flask import render_template, session, redirect, url_for,request
from flask_login import login_user, logout_user, login_required
from .. import db

# 定义登录函数
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 回调函数，name字段会在用户填写完表单并点击提交按钮后被赋值
    if form.validate_on_submit():
        admin = Admin.query.filter_by(name=form.name.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            # 如果值为 True ，那么会在用户浏览器中写入一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。cookie 默认记住一年
            login_user(admin,form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return  render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(email=form.email.data,
        name=form.name.data,
        password=form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)