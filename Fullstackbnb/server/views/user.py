from flask import Blueprint, request, jsonify
from models import db, User, Booking, Favorites, Review, Listing
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

# --- Helpers ---
def is_admin(user):
    return user and user.role == 'admin'

def is_host(user):
    return user and user.role == 'host'

def is_guest(user):
    return user and user.role == 'guest'

def is_self_or_admin(current_user, target_user_id):
    return current_user and (current_user.id == target_user_id or is_admin(current_user))

# --- Routes ---

# Create user
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'guest')

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": "New user created successfully!"}), 201

# Get current user
@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# Get any user
@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    if not is_self_or_admin(current_user, user_id):
        return jsonify({"error": "Unauthorized access"}), 403
    return jsonify(target_user.to_dict()), 200

# Update user
@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
@jwt_required()
def update_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({"error": "User not found"}), 404
    if not is_self_or_admin(current_user, user_id):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    if 'username' in data:
        target_user.username = data['username']
    if 'email' in data:
        target_user.email = data['email']
    if 'password' in data:
        target_user.password = generate_password_hash(data['password'])
    if 'role' in data and is_admin(current_user):
        target_user.role = data['role']

    db.session.commit()
    return jsonify({"success": "User updated successfully"}), 200

# Delete user
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not is_self_or_admin(current_user, user_id):
        return jsonify({"error": "Unauthorized"}), 403

    Booking.query.filter_by(user_id=user.id).delete()
    Favorites.query.filter_by(user_id=user.id).delete()
    Review.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "User deleted successfully!"})

# Admin: Get all users
@user_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    current_user = User.query.get(get_jwt_identity())
    if not is_admin(current_user):
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Book listing
@user_bp.route('/users/bookings/<int:listing_id>', methods=['POST'])
@jwt_required()
def book_listing_for_user(listing_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if is_host(user):
        return jsonify({'error': 'Hosts are not allowed to book listings'}), 403

    data = request.get_json()
    check_in = data.get('check_in')
    check_out = data.get('check_out')

    if not check_in or not check_out:
        return jsonify({'error': 'Check-in and check-out dates are required'}), 400

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if check_out_date <= check_in_date:
        return jsonify({'error': 'Check-out must be after check-in'}), 400

    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    overlapping = Booking.query.filter(
        Booking.listing_id == listing_id,
        Booking.check_out > check_in_date,
        Booking.check_in < check_out_date
    ).first()
    if overlapping:
        return jsonify({'error': 'Listing is not available for the selected dates'}), 400

    nights = (check_out_date - check_in_date).days
    total_price = listing.price_per_night * nights

    booking = Booking(
        user_id=user_id,
        listing_id=listing_id,
        check_in=check_in_date,
        check_out=check_out_date,
        total_price=total_price
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        'message': 'Booking successful',
        'booking': booking.to_dict()
    }), 201
