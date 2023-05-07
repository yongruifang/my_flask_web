from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

basedir = os.path.abspath(os.path.dirname(__file__))

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name='production'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # app.secret_key = "my_secret_key"
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    # 'sqlite:///' + os.path.join(basedir,'data.sqlite')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app