# 导入 Flask 模块和其他所需的模块
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
import functools

# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = "my_secret_key"

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
            # flash('Welcome, {}!'.format(username), 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            return render_template('login.html')
            # return "Invalid username or password"
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
    # if 'admin' in session:
    #     return "Welcome, %s!" % session['admin']
    # else:
    return render_template('index.html')

# 定义关于页面函数
@app.route('/about')
@login_required
def about():
    return "This is a simple Flask website."

# 运行应用
if __name__ == '__main__':
    app.run()
