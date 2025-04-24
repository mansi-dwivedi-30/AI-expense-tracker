from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Bills', 'Bills'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=200)])
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Add Expense')
