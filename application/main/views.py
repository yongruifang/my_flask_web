# 导入 Flask 模块和其他所需的模块
from flask import render_template, session, redirect, url_for
from datetime import datetime
from . import main
from .forms import PredictForm
from flask_login import login_required
from .quant.main.prediction import execute

# 定义主页函数
@main.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow(),name=session.get('name'))

@main.route('/intro')
@login_required
def intro():
    return render_template('intro.html')

@main.route('/today_input', methods=['GET', 'POST'])
@login_required
def today_input():
    predictForm = PredictForm()
    value = None
    if predictForm.validate_on_submit():
        morning = predictForm.morning_stocks.data.split(' ')
        noon = predictForm.afternoon_stocks.data.split(' ')
        # 保存到会话中
        session['morning'] = morning
        session['noon'] = noon
        return redirect(url_for('main.today_result'))
    else:
        return render_template('today_input.html',predictForm=predictForm)

@main.route('/today_result', methods=['GET', 'POST'])
@login_required
def today_result():
    return render_template('today_result.html')

@main.route('/today_execute',methods=['GET','POST'])
def today_execute():
    morning = session['morning']
    noon = session['noon']
    value = execute(morning_stock=morning,afternoon_stock=noon)
    return render_template('today_result.html',value=value)

@main.route('/today_print',methods=['GET','POST'])
def today_print():
    text = session['morning'] + session['noon']
    return render_template('today_result.html',text=text)

@main.route('/history')
def history():
    return render_template('history.html')

@main.route('/benifit')
def benifit():
    return render_template('benifit.html')