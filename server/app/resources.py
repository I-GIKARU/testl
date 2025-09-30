# resources.py
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, jwt_required,
    get_jwt_identity, get_jwt,
    set_access_cookies, unset_jwt_cookies
)
from .models import db, Student, Client, Admin, get_user_by_email, get_user_by_id_and_role, get_user_model_by_role
from .utils import role_required, send_confirmation_email, send_password_reset_email, send_welcome_email

def get_current_user():
    """Helper function to get current user from JWT"""
    identity = get_jwt_identity()  # now just a string or int (user ID)
    claims = get_jwt()
    role = claims.get('role')

    if not identity:
        return None

    user_id = int(identity)

    # Use role from claims if available
    if role:
        return get_user_by_id_and_role(user_id, role)

    # Fallback: search all roles
    for role_name in ['student', 'client', 'admin']:
        user = get_user_by_id_and_role(user_id, role_name)
        if user:
            return user
    return None


class EmailConfirmation(Resource):
    def get(self, token):
        # Search for the token across all user tables
        user = None
        for model in [Student, Client, Admin]:
            user = model.query.filter_by(email_confirmation_token=token).first()
            if user:
                break
        
        if user and user.confirm_email(token):
            db.session.commit()
            
            # Send welcome email after successful verification
            try:
                send_welcome_email(user)
                print(f"Welcome email sent to {user.email}")
            except Exception as e:
                print(f"Error sending welcome email: {e}")
                # Don't fail the confirmation if welcome email fails
            
            return {'message': 'Email confirmed successfully! Welcome to our platform.'}, 200
        return {'message': 'Invalid or expired token'}, 400

class PasswordResetRequest(Resource):
    def post(self):
        data = request.get_json()
        user, role = get_user_by_email(data['email'])
        if not user:
            return {'message': 'User not found'}, 404
        token = user.generate_password_reset_token()
        db.session.commit()
        send_password_reset_email(user, token)
        return {'message': 'Password reset email sent'}, 200

class PasswordReset(Resource):
    def post(self, token):
        data = request.get_json()
        
        # Search for the token across all user tables
        user = None
        for model in [Student, Client, Admin]:
            user = model.query.filter_by(password_reset_token=token).first()
            if user:
                break
        
        if user and user.reset_password(token, data['new_password']):
            db.session.commit()
            return {'message': 'Password reset successfully'}, 200
        return {'message': 'Invalid or expired token'}, 400

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        
        # Check if email already exists across all user tables
        existing_user, _ = get_user_by_email(data['email'])
        if existing_user:
            return {'message': 'Email already exists'}, 400
        
        # Get the role and corresponding model
        role = data.get('role', 'student')  # Default to student
        user_model = get_user_model_by_role(role)
        
        if not user_model:
            return {'message': 'Invalid role'}, 400
        
        # Create user with the appropriate model
        user = user_model(
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])
        token = user.generate_email_confirmation_token()
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user, token)

        return {'message': 'User created successfully, please confirm your email'}, 201


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user, role = get_user_by_email(data['email'])

        if not user:
            return {'message': 'Invalid credentials'}, 401

        if not user.email_confirmed:
            return {'message': 'Email not confirmed, please check your email'}, 403

        if not user.check_password(data['password']):
            return {'message': 'Invalid credentials'}, 401

        # Create JWT token with user identity including role
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'name': user.name,
                'email': user.email,
                'role': role
            }
        )

        # Create response and set cookies
        resp = jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': role
            }
        })

        set_access_cookies(resp, access_token)
        return resp


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        resp = jsonify({'message': 'Successfully logged out'})
        unset_jwt_cookies(resp)
        return resp


class AuthMe(Resource):
    @jwt_required()
    def get(self):
        """Get current user information from JWT token"""
        current_user = get_current_user()
        if not current_user:
            return {'message': 'User not found'}, 404

        claims = get_jwt()
        role = claims.get('role')

        return {
            'user': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email,
                'role': role
            }
        }, 200

class Dashboard(Resource):
    @jwt_required()
    def get(self):
        current_user = get_current_user()
        if not current_user:
            return {'message': 'User not found'}, 404
        return {'message': f'Welcome {current_user.name} (User)'}, 200


class AdminDashboard(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        current_user = get_current_user()
        if not current_user:
            return {'message': 'User not found'}, 404
        return {'message': f'Welcome Admin {current_user.name}'}, 200


class ClientDashboard(Resource):
    @jwt_required()
    @role_required('client')
    def get(self):
        current_user = get_current_user()
        if not current_user:
            return {'message': 'User not found'}, 404
        return {'message': f'Welcome Client {current_user.name}'}, 200


class StudentDashboard(Resource):
    @jwt_required()
    @role_required('student')
    def get(self):
        current_user = get_current_user()
        if not current_user:
            return {'message': 'User not found'}, 404
        return {'message': f'Welcome Student {current_user.name}'}, 200
