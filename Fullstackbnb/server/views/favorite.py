from flask import Blueprint, request, jsonify
from models import db, Favorites, Listing, User

favorite_bp = Blueprint('favorite_', __name__)


@favorite_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    results = []
    for favorite in favorites:
        listing = Listing.query.get(favorite.listing_id)
        results.append({
            "favorite_id": favorite.id,
            "listing_id": listing.id if listing else None,
            "title": listing.title if listing else None,
            "description": listing.description if listing else None,
            "price_per_night": listing.price_per_night if listing else None,
            "image_url": listing.image_url if listing else None,
            "note": favorite.note,
            "created_at": favorite.created_at
        })
    return jsonify(results), 200


@favorite_bp.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    user_id = data.get('user_id')
    listing_id = data.get('listing_id')
    note = data.get(
        'note', 'Want to book next month we gatchu you can always count on us!')

    # Check if the user and listing exist
    if not user_id or not listing_id:
        return jsonify({"error": "User_id and Listing_id required"}), 400
    user = User.query.get(user_id)
    listing = Listing.query.get(listing_id)
    if not user or not listing:
        return jsonify({"error": "User or Listing does not exist"}), 404

    # prevent duplicate favorites
    existing_favorite = Favorites.query.filter_by(
        user_id=user_id, listing_id=listing_id).first()
    if existing_favorite:
        return jsonify({"error": "This listing exists in your favorites"}), 400

    # Add the new favorite
    new_favorite = Favorites(user_id=user_id, listing_id=listing_id, note=note)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"success": "Listing added to favorites successfully!"}), 201

@favorite_bp.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def remove_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"success": "Favorite removed successfully!"}), 200
