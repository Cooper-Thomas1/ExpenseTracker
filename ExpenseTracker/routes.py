from flask import render_template, url_for, flash, redirect, jsonify, request
from ExpenseTracker import app, db, bcrypt, mail
from ExpenseTracker.forms import RegistrationForm, LoginForm, ManualExpenseForm, FileExpenseForm, ForgotPasswordForm, ResetPasswordForm, ShareForm
from ExpenseTracker.models import User, Expense, SharedExpense
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from dateutil.parser import parse
from flask_mail import Message
from werkzeug.utils import secure_filename
from datetime import date
import csv


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/dashboard")
@login_required
def dashboard():
    totalexpenses = Expense.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", totalexpenses=sum([totalexpense.amount for totalexpense in totalexpenses]))

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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, primary_saving_goal=form.primary_saving_goal.data)
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

BANK_HEADER_MAP = {
    'transaction date': 'date',
    'date': 'date',
    'amount': 'amount',
    'value': 'amount',
    'description': 'description',
    'details': 'description',
    'narration': 'description',
    'type': 'category',
    'category': 'category'
}

VALID_CATEGORIES = {'food', 'transport', 'entertainment', 'utilities', 'misc'}

def normalize_headers(header_row):
    return [BANK_HEADER_MAP.get(h.strip().lower(), h.strip().lower()) for h in header_row]

def process_expense_file(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            original_headers = next(reader)
            headers = normalize_headers(original_headers)
            DictReader = csv.DictReader(file, fieldnames=headers)

            skipped_rows = 0
            for idx, row in enumerate(DictReader, start=2):
                try:
                    if not row.get('date') or not row.get('amount'):
                        raise ValueError("Missing required fields.")

                    category = row.get('category', 'misc').strip().lower()
                    if category not in VALID_CATEGORIES:
                        category = 'misc'

                    expense = Expense(
                        date=parse(row['date'], dayfirst=True),
                        amount=float(row['amount']),
                        description=row.get('description', '').strip(),
                        category=category,
                        user_id=current_user.id
                    )
                    db.session.add(expense)
                except Exception as e:
                    skipped_rows += 1
                    flash(f"Skipped row {idx} due to error: {e}", 'warning')

                db.session.commit()

                if skipped_rows != 0:
                    flash(f"Processed with {skipped_rows} row(s) skipped.", "info")


    except Exception as e:
        flash(f'Error processing file: {e}', 'danger')

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    manual_form = ManualExpenseForm()
    file_form = FileExpenseForm()

    # Handle manual expense form submission
    if manual_form.validate_on_submit() and 'manual_submit' in request.form:
        expense = Expense(
            date=manual_form.date.data,
            category=manual_form.category.data,
            amount=manual_form.amount.data,
            description=manual_form.description.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))

    # Handle file upload form submission
    if file_form.validate_on_submit() and 'file_submit' in request.form:
        file = file_form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(f"{app.config['UPLOAD_FOLDER']}/{filename}")
            process_expense_file(f"{app.config['UPLOAD_FOLDER']}/{filename}")
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('No file selected!', 'danger')

    return render_template('upload.html', manual_form=manual_form, file_form=file_form)

@app.route("/share", methods=['GET', 'POST'])
@login_required
def share():
    form = ShareForm()
    if form.validate_on_submit():
        recipient = User.query.filter_by(username=form.username.data).first()
        if recipient == None:
            flash("No account with that username found.")
        elif recipient.id == current_user.id:
            flash("Cannot share expenses with yourself.")
        else:
            sharedExpense = SharedExpense(
                sender_id=current_user.id,
                recipient_id=recipient.id,
                start_date=form.start_date.data,
                end_date=form.end_date.data
            )
            db.session.add(sharedExpense)
            db.session.commit()
            flash("Successfully shared expenses.")
    
    shared_expenses = SharedExpense.query.filter_by(sender_id=current_user.id).all()
    formatted_expenses = []
    for shared_expense in shared_expenses:
        recipient_username = User.query.get(shared_expense.recipient_id).username
        formatted_expenses.append({"id": shared_expense.id,
                                   "username": recipient_username, 
                                   "start_date": shared_expense.start_date, 
                                   "end_date": shared_expense.end_date,
                                   "created_at": shared_expense.created_at
                                   })
    return render_template("share.html", form=form, shared_expenses=formatted_expenses)

@app.route("/shared-with-me", methods=['GET'])
@login_required
def shared_with_me():
    shared_expenses = SharedExpense.query.filter_by(recipient_id=current_user.id).all()

    formatted_expenses = []
    for shared_expense in shared_expenses:
        sender_username = User.query.get(shared_expense.sender_id).username
        expenses = Expense.query.filter(Expense.user_id == shared_expense.sender_id, 
                                        Expense.date >= shared_expense.start_date,
                                        Expense.date <= shared_expense.end_date).all()
        formatted_expenses.append({"username": sender_username, "expenses": expenses, "created_at": shared_expense.created_at})

    return render_template("shared-with-me.html", shared_expenses=formatted_expenses)

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
        {"date": expense.date.strftime('%Y-%m-%d'), "amount": expense.amount, "category": expense.category}
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

@app.route("/delete-shared-expense/<int:shared_expense_id>", methods=['POST'])
@login_required
def delete_shared_expense(shared_expense_id):
    shared_expense = SharedExpense.query.get_or_404(shared_expense_id)
    if shared_expense.sender_id != current_user.id:
        flash("You are not authorized to delete this shared expense.", "danger")
        return redirect(url_for('share'))
    db.session.delete(shared_expense)
    db.session.commit()
    flash("Shared expense deleted successfully!", "success")
    return redirect(url_for('share'))

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms-of-service.html')

