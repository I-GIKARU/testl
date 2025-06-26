# views/admin.py
from flask import Blueprint, jsonify, request
from models import db, User, Listing, Booking, Favorites, Review
from flask_jwt_extended import jwt_required, get_jwt_identity
admin_blueprint = Blueprint('admin', __name__)


def require_admin_role(identity=None):
    if identity is None:
        identity = get_jwt_identity()
    user = User.query.get(identity)
    if not user or user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    return user
# ==========Get all users==========
@admin_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "role": user.role
        } for user in users
    ]), 200

# ==========Get all listings==========
@admin_blueprint.route('/listings', methods=['GET'])
@jwt_required()
def get_all_listings():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    listings = Listing.query.all()
    return jsonify([listing.to_dict() for listing in listings]), 200


# ==========Delete a listing by id==========
@admin_blueprint.route('/listings/<int:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({"error": "Listing not found"}), 404

    Booking.query.filter_by(listing_id=listing_id).delete()
    Favorites.query.filter_by(listing_id=listing_id).delete()
    Review.query.filter_by(listing_id=listing_id).delete()
    db.session.delete(listing)
    db.session.commit()
    return jsonify({"success": "Listing deleted successfully"}), 200

# ==========Get analytics==========
@admin_blueprint.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    current_user = get_jwt_identity()
    current_user = User.query.get(current_user)
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(
        db.func.sum(Booking.total_price)).scalar() or 0
    popular_locations = db.session.query(
        Listing.location,
        db.func.count(Booking.id).label('booking_count')
    ).join(Booking, Booking.listing_id == Listing.id).group_by(Listing.location).order_by(db.desc('booking_count')).all()
    return jsonify({
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'popular_locations': [{'location': loc, 'bookings': count} for loc, count in popular_locations]
    })

# ======promote or demote a user from guest to host or vice versa ==========
@admin_blueprint.route('/users/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
def change_user_role(user_id):
    admin_id = get_jwt_identity()
    current_user = User.query.get(admin_id)
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    new_role = data.get('role')
    if new_role not in ['guest', 'host', 'admin']:
        return jsonify({"error": "Invalid role"}), 400
    user.role = new_role
    db.session.commit()
    return jsonify({"success": f"User role changed to {new_role}"}), 200


@admin_blueprint.route('/listings/<int:listing_id>/status', methods=['PATCH'])
@jwt_required()
def update_listing_status(listing_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['Pending', 'Approved', 'Rejected']:
        return jsonify({'error': 'Invalid status value'}), 400

    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    listing.status = new_status
    db.session.commit()

    return jsonify({'message': f'Status updated to {new_status}', 'listing': listing.serialize()}), 200



