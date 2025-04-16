from ExpenseTracker import website
from flask import render_template

@website.route("/")
def index():
    return render_template("home.html")