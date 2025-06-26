import React from 'react';
import {
  MapPin,
  Bed,
  Bath,
  Users,
  Star,
  Edit3,
  Eye,
  Trash2,
  RefreshCcw,
} from 'lucide-react';

const renderAmenityIcon = (amenity) => {
  const icons = { wifi: 'Wifi', parking: 'Car', kitchen: 'Coffee', tv: 'Tv' };
  return <span className="mr-1">{amenity}</span>;
};

function ListingsTab({
  listings,
  animate,
  getStatusColor,
  onEdit,
  onDelete,
  onToggleStatus,
}) {
  return (
    <div
      className={`transition-all duration-500 ${
        animate ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-purple-600 mb-6">
        Manage Your Listings 🏠
      </h1>
      <div className="grid gap-6">
        {listings.map((listing) => (
          <div
            key={listing.id}
            className="bg-white/80 p-6 rounded-2xl shadow-md border border-pink-100"
          >
            <div className="flex flex-col lg:flex-row gap-6">
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-1">{listing.title}</h3>
                <p className="text-gray-600 flex items-center mb-1">
                  <MapPin className="w-4 h-4 mr-1" />
                  {listing.location}
                </p>
                <div className="flex space-x-4 text-sm text-gray-600 mb-2">
                  <span className="flex items-center">
                    <Bed className="w-4 h-4 mr-1" />
                    {listing.bedrooms} bed
                  </span>
                  <span className="flex items-center">
                    <Bath className="w-4 h-4 mr-1" />
                    {listing.bathrooms} bath
                  </span>
                  <span className="flex items-center">
                    <Users className="w-4 h-4 mr-1" />
                    {listing.maxGuests} guests
                  </span>
                </div>
                <div className="flex space-x-2 mb-4">
                  {(Array.isArray(listing.amenities) ? listing.amenities : []).map(
                    (a, index) => (
                      <span
                        key={`${listing.id}-amenity-${index}-${a}`}
                        className="px-3 py-1 text-sm bg-purple-100 text-purple-800 rounded-full flex items-center"
                      >
                        {renderAmenityIcon(a)} <span className="ml-1">{a}</span>
                      </span>
                    )
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-gray-600">
                    <Star className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                    {listing.rating ?? 0} ({listing.reviews ?? 0} reviews)
                  </div>
                  <div className="text-lg font-bold text-pink-600">
                    ${listing.price ?? 0}/night
                  </div>
                </div>
                <div className="mt-4 flex space-x-3">
                  <button
                    onClick={() => onEdit(listing.id)}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg flex items-center hover:bg-blue-600"
                  >
                    <Edit3 className="w-4 h-4 mr-2" />
                    Edit
                  </button>
                  <button
                    onClick={() => onDelete(listing.id)}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg flex items-center hover:bg-red-600"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete
                  </button>
                  <button
                    onClick={() => onToggleStatus(listing.id)}
                    className={`px-4 py-2 rounded-lg flex items-center ${
                      listing.status === 'Active'
                        ? 'bg-yellow-400 text-black hover:bg-yellow-500'
                        : 'bg-gray-300 text-gray-700 hover:bg-gray-400'
                    }`}
                  >
                    <RefreshCcw className="w-4 h-4 mr-2" />
                    {listing.status === 'Active' ? 'Deactivate' : 'Activate'}
                  </button>
                </div>
              </div>
              <div className="lg:w-48">
                <div className="text-center text-4xl mb-2">
                  {listing.images && listing.images.length > 0
                    ? listing.images[0]
                    : '🏠'}
                </div>
                <div className="text-sm text-gray-600 mb-4">Featured</div>
                <div className="space-y-1 text-sm">
                  <p>
                    <strong>Bookings:</strong> {listing.bookings ?? 0}
                  </p>
                  <p>
                    <strong>Revenue:</strong>{' '}
                    <span className="text-green-600">
                      ${Number(listing.revenue ?? 0).toLocaleString()}
                    </span>
                  </p>
                </div>
                <div
                  className={`mt-2 px-2 py-1 rounded-full text-xs font-medium inline-block ${getStatusColor(
                    listing.status
                  )}`}
                >
                  {listing.status}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ListingsTab;