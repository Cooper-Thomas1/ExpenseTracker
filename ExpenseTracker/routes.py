from flask import render_template
from ExpenseTracker import app

# Mock current_user for now
current_user = {"username": "ABC_123"}  # Replace with actual user logic later

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", current_user=current_user)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")

@app.route("/share")
def share():
    return render_template("share.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/visualise")
def visualize():
    return render_template("visualise.html")

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')

