#!/usr/bin/env python3
from app import app
from models import db, User, Listing, Booking, Favorites, Review
from werkzeug.security import generate_password_hash

users = [
    {"username":"Jayden Kamau", "email":"jayden@gmail.com", "password":"jay123", "role":"host"},
    {"username":"Margaret Wambui", "email":"margaret@gmail.com", "password":"magimagi", "role":"guest"},
    {"username": "Jason Kahare", "email": "jay@gmail.com", "password": "jayjay124", "role": "guest"},
    {"username": "George Kamau", "email": "kamau3@gmail.com", "password": "kamaubeme123", "role": "guest"},
    {"username": "William Muiruri", "email":"muiruri@gmail.com", "password":"muiruri123", "role":"admin"},
]

listings = [
    {"id":1, "user_id": 1, "title": "Cozy Cottage", "description": "A cozy cottage in the woods.", "price_per_night": 100.0, "amenities": "WiFi, Fireplace", "location": "Woods", "image_url": "https://images.unsplash.com/photo-1723258343563-7d71a55d6dfa?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDF8fHxlbnwwfHx8fHw%3D", "status":"Pending"},
    {"id":2 , "user_id": 1, "title": "Modern Apartment", "description": "A modern apartment in the city center.", "price_per_night": 150.0, "amenities": "WiFi, Air Conditioning, Pool", "location": "city center", "image_url": "https://images.unsplash.com/photo-1634351580440-8fcf7813367e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGFuJTIwYWlyYm5iJTIwd2l0aCUyMHN1Y2glMjBkZXNjcmlwdGlvbiUyMCUyMCUyMkElMjBsdXh1cnklMjB2aWxsYSUyMGluJTIwdGhlJTIwY2l0eSUyMGNlbnRlci4lMjJ8ZW58MHx8MHx8fDA%3D","status":"Pending"},
    {"id":3 , "user_id": 2, "title": "Beach House", "description": "A beautiful beach house with ocean views.", "price_per_night": 200.0, "amenities": "WiFi, Beach Access, Pool", "location": "Beachfront", "image_url": "https://images.unsplash.com/photo-1711426793021-ae58d127d79c?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8YW4lMjBhaXJibmIlMjB3aXRoJTIwc3VjaCUyMGRlc2NyaXB0aW9uJTIwJTIyQSUyMGJlYXV0aWZ1bCUyMGJlYWNoJTIwaG91c2UlMjB3aXRoJTIwb2NlYW4lMjB2aWV3cy4lMjJ8ZW58MHx8MHx8fDA%3D", "status":"Pending"},
    {"id":4 , "user_id": 2, "title": "Mountain Cabin", "description": "A rustic cabin in the mountains.", "price_per_night": 120.0, "amenities": "WiFi, Fireplace, Hiking Trails", "location": "Mountains", "image_url": "https://images.unsplash.com/photo-1660704897219-452265e6dd7e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8YW4lMjBhaXJibmIlMjB3aXRoJTIwc3VjaCUyMGRlc2NyaXB0aW9uJTIwJTIyQSUyMGJlYXV0aWZ1bCUyMG1vdW50YWluJTIwdmlld3MuJTIyfGVufDB8fDB8fHww", "status":"Pending"},
    {"id":5 , "user_id": 3, "title": "Luxury Villa", "description": "A luxury villa with a private pool.", "price_per_night": 300.0, "amenities": "WiFi, Pool, Spa", "location": "Uptown", "image_url": "https://plus.unsplash.com/premium_photo-1687995673113-865539d3b21d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YW4lMjBhaXJibmIlMjB3aXRoJTIwc3VjaCUyMGRlc2NyaXB0aW9uJTIwJTIwJTIyQSUyMGx1eHVyeSUyMHZpbGxhJTIwaW4lMjB0aGUlMjBjaXR5JTIwY2VudGVyLiUyMnxlbnwwfHwwfHx8MA%3D%3D", "status":"Pending"},
]

bookings = [
    {"id":1, "user_id": 2, "listing_id": 1, "booking_status": "completed", "total_price": 400.0},
    {"id":2, "user_id": 3, "listing_id": 2,  "booking_status": "pending", "total_price": 750.0},
    {"id":3, "user_id": 4, "listing_id": 3,  "booking_status": "completed", "total_price": 1400.0},
    {"id":4, "user_id": 5, "listing_id": 4,  "booking_status": "pending", "total_price": 240.0},
    {"id":5, "user_id": 1, "listing_id": 5,  "booking_status": "completed", "total_price": 900.0},
]

favorites = [
    {"id":1, "user_id": 2, "listing_id": 1, "note": "Looking forward to booking this next month!"},
    {"id":2, "user_id": 3, "listing_id": 2, "note": "This place looks amazing!"},
    {"id":3, "user_id": 4, "listing_id": 3, "note": "Can't wait to stay here!"},
    {"id":4, "user_id": 5, "listing_id": 4, "note": "This is my dream vacation spot!"},
    {"id":5, "user_id": 1, "listing_id": 5, "note": "Perfect for a weekend getaway!"},
] 

reviews = [
    {"id": 1, "user_id": 2, "listing_id": 1, "comment": "Had a wonderful stay! The cottage was cozy and well-equipped.", "rating": 5},
    {"id": 2, "user_id": 3, "listing_id": 2, "comment": "The apartment was modern and clean. Great location!", "rating": 4},
    {"id": 3, "user_id": 4, "listing_id": 3, "comment": "Amazing views from the beach house. Highly recommend!", "rating": 5},
    {"id": 4, "user_id": 5, "listing_id": 4, "comment": "The cabin was rustic and charming. Perfect for a mountain retreat.", "rating": 4},
    {"id": 5, "user_id": 1, "listing_id": 5, "comment": "The villa was luxurious and spacious. Loved the private pool!", "rating": 5},

]

with app.app_context():
    db.session.query(Favorites).delete()
    db.session.query(Booking).delete()
    db.session.query(Listing).delete()
    db.session.query(User).delete()
    db.session.query(Review).delete()
    db.session.commit()

    user_objs = [User(username=user["username"], email=user["email"], password=generate_password_hash(user["password"]), role=user["role"]) for user in users]
    db.session.add_all(user_objs)
    db.session.commit()

    listing_objs = [Listing(**listing) for listing in listings]
    db.session.add_all(listing_objs)
    db.session.commit()

    booking_objs = [Booking(**booking) for booking in bookings]
    db.session.add_all(booking_objs)
    db.session.commit()

    favorite_objs = [Favorites(**favorite) for favorite in favorites]
    db.session.add_all(favorite_objs)
    db.session.commit()

    review_objs = [Review(**review) for review in reviews]
    db.session.add_all(review_objs)
    db.session.commit()

    print("Seed data inserted successfully!")
