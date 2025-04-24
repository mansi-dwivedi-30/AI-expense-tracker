from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from app import db
from app.models import Expense
from app.forms import ExpenseForm
from flask import flash 
from datetime import datetime
from app.gemini_utils import get_expense_insights


expenses_bp = Blueprint('expenses', __name__)
@expenses_bp.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    total_amount = sum(exp.amount for exp in expenses)

    total_expenses = sum(e.amount for e in expenses)
    max_expense = max((e.amount for e in expenses), default=0)
    total_income = 70000
    category_summary_dict = {}
    for exp in expenses:
        category_summary_dict[exp.category] = category_summary_dict.get(exp.category, 0) + exp.amount

    # Convert to list of tuples so Jinja can use map safely
    category_summary = list(category_summary_dict.items())

    expenses_data = [
        {"date": e.date.strftime("%Y-%m-%d"), "category": e.category, "amount": e.amount}
        for e in expenses
    ]
    insights = get_expense_insights(expenses_data)
    

    return render_template('dashboard.html',
                           expenses=expenses,
                           insights=insights,
                           total_amount=total_amount,
                           category_summary=category_summary,
                           max_expense=max_expense,
                           total_income=total_income,
                           total_expenses=total_expenses,
                           savings = current_user.income - total_expenses if current_user.income else None)
@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            title=form.description.data,
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.dashboard'))

    return render_template('add_expense.html', form=form)

@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for('expenses.dashboard'))
    
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('expenses.dashboard'))

@expenses_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Unauthorized!", "danger")
        return redirect(url_for('expenses.dashboard'))

    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']

        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('expenses.dashboard'))

    return render_template('edit_expense.html', expense=expense)


@expenses_bp.route('/react/<int:expense_id>', methods=['POST'])
@login_required
def react_to_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash("Not allowed!", "danger")
        return redirect(url_for('expenses.dashboard'))

    emoji = request.form.get('emoji')
    if emoji:
        expense.reaction = emoji
        db.session.commit()
        flash("Reacted!", "success")

    return redirect(url_for('expenses.dashboard'))

@expenses_bp.route('/dev/reset-expenses')
@login_required
def reset_expenses():
    # WARNING: Only use this route in development!
    Expense.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    # Sample valid entries
    sample_expenses = [
        Expense(user_id=current_user.id, amount=100.0, category='Food', description='Lunch at cafe', date=datetime(2024, 5, 1)),
        Expense(user_id=current_user.id, amount=50.0, category='Transport', description='Taxi fare', date=datetime(2024, 5, 2)),
        Expense(user_id=current_user.id, amount=150.0, category='Groceries', description='Weekly groceries', date=datetime(2024, 5, 3)),
    ]

    db.session.add_all(sample_expenses)
    db.session.commit()

    flash("Expenses reset and test data loaded!", "success")
    return redirect(url_for('dashboard'))

