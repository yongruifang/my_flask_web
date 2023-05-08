from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class PredictForm(FlaskForm):
    morning_stocks = StringField('morning_stocks', validators=[DataRequired()])
    afternoon_stocks = StringField('afternoon_stocks', validators=[DataRequired()])
    submit = SubmitField('save')
