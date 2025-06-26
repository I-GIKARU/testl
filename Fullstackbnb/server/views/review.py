from flask import jsonify, request, Blueprint
from models import Review, db
from flask_jwt_extended import jwt_required, get_jwt_identity
review_bp = Blueprint('review', __name__)


@review_bp.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    data = request.json
    user_id = get_jwt_identity()
    new_review = Review(
        user_id=user_id,
        listing_id=data['listing_id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({"success": "Review added!"}), 201


@review_bp.route('/reviews/<int:review_id>',methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'error':"Review not found"}), 404
    if review.user_id != user_id:
        return jsonify({'error': "You are not authorized to delete this review"}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({"success":"Review deleted successfully!"}), 200

@review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    reviews_list = []
    for review in reviews:
        reviews_list.append({
            "id": review.id,
            "user_id": review.user_id,
            "listing_id": review.listing_id,
            "rating": review.rating,
            "comment": getattr(review, 'comment', '') or getattr(review, 'content', ''),  
            # add any other fields you want here
        })
    return jsonify(reviews_list), 200

