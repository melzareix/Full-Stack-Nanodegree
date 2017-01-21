from flask_sqlalchemy import SQLAlchemy
import flask
from oauth2client import client

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    items = db.relationship('Item', backref='category')
    user_id = db.Column(db.String, db.ForeignKey('users.id'))


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cat_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.String, db.ForeignKey('users.id'))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    categories = db.relationship('Category', backref='user')
    items = db.relationship('Item', backref='user')
