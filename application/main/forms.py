from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    # StringField和SubmitField是Flask-WTF中的类，用于生成HTML表单元素
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your Password', validators=[DataRequired()])
    submit = SubmitField('Submit')