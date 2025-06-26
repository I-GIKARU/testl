import React from 'react';
import { useParams } from 'react-router-dom';
import BookingForm from '../Components/BookingForm';
import ReviewForm from '../Components/ReviewForm';

function ListingDetails() {
  const { id } = useParams();

  //  fetch from backend later
  const listing = {
    id,
    title: "Modern Studio Apartment",
    location: "Downtown New York",
    price: 120,
    description:
      "A beautiful and modern apartment in the heart of the city. Perfect for short stays!",
    amenities: ["WiFi", "Air Conditioning", "Kitchen", "Pool"],
    images: [
      "https://cdn.pixabay.com/photo/2018/01/31/12/16/architecture-3121009_640.jpg",
      "https://cdn.pixabay.com/photo/2018/01/31/12/16/architecture-3121009_640.jpg",
      "https://cdn.pixabay.com/photo/2018/01/31/12/16/architecture-3121009_640.jpg",
    ],
    reviews: [
      { id: 1, user: "Jane", rating: 5, comment: "Loved it!" },
      { id: 2, user: "Alex", rating: 4, comment: "Great place and location." },
    ],
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Title & Price */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold">{listing.title}</h1>
        <p className="text-gray-600">{listing.location}</p>
        <p className="text-lg font-semibold mt-2 text-pink-600">${listing.price}/night</p>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        {listing.images.map((img, i) => (
          <img key={i} src={img} alt={`Listing ${i}`} className="rounded-lg w-full h-48 object-cover" />
        ))}
      </div>

      {/* Description & Amenities */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-6">
        <div className="md:col-span-2">
          <h2 className="text-xl font-semibold mb-2">Description</h2>
          <p className="text-gray-700 mb-4">{listing.description}</p>

          <h2 className="text-xl font-semibold mb-2">Amenities</h2>
          <ul className="list-disc list-inside text-gray-600">
            {listing.amenities.map((amenity, i) => (
              <li key={i}>{amenity}</li>
            ))}
          </ul>
        </div>

        {/* Booking Form */}
        <div className="border p-4 rounded-lg shadow-md">
          <BookingForm pricePerNight={listing.price} />
        </div>
      </div>

      {/* Reviews Section */}
      <div className="mt-10">
        <h2 className="text-xl font-semibold mb-4">Reviews</h2>
        <div className="space-y-4">
          {listing.reviews.map((review) => (
            <div key={review.id} className="border-b pb-2">
              <p className="font-semibold">{review.user}</p>
              <p className="text-yellow-500">⭐ {review.rating}</p>
              <p>{review.comment}</p>
            </div>
          ))}
        </div>

        {/* Leave a Review */}
        <div className="mt-6">
          <h3 className="text-lg font-bold mb-2">Leave a Review</h3>
          <ReviewForm />
        </div>
      </div>
    </div>
  );
}

export default ListingDetails;
