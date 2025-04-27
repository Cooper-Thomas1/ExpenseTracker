from flask import render_template, url_for, flash, redirect, jsonify
from ExpenseTracker import app, db, bcrypt, mail
from ExpenseTracker.forms import RegistrationForm, LoginForm, ManualExpenseForm, ForgotPasswordForm, ResetPasswordForm, ShareForm
from ExpenseTracker.models import User, Expense
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from flask_mail import Message

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

@app.route("/forgot-password", methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('No account found with that email.', 'info')
    return render_template("forgot-password.html", form=form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@expensetracker.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset-password.html', form=form)

@app.route("/expense-history")
@login_required
def expense_history():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template("expense-history.html", expenses=expenses)

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
@login_required
def share():
    form = ShareForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
    return render_template("share.html", form=form)

@app.route("/visualise")
@login_required
def visualise():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    total_spent = sum(expense.amount for expense in expenses)
    months = len(set(expense.date.strftime('%Y-%m') for expense in expenses))
    avg_monthly_spend = total_spent / months if months > 0 else 0

    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
    most_spent_category = max(category_totals, key=category_totals.get) if category_totals else "N/A"

    current_month = datetime.now().strftime('%Y-%m')
    last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime('%Y-%m')
    current_month_total = sum(expense.amount for expense in expenses if expense.date.strftime('%Y-%m') == current_month)
    last_month_total = sum(expense.amount for expense in expenses if expense.date.strftime('%Y-%m') == last_month)
    difference = current_month_total - last_month_total

    return render_template('visualise.html', 
                           avg_monthly_spend=avg_monthly_spend, 
                           most_spent_category=most_spent_category, 
                           difference=difference)

@app.route("/api/expenses")
@login_required
def api_expenses():
    expenses = [
        {"date": expense.date.strftime('%Y-%m-%d'), "amount": expense.amount}
        for expense in current_user.expenses
    ]
    return jsonify(expenses)

@app.route("/delete-expense/<int:expense_id>", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("You are not authorized to delete this expense.", "danger")
        return redirect(url_for('expense_history'))
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('expense_history'))

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')

