# app/models.py
from .extensions import db
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
import secrets


class BaseUserMixin:
    """Base mixin class for common user functionality"""
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, role):
        return create_access_token(
            identity=str(self.id),
            additional_claims={
                'name': self.name,
                'email': self.email,
                'role': role
            }
        )

    def generate_email_confirmation_token(self):
        """Generate a token for email confirmation"""
        self.email_confirmation_token = secrets.token_urlsafe(32)
        self.email_confirmation_token_expires = datetime.utcnow() + timedelta(hours=24)
        return self.email_confirmation_token
    
    def confirm_email(self, token):
        """Confirm email with token"""
        if (self.email_confirmation_token == token and 
            self.email_confirmation_token_expires > datetime.utcnow()):
            self.email_confirmed = True
            self.email_confirmation_token = None
            self.email_confirmation_token_expires = None
            return True
        return False
    
    def generate_password_reset_token(self):
        """Generate a token for password reset"""
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return self.password_reset_token
    
    def reset_password(self, token, new_password):
        """Reset password with token"""
        if (self.password_reset_token == token and 
            self.password_reset_token_expires > datetime.utcnow()):
            self.set_password(new_password)
            self.password_reset_token = None
            self.password_reset_token_expires = None
            return True
        return False


class Student(db.Model, BaseUserMixin):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Email confirmation fields
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_token = db.Column(db.String(100), unique=True)
    email_confirmation_token_expires = db.Column(db.DateTime)
    
    # Password reset fields
    password_reset_token = db.Column(db.String(100), unique=True)
    password_reset_token_expires = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_token(self):
        return super().get_token('student')


class Client(db.Model, BaseUserMixin):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Email confirmation fields
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_token = db.Column(db.String(100), unique=True)
    email_confirmation_token_expires = db.Column(db.DateTime)
    
    # Password reset fields
    password_reset_token = db.Column(db.String(100), unique=True)
    password_reset_token_expires = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_token(self):
        return super().get_token('client')


class Admin(db.Model, BaseUserMixin):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Email confirmation fields
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_token = db.Column(db.String(100), unique=True)
    email_confirmation_token_expires = db.Column(db.DateTime)
    
    # Password reset fields
    password_reset_token = db.Column(db.String(100), unique=True)
    password_reset_token_expires = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_token(self):
        return super().get_token('admin')


# Helper function to get user by email across all tables
def get_user_by_email(email):
    """Get user by email from any of the user tables"""
    student = Student.query.filter_by(email=email).first()
    if student:
        return student, 'student'
    
    client = Client.query.filter_by(email=email).first()
    if client:
        return client, 'client'
    
    admin = Admin.query.filter_by(email=email).first()
    if admin:
        return admin, 'admin'
    
    return None, None


# Helper function to get user by ID and role
def get_user_by_id_and_role(user_id, role):
    """Get user by ID and role"""
    if role == 'student':
        return Student.query.get(user_id)
    elif role == 'client':
        return Client.query.get(user_id)
    elif role == 'admin':
        return Admin.query.get(user_id)
    return None


# Helper function to get user model by role
def get_user_model_by_role(role):
    """Get the appropriate user model class by role"""
    models = {
        'student': Student,
        'client': Client,
        'admin': Admin
    }
    return models.get(role)
