from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, FloatField, DateField, SubmitField, DecimalField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ExpenseTracker.models import User
from datetime import date

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
    category = SelectField('Category', 
                            choices=[
                                ('food', 'Food'),
                                ('transport', 'Transport'),
                                ('entertainment', 'Entertainment'),
                                ('utilities', 'Utilities'),
                                ('misc', 'Miscellaneous')
                            ], 
                            validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Add Expense')

    def validate_date(self, date_field):
        if date_field.data > date.today():
            flash('The date cannot be in the future.', 'danger')
            raise ValidationError('The date cannot be in the future.')

class FileExpenseForm(FlaskForm):
    file = FileField('Expense File', validators=[DataRequired()])
    submit = SubmitField('Upload')

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

class ShareForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"placeholder": "Start Date"})
    end_date = DateField('End Date', validators=[DataRequired(), ], format='%Y-%m-%d', render_kw={"placeholder": "End Date"})
    submit = SubmitField('Submit')
