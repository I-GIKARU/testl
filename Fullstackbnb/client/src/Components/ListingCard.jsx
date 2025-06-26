import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function ListingCard({ listing }) {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/listings/${listing.id}/image_url`)
      .then(res => res.json())
      .then(data => setImageUrl(data.image_url))
      .catch(() => setImageUrl('https://cdn.pixabay.com/photo/2018/01/31/12/16/architecture-3121009_640.jpg'));
  }, [listing.id]);

  return (
    <Link to={`/listing/${listing.id}`} className="block rounded shadow hover:shadow-lg transition overflow-hidden">
      <img
        src={imageUrl}
        alt={listing.title}
        className="w-full h-52 object-cover"
      />
      <div className="p-4">
        <h3 className="text-lg font-semibold">{listing.title}</h3>
        <p className="text-sm text-gray-500">{listing.location}</p>
        <div className="text-pink-600 font-bold mt-1">${listing.price} <span className="text-xs font-normal">/ night</span></div>
      </div>
    </Link>
  );
}

export default ListingCard;