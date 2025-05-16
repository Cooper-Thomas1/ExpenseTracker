from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from dotenv import dotenv_values
from flask_migrate import Migrate
import os

# Load environment variables from .env file
env = dotenv_values(".env")

# Initialize Flask app
app = Flask(__name__)

# use a database in memory if we're in a testing environment
testing_environment = env['SELENIUM_TESTING'] == 'True'
if testing_environment:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    print("Selenium testing database is in use.")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)

app.config['MAIL_SERVER'] = env['MAIL_SERVER']
app.config['MAIL_PORT'] = int(env['MAIL_PORT'])
app.config['MAIL_USE_TLS'] = env['MAIL_USE_TLS'] == 'True'
app.config['MAIL_USE_SSL'] = env['MAIL_USE_SSL'] == 'True'
app.config['MAIL_USERNAME'] = env['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = env['MAIL_PASSWORD']
mail = Mail(app)

app.config['UPLOAD_FOLDER'] = env['UPLOAD_FOLDER']

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# create an empty database if we're in a testing environment
if testing_environment:
    from ExpenseTracker import models
    with app.app_context():
        db.create_all()

from ExpenseTracker import routes

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
