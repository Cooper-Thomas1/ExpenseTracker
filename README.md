## Agile Web Development Group 41's Project

# Expense Tracker & Analysis Web Application

## Purpose and Overview

This application is a secure and user-friendly **expense tracking and analytics platform**. Users can upload or enter expense data, receive automated analysis and insights, and selectively share their financial summaries with others (e.g., a partner, financial advisor, or accountability buddy).

The goal is to make budgeting more engaging, effective, and intuitive through rich data visualization and collaborative features.

---

## Group Members

| UWA ID     | Name              | GitHub Username    |
|------------|-------------------|--------------------|
| 23723986   | Cooper Thomas     | Cooper-Thomas1     |
| 23964287   | Houssein Marouff  | Big-H-21           |
| 23487767   | Luke Waters       | LJW-Dev            |
| 23777359   | Sans Biticon      | Sans936            |

---

## Install guide

1. **Download or Clone**  
   - Download the latest release or clone the repository and open a terminal in the project’s root directory.

2. **(Recommended) Create a Virtual Environment**  
   Use a virtual environment to manage dependencies:  
   [Python venv documentation](https://docs.python.org/3/library/venv.html).  
   - **Windows**  
        ```
        python -m venv venv
        venv\Scripts\activate
        ```
   
   - **MacOS/Linux**  
        ```
        python -m venv venv
        source venv/bin/activate
        ```

3. **Install Dependencies**  
        ```
        python -m pip install -r requirements.txt
        ```

4. **Run the Flask Project**  
        ```
        flask run
        ```

5. **Access the Website**  
   Open your browser and visit:  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Application Features

### Introductory View
- Landing page with an overview of the app
- Register/Login to access personalised tracking

### Upload Data View
- Users can upload expense files (CSV/JSON) or manually input expenses
- Data categories include: food, transport, bills, misc, etc.

### Visualise Data View
- Interactive charts and graphs showing:
  - Spending over time
  - Category breakdowns
  - Budget vs. actual
  - Trends and anomalies
- Users can view both their own data and shared datasets

### Share Data View
- Share monthly summaries or custom reports
- Granular permission control over what’s shared and with whom

---

## Tech Stack

- **Backend:** Python, Flask, Flask-WTF, Flask-Login, SQLAlchemy, SQLite
- **Frontend:** HTML5, CSS, JavaScript, Bootstrap, jQuery, AJAX
- **Data Analysis:** Pandas, NumPy
- **Visualisation:** Chart.js or Plotly.js for graphs and pie charts

---

## Running Tests

1. **Update Environment Variables**  
   In your `.env` or `.flaskenv` file, add the line `SELENIUM_TESTING=True`. This will make ExpenseTracker use a clean database to test with.

2. **Start the Flask Server**  
   In a terminal, start ExpenseTracker with the command `flask run`.

3. **Run the Tests**  
   In a different terminal to step 2, run the tests using the command `pytest`.

To switch back to the default database, set `SELENIUM_TESTING=False` and restart the flask server.

## Directory Structure
```
expense_tracker/
│   .flaskenv
│   .gitignore
│   README.md
│   requirements.txt
│
├───ExpenseTracker
│   │   forms.py
│   │   models.py
│   │   routes.py
│   │   __init__.py
│   │
│   ├───api
│   │       expenses.py
│   │
│   ├───static
│   │       dashboard.css
│   │       dashboard.js
│   │       forgot-password.css
│   │       login.css
│   │       register.css
│   │       reset-password.css
│   │       styles.css
│   │
│   └───templates
│           base.html
│           dashboard.html
│           expense-history.html
│           forgot-password.html
│           home.html
│           login.html
│           privacy-policy.html
│           register.html
│           reset-password.html
│           share.html
│           shared-with-me.html
│           terms-of-service.html
│           upload.html
│           visualise.html
│
├───instance
│       site.db
│
├───migrations
│   │   alembic.ini
│   │   env.py
│   │   README
│   │   script.py.mako
│   │
│   └───versions
│           0038c57a8a69_add_profile_picture_to_user.py
│           6dee1339c39e_add_created_at_to_sharedexpense.py
│           ea28269e63b5_remove_profile_picture_and_add_primary_.py
│
├───tests
│       test_forms.py
│       test_selenium.py
│       __init__.py
│
└───uploads
        test1.csv
```

