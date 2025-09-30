from functools import wraps
from flask_jwt_extended import verify_jwt_in_request,  get_jwt
from flask import jsonify, current_app
from flask_mail import Message
from .extensions import mail

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')

            if not user_role:
                return jsonify(message='User role not found in token'), 401

            if user_role != required_role:
                return jsonify(message=f'{required_role} role required!'), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
def send_email(subject, recipients, text_body, html_body=None):
    msg = Message(subject=subject, recipients=recipients, body=text_body, html=html_body)
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_confirmation_email(user, token):
    subject = "🚀 Welcome to Moringa Innovation Marketplace - Confirm Your Email"
    confirmation_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/auth/confirm-email/{token}"

    text_body = f"""Hi {user.name}!

Welcome to the Moringa School Innovation Marketplace!

To confirm your email, click this link: {confirmation_url}

This link will expire in 24 hours.

The Moringa Innovation Team"""

    html_body = f"""
    <div style="font-family: Arial; max-width: 600px; padding: 20px;">
        <h2 style="color: #764ba2;">🚀 Confirm Your Email</h2>
        <p>Hi {user.name},</p>
        <p>Welcome to the Moringa Innovation Marketplace! Please confirm your email:</p>
        <a href="{confirmation_url}" style="background:#764ba2; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Confirm Email</a>
        <p>This link will expire in 24 hours.</p>
        <p>- The Moringa Team</p>
    </div>
    """
    return send_email(subject, [user.email], text_body, html_body)

def send_password_reset_email(user, token):
    subject = "🔐 Moringa Marketplace - Password Reset Request"
    reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/auth/reset-password/{token}"

    text_body = f"""Hi {user.name},

We received a request to reset your password.

Reset here: {reset_url}

This link expires in 1 hour.

Ignore this if you didn’t request it."""

    html_body = f"""
    <div style="font-family: Arial; max-width: 600px; padding: 20px;">
        <h2 style="color: #ee5a24;">🔐 Reset Your Password</h2>
        <p>Hi {user.name},</p>
        <p>Click the button below to reset your password:</p>
        <a href="{reset_url}" style="background:#ee5a24; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Reset Password</a>
        <p>This link expires in 1 hour.</p>
        <p>- The Moringa Team</p>
    </div>
    """
    return send_email(subject, [user.email], text_body, html_body)

def send_welcome_email(user):
    subject = "🎉 Welcome to Moringa Innovation Marketplace!"
    dashboard_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/dashboard"

    text_body = f"""Hi {user.name}!

Your email is confirmed. Welcome to the Moringa Innovation Marketplace.

Dashboard: {dashboard_url}

Let’s build the future together!

The Moringa Team"""

    html_body = f"""
    <div style="font-family: Arial; max-width: 600px; padding: 20px;">
        <h2 style="color: #10ac84;">🎉 Welcome, {user.name}!</h2>
        <p>Your email has been confirmed. You can now access your dashboard:</p>
        <a href="{dashboard_url}" style="background:#10ac84; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Go to Dashboard</a>
        <p>We're excited to have you join our community!</p>
        <p>- The Moringa Team</p>
    </div>
    """
    return send_email(subject, [user.email], text_body, html_body)
