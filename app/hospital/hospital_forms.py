from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import Users


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('sign in')


class RegistrationForm(FlaskForm):
    """registration form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('register')


    def validate_email(self, email):
        """to make sure email is unique before storing in database"""
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email')