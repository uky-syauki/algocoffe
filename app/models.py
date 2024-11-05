from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(168))    
    role = db.Column(db.String(12), default="user")
    alamat = db.Column(db.String(64))
    email = db.Column(db.String(64))
    telp = db.Column(db.String(15))
    def __repr__(self):
        return f'<Admin {self.username}'
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))
    

class Coffe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(42), index=True)
    harga = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    