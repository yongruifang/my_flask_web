# 导入 Flask 模块和其他所需的模块
from flask import render_template, session, redirect, url_for, current_app
from flask import copy_current_request_context
from datetime import datetime
from . import main
from .forms import PredictForm
from flask_login import login_required
from .quant.main.prediction import execute
from threading import Thread
from .. import redis_client
import json


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

@main.route('/today_result')
@login_required
def today_result():
    json_string = redis_client.get('value_list')
    print(json_string)
    if json_string != None:
        value_list = json.loads(json_string.decode())
        return render_template('today_result.html',predict_result=value_list)
    return render_template('today_result.html')


def async_execute(morning_stock, afternoon_stock):
    value_list = execute(morning_stock=morning_stock, afternoon_stock=afternoon_stock)
    json_string = json.dumps(value_list)
    redis_client.set('value_list',json_string)
    # json_string = redis_client.get('value_list')
    # print(json_string)  # b'[34, 3]'
    # print(type(json_string)) # <class 'bytes'>
    # value_list = json.loads(json_string.decode())
    # print(value_list) # [34, 3]
    # print(type(value_list)) # <class 'list'>
   

@main.route('/today_execute',methods=['GET','POST'])
@login_required
def today_execute():
    morning = session['morning']
    noon = session['noon']
    # value = execute(morning_stock=morning, afternoon_stock=noon)
    thr = Thread(target=async_execute, args=[morning,noon]) 
    thr.start() 
    return render_template('today_result.html')

@main.route('/today_print',methods=['GET','POST'])
@login_required
def today_print():
    text = session['morning'] + session['noon']
    return render_template('today_result.html',text=text)

@main.route('/history')
def history():
    return render_template('history.html')

@main.route('/benifit')
def benifit():
    return render_template('benifit.html')

# @main.route('/redis/index')
# def redis_index():
#     session['username'] = 'xiaohui'
#     return 'ok'
# @main.route('/redis/get_session')
# def redis_get_session():
#     return session['username']
# @main.route('/redis/set1')
# def redis_set1():
#     redis_client.set('username','xiaoming')
#     redis_client.hset('brother','zhangfei','17')
#     return 'ok'
# @main.route('/redis/set2')
# def redis_set2():
#     user = redis_client.get('username').decode()
#     print(user)
#     brother = redis_client.hgetall('brother')
#     print(brother)
#     # encode编码，就是zhangfei在redis中的真实样子，
#     # brother['zhangfei'.encode()]得到了'17'的编码
#     # 再对其进行解码，得到真正的'17'
#     print(brother['zhangfei'.encode()].decode())
#     return 'ok'
