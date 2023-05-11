from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from ..models import Admin

class LoginForm(FlaskForm):
    # StringField和SubmitField是Flask-WTF中的类，用于生成HTML表单元素
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
    Email()])
    name = StringField('name', validators=[
                        DataRequired(), Length(1, 64),
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                        'Usernames must have only letters, numbers, dots or '
                        'underscores')])
    password = PasswordField('Password', validators=[
                        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_name(self, field):
        if Admin.query.filter_by(name=field.data).first():
            raise ValidationError('name already in use.')