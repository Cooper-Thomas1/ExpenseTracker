from flask import render_template
from flask import Flask

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
