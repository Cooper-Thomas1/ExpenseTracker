from flask import render_template
from ExpenseTracker import app

# Mock current_user for now
current_user = {"username": "ABC_123"}  # Replace with actual user logic later

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", current_user=current_user)