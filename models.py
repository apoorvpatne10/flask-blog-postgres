from app import db
from datetime import datetime


class User(db.Model):
    # User model for storing user information
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    blogs = db.relationship("Blog", backref="user")


class Blog(db.Model):
    # Blog model for storing blog post information
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        # A representation of the Blog object for debugging purposes
        return f"BlogPost(id={self.id}, title={self.title})"
