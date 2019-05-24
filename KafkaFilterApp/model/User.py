from KafkaFilterApp import db, bcrypt
import jwt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, username,email,password):
        self.username=username
        self.email=email
        self.hash_password(password)
        print(self.username,self.email,self.password)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return unicode(self.id)


    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

