from flask import Blueprint, jsonify, request
from models import Booking, Listing, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

host_blueprint = Blueprint('host', __name__)


def require_host_role(identity=None):
    if identity is None:
        identity = get_jwt_identity()
    user = User.query.get(identity)
    if not user or user.role != 'host':
        return jsonify({"error": "Unauthorized"}), 403
    return user


# ========== Create listings =========
@host_blueprint.route('/listings', methods=['POST'])
@jwt_required()
def create_listing():
    data = request.json

    role_check = require_host_role()
    if isinstance(role_check, tuple) or hasattr(role_check, 'status_code'):
        return role_check

    user = role_check  
    identity = user.id  

    required_fields = ['title', 'description', 'price_per_night', 'location', 'amenities', 'image_url']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} required."}), 400

    new_listing = Listing(
        user_id=identity,
        title=data['title'],
        description=data['description'],
        location=data['location'],
        price_per_night=data['price_per_night'],
        amenities=data['amenities'],
        image_url=data['image_url'],
        created_at=datetime.utcnow()
    )

    try:
        db.session.add(new_listing)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to save listing", "details": str(e)}), 500

    return jsonify({
        "message": "Listing created successfully!",
        "listing": {
            "id": new_listing.id,
            "user_id": new_listing.user_id,
            "title": new_listing.title,
            "description": new_listing.description,
            "location": new_listing.location,
            "price_per_night": new_listing.price_per_night,
            "amenities": new_listing.amenities,
            "image_url": new_listing.image_url,
            "created_at": new_listing.created_at.isoformat()
        }
    }), 201




# ========== update bookings =========
@host_blueprint.route('/host/bookings/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    identity = get_jwt_identity()
    role_check = require_host_role(identity)
    if role_check:
        return role_check
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    if booking.listing.user_id != identity:
        return jsonify({"error": "Unauthorized"}), 403
    data = request.json
    booking.booking_status = data.get('booking_status', booking.booking_status)
    db.session.commit()
    return jsonify({"success": "Booking updated successfully!"}), 200

# ========== Get Bookings made on their listings =========
@host_blueprint.route('/host/bookings', methods=['GET'])
@jwt_required()
def get_host_bookings():
    identity = get_jwt_identity()
    role_check = require_host_role()
    if role_check:
        return role_check
    listings = Listing.query.filter_by(user_id=identity).all()
    listing_ids = [listing.id for listing in listings]
    bookings = Booking.query.filter(Booking.listing_id.in_(listing_ids)).all()
    return jsonify([{
        'booking_id': booking.id,
        'listing_id': booking.listing_id,
        'guest_id': booking.user_id,
        'check_in': booking.check_in,
        'check_out': booking.check_out,
        'total_price': booking.total_price,
        'booking_status': booking.booking_status
    } for booking in bookings]), 200

#  ========== Track Total Earnings =========
@host_blueprint.route('/host/total-earnings', methods=['GET'])
@jwt_required()
def track_total_earnings():
    identity = get_jwt_identity()
    role_check = require_host_role(identity)
    if role_check:
        return role_check
    listings = Listing.query.filter_by(user_id=identity).all()
    listing_ids = [listing.id for listing in listings]
    bookings = Booking.query.filter(Booking.listing_id.in_(
        listing_ids), Booking.booking_status == 'completed').all()
    total_earnings = sum(booking.total_price for booking in bookings)
    return jsonify({'total_earnings': total_earnings}), 200


# ========== Edit Listings =========
@host_blueprint.route('/host/<int:listing_id>', methods=['PUT'])
@jwt_required()
def edit_listing_v2(listing_id):
    identity = get_jwt_identity()
    
    # Get user and check role in one step
    user = User.query.get(identity)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.role != 'host':
        return jsonify({"error": "Host access required"}), 403
    
    listing = Listing.query.get(listing_id)
    if not listing or listing.user_id != identity:
        return jsonify({"error": "Listing not found or unauthorized"}), 404
    
    data = request.json
    listing.title = data.get('title', listing.title)
    listing.description = data.get('description', listing.description)
    listing.price_per_night = data.get('price_per_night', listing.price_per_night)
    listing.amenities = data.get('amenities', listing.amenities)
    listing.image_url = data.get('image_url', listing.image_url)
    listing.location = data.get('location', listing.location)
    
    db.session.commit()
    return jsonify({"success": "Listing updated successfully!"}), 200


# ========== Delete Listings =========
@host_blueprint.route('/host/<int:listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    identity = get_jwt_identity()
    role_check = require_host_role(identity)
    if role_check:
        return role_check
    listing = Listing.query.get(listing_id)
    if not listing or listing.user_id != identity:
        return jsonify({"error": "Listing not found or unauthorized"}), 404
    db.session.delete(listing)
    db.session.commit()
    return jsonify({"success": "Listing deleted successfully!"}), 200





