from flask import Flask

# Initialize Flask app
website = Flask(__name__)

from ExpenseTracker import routes

# Run the app
if __name__ == "__main__":
    website.run(debug=True)
