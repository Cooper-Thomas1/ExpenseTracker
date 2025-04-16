from ExpenseTracker import website
from flask import render_template

@website.route("/")
@website.route("/home")
def home():
    return render_template("home.html")

@website.route("/login")
def login():
    return render_template("login.html")

@website.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")