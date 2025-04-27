from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ExpenseTracker.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

class ManualExpenseForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    category = StringField('Category', validators=[DataRequired(), Length(max=50)])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Add Expense')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No account found with that email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()], render_kw={"placeholder": "New Password"})
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Reset Password')