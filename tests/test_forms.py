import pytest
from flask import Flask
from flask_wtf import FlaskForm
from ExpenseTracker.models import User
from ExpenseTracker import db
from ExpenseTracker.forms import (
    RegistrationForm, LoginForm, ManualExpenseForm,
    ForgotPasswordForm, ResetPasswordForm, ShareForm
)

# Fixtures
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF in tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.secret_key = 'testsecret'
    db.init_app(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

# -------- Registration Form --------
def test_registration_form_valid(app, init_db):
    with app.test_request_context():
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'primary_saving_goal': 'new car'
        }
        form = RegistrationForm(data=form_data)
        assert form.validate()

def test_registration_form_username_taken(app, init_db):
    with app.app_context():
        user = User(username='existinguser', email='existing@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
    with app.test_request_context():
        form_data = {
            'username': 'existinguser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'primary_saving_goal': 'new car'
        }
        form = RegistrationForm(data=form_data)
        assert not form.validate()
        assert 'That username is already taken.' in form.errors.get('username', [])

def test_registration_form_email_taken(app, init_db):
    with app.app_context():
        user = User(username='testuser', email='existing@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
    with app.test_request_context():
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'primary_saving_goal': 'new car'
        }
        form = RegistrationForm(data=form_data)
        assert not form.validate()
        assert 'That email is already registered.' in form.errors.get('email', [])

# -------- Login Form --------
def test_login_form_valid(app, init_db):
    with app.app_context():
        user = User(username='testuser', email='testuser@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
    with app.test_request_context():
        form_data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        assert form.validate()

def test_login_form_invalid_email(app):
    with app.test_request_context():
        form_data = {
            'email': 'invalid@example',
            'password': 'password123'
        }
        form = LoginForm(data=form_data)
        assert not form.validate()

# -------- ManualExpenseForm --------
def test_manual_expense_form_valid(app):
    with app.test_request_context():
        form_data = {
            'date': '2025-05-01',
            'category': 'food',
            'amount': 10.5,
            'description': 'Lunch'
        }
        form = ManualExpenseForm(data=form_data)
        assert form.validate()

def test_manual_expense_form_invalid_date(app):
    with app.test_request_context():
        form_data = {
            'date': '2099-01-01',  # future date
            'category': 'food',
            'amount': 10.5,
            'description': 'Lunch'
        }
        form = ManualExpenseForm(data=form_data)
        assert not form.validate()
        assert 'The date cannot be in the future.' in form.errors.get('date', [])

def test_manual_expense_form_invalid_description(app):
    with app.test_request_context():
        form_data = {
            'date': '2025-05-01',
            'category': 'invalid',
            'amount': 10.5,
            'description': 't' * 201 # string of 201 't's
        }
        form = ManualExpenseForm(data=form_data)
        assert not form.validate()

# -------- ForgotPasswordForm --------
def test_forgot_password_form_valid(app, init_db):
    with app.app_context():
        user = User(username='testuser', email='testuser@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
    with app.test_request_context():
        form_data = {'email': 'testuser@example.com'}
        form = ForgotPasswordForm(data=form_data)
        assert form.validate()

def test_forgot_password_form_invalid_email(app, init_db):
    with app.test_request_context():
        form_data = {'email': 'nonexistent@example.com'}
        form = ForgotPasswordForm(data=form_data)
        assert not form.validate()
        assert 'No account found with that email.' in form.errors.get('email', [])

# -------- ResetPasswordForm --------
def test_reset_password_form_valid(app):
    with app.test_request_context():
        form_data = {
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }
        form = ResetPasswordForm(data=form_data)
        assert form.validate()

def test_reset_password_form_mismatch(app):
    with app.test_request_context():
        form_data = {
            'password': 'newpassword123',
            'confirm_password': 'otherpassword'
        }
        form = ResetPasswordForm(data=form_data)
        assert not form.validate()
        assert 'Field must be equal to password.' in form.errors.get('confirm_password', [])


# -------- ShareForm --------
def test_share_form_valid(app):
    with app.test_request_context():
        form_data = {
            'username': 'testUser',
            'start_date': '2025-01-12',
            'end_date': '2025-04-25'
        }
        form = ShareForm(data=form_data)
        assert form.validate()

def test_share_form_invalid_username(app):
    with app.test_request_context():
        form_data = {
            'username': '123456789123456789123',
            'start_date': '2025-01-12',
            'end_date': '2025-04-25'
        }
        form = ShareForm(data=form_data)
        assert not form.validate()

def test_share_form_invalid_date(app):
    with app.test_request_context():
        form_data = {
            'username': 'testUser',
            'start_date': '2025-01-12',
            'end_date': ''
        }
        form = ShareForm(data=form_data)
        assert not form.validate()