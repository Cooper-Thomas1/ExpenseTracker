from flask import render_template, url_for, flash, redirect, jsonify
from ExpenseTracker import app, db, bcrypt
from ExpenseTracker.forms import RegistrationForm, LoginForm, ManualExpenseForm
from ExpenseTracker.models import User, Expense
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot-password.html")

@app.route("/expense-history")
@login_required
def expense_history():
    return render_template("expense-history.html")

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = ManualExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            date=form.date.data,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('upload.html', manual_form=form)

@app.route("/share")
def share():
    return render_template("share.html")

@app.route("/visualise")
@login_required
def visualise():
    return render_template("visualise.html")

@app.route("/api/expenses")
@login_required
def api_expenses():
    expenses = [
        {"date": expense.date.strftime('%Y-%m-%d'), "amount": expense.amount}
        for expense in current_user.expenses
    ]
    return jsonify(expenses)

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')

