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

## Application Features

### Introductory View
- Landing page with an overview of the app
- Register/Login to access personalized tracking

### Upload Data View
- Users can upload expense files (CSV/JSON) or manually input expenses
- Data categories include: food, transport, bills, subscriptions, etc.

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
- **Visualization:** Chart.js or Plotly.js for graphs and pie charts

## Directory Structure
```
expense_tracker/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── home.html
│   ├── login.html
│   ├── share.html
│   ├── upload.html
│   ├── visualise.html
│
├── static/
│   └── styles.css
│
├── venv/
└── ...
```

