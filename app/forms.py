from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
import sqlalchemy as sa
from app import db
from app.models import Users


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    minecraft_username = StringField('Minecraft Username (Optional)', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                                                             EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(
            Users.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
