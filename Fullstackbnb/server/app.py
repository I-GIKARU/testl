#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime
from config import Config

from models import db, TokenBlocklist

# Blueprints
from views.user import user_bp
from views.host import host_blueprint
from views.admin import admin_blueprint
from views.auth import auth_bp
from views.booking import booking_bp
from views.favorite import favorite_bp
from views.review import review_bp
from views.listing import listing_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, supports_credentials=True)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(host_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(auth_bp)
app.register_blueprint(listing_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(favorite_bp)
app.register_blueprint(review_bp)

# Revoke token check
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    return db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar() is not None

# Root route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Fullstackbnb!'})

# Error handlers (optional, helpful in dev/prod)
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

# Entry point
if __name__ == '__main__':
    app.run(port=5000, debug=True)
