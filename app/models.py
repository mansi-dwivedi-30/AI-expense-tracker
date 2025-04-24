from datetime import datetime
from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    expenses = db.relationship('Expense', backref='user', lazy=True)
    income = db.Column(db.Float, nullable=True)    

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ correct
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reaction = db.Column(db.String(10)) 

