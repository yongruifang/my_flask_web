from flask_migrate import Migrate
from application import create_app, db
from application.models import Admin
import click
from threading import Thread
import time 
from application.main.quant.main.prediction import execute
from flask import session
import json
from application import redis_client
import datetime
import pytz

app = create_app()
migrate = Migrate(app, db)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Admin=Admin)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def my_background_task():
    while True:
        # 执行你的任务逻辑
        # 获取当前时间
        current_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        # 获取上午九点的时间
        nine_am = current_time.replace(hour=9,minute=0,second=0,microsecond=0)
        # 获取下午三点的时间
        three_pm = current_time.replace(hour=15, minute=0, second=0, microsecond=0)
        # 判断当前时间
        if nine_am >= current_time or current_time >= three_pm:
            time.sleep(180)
            continue
        json_string = redis_client.get('morning_code_list')
        if json_string!=None:
            morning = json.loads(json_string.decode())
        json_string = redis_client.get('noon_code_list')
        if json_string!=None:
            noon = json.loads(json_string.decode())
        if json_string!=None:
                value_list = execute(morning_stock=morning, afternoon_stock=noon)
                json_string = json.dumps(value_list)
                redis_client.set('value_list',json_string)
                print("Running background task...")
        time.sleep(60)

@app.before_first_request
def activate_background_task():
    thread = Thread(target=my_background_task)
    thread.start()


@app.route('/test')
def test():
    return "<h1>欢迎访问我的网站</h1>";

if __name__ == '__main__':
    app.run()

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status,response_headers)
    return ['Hello,World!']
