from . import db

class Admin(db.Model):
    __tablename__ = 'admin'
    name = db.Column(db.String(64),primary_key = True)
    password = db.Column(db.String(64),unique=False)
    id = db.Column(db.Integer,unique=True)

    def __repr__(self):
        return '<Admin %r>' %self.name