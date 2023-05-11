from mycelery import make_celery
from flask import Flask

app = Flask(__name__)
celery = make_celery(app)

@app.route('/hello')
def index():
    result = app.celery.send_task("atask",(2,3))
    return "hello"

if __name__ == '__main__':
    app.run()