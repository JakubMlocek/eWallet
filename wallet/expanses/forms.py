from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, DateField, TextAreaField
from wtforms.validators import DataRequired

class ExpanseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')