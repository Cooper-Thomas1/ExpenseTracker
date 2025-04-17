from flask import Flask

# Initialize Flask app
app = Flask(__name__)

from ExpenseTracker import routes

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
