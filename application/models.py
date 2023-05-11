from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(64),unique=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True,index=True)

    # 修改password属性为只写，不可读，并添加一个新的方法set_password来设置password_hash属性。这样就可以避免在数据库中保存明文密码了。
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    def __repr__(self):
        return '<Admin %r>' %self.name
    
@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))