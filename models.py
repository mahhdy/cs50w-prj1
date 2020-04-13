import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120),  nullable=True)
    def __repr__(self):
        return '<User %r>' % self.username
class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id=db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    add_time=db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    comment=db.Column(db.Text, nullable=False)
    def __repr__(self):
        return '<Comment %r>' % self.comment[:20]
class Book(db.Model):
    __tablename__='books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(80), unique=True, nullable=False)
    title=db.Column(db.Text, nullable=False)
    author=db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Book %r>' % self.title[:25]    