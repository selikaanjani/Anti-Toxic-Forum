from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        InputRequired(), Email(), Length(min=2, max=255)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=255)])


class SignUpForm(FlaskForm):
    name = StringField('Full name', validators=[
                       InputRequired(), Length(min=2, max=255)])
    email = StringField('Email', validators=[
                        InputRequired(), Email(), Length(min=2, max=255)])
    password = PasswordField('Password', validators=[
                             InputRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirm password', validators=[InputRequired()])
