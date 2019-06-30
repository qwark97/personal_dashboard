from config import App
import datetime
from flask_login import UserMixin

db = App.db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    pictures = db.relationship('Picture', backref='owner', lazy=True)
    notes = db.relationship('Note', backref='owner', lazy=True)
    friends = db.relationship('Friend', backref='mate', lazy=True)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commitments = db.relationship('Commitment', backref='owns', lazy=True)
    receivables = db.relationship('Receivable', backref='owes', lazy=True)

class Commitment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'), nullable=False)

class Receivable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'), nullable=False)
    