import React, { useEffect, useState } from 'react';
import { Star } from "lucide-react";
import ReviewForm from './ReviewForm.jsx';

function ReviewsTab() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/reviews', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(res => res.json())
      .then(data => setReviews(data))
      .catch(() => setReviews([]));
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800">My Reviews</h1>
        <div className="text-2xl">⭐</div>
      </div>

      {reviews.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-6">
          {reviews.map(review => (
            <div key={review.id} className="bg-white rounded-xl shadow p-4">
              <h2 className="font-bold text-lg mb-2">{review.listing_title || 'Listing'}</h2>
              <p className="text-gray-700 mb-2">{review.comment || review.content}</p>
              <p className="text-yellow-500 font-semibold">Rating: {review.rating}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-12 text-center shadow-lg border border-white/50">
          <Star size={64} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-bold text-gray-800 mb-2">No reviews yet</h3>
          <p className="text-gray-600">Complete a stay to leave your first review!</p>
        </div>
      )}

      <div className="mt-8 p-6 bg-white/80 rounded-xl shadow border border-white/50">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Leave a Review</h2>
        <ReviewForm />
      </div>
    </div>
  );
}

export default ReviewsTab;

