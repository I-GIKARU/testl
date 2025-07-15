# app/__init__.py
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .extensions import db, mail
from .resources import (
    UserRegistration, UserLogin, UserLogout,
    Dashboard, AdminDashboard, ClientDashboard, StudentDashboard,
    EmailConfirmation, PasswordResetRequest, PasswordReset, AuthMe
)
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)
    api = Api(app)
    CORS(app, 
         supports_credentials=True,
         origins=['http://localhost:3000'],  # Specific origin for credentials
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    # API Routes (JSON)
    api.add_resource(UserRegistration, '/api/register')
    api.add_resource(UserLogin, '/api/login')
    api.add_resource(UserLogout, '/api/logout')
    api.add_resource(Dashboard, '/api/dashboard')
    api.add_resource(AdminDashboard, '/api/admin')
    api.add_resource(ClientDashboard, '/api/client')
    api.add_resource(StudentDashboard, '/api/student')
    api.add_resource(EmailConfirmation, '/api/confirm/<token>')
    api.add_resource(AuthMe, '/api/auth/me')
    api.add_resource(PasswordResetRequest, '/api/password-reset-request')
    api.add_resource(PasswordReset, '/api/password-reset/<token>')

    return app
