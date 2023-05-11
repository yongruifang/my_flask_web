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

app = create_app()
migrate = Migrate(app, db)

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
        json_string = redis_client.get('morning_code_list')
        morning = json.loads(json_string.decode())
        json_string = redis_client.get('noon_code_list')
        noon = json.loads(json_string.decode())
        value_list = execute(morning_stock=morning, afternoon_stock=noon)
        json_string = json.dumps(value_list)
        redis_client.set('value_list',json_string)
        print("Running background task...")
        time.sleep(60)

@app.before_first_request
def activate_background_task():
    thread = Thread(target=my_background_task)
    thread.start()


if __name__ == '__main__':
    app.run(debug=True)