from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, IntegerField, BooleanField, RadioField, validators, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length

#
class ObjectListForm(FlaskForm):
    name = StringField('Наименование *', validators=[DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('Submit')
    # description = TextAreaField('Course Description',
    #                             validators=[InputRequired(),
    #                                         Length(max=200)])
    # price = IntegerField('Price', validators=[InputRequired()])
    # level = RadioField('Level',
    #                    choices=['Beginner', 'Intermediate', 'Advanced'],
    #                    validators=[InputRequired()])
    # available = BooleanField('Available', default='checked')
#
#
# class ObjectListForm(Form):
#     name = StringField('name', [validators.Length(min=4, max=25)])
    # email = StringField('Email Address', [validators.Length(min=6, max=35)])
    # password = PasswordField('New Password', [
    #     validators.DataRequired(),
    #     validators.EqualTo('confirm', message='Passwords must match')
    # ])
    # confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])