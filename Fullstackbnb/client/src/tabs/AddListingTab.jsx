import React from 'react';

function AddListingTab({
  newListing,
  setNewListing,
  toggleAmenity,
  handleAddListing,
  setSelectedTab,
  animate,
}) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewListing((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const availableAmenities = [
    'Wi-Fi',
    'Air Conditioning',
    'Kitchen',
    'Free Parking',
    'Washer',
    'Pool',
  ];

  return (
    <div
      className={`transition-all duration-500 ${
        animate ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-600 to-purple-600 mb-6">
        Add New Listing 🏠
      </h1>

      <form onSubmit={handleAddListing} className="space-y-6 max-w-lg">
        {/* Title */}
        <div>
          <label className="block font-semibold mb-1" htmlFor="title">
            Title
          </label>
          <input
            id="title"
            name="title"
            value={newListing.title}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded-md p-2"
            placeholder="Listing title"
          />
        </div>

        {/* Location */}
        <div>
          <label className="block font-semibold mb-1" htmlFor="location">
            Location
          </label>
          <input
            id="location"
            name="location"
            value={newListing.location}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded-md p-2"
            placeholder="City, state, or address"
          />
        </div>

        {/* Description */}
        <div>
          <label className="block font-semibold mb-1" htmlFor="description">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={newListing.description}
            onChange={handleChange}
            rows={4}
            required
            className="w-full border border-gray-300 rounded-md p-2"
            placeholder="Describe your listing"
          />
        </div>

        {/* Image URL */}
        <div>
          <label className="block font-semibold mb-1" htmlFor="image_url">
            Image URL
          </label>
          <input
            id="image_url"
            name="image_url"
            value={newListing.image_url || ''}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-md p-2"
            placeholder="https://example.com/image.jpg"
          />
        </div>

        {/* Price per night */}
        <div>
          <label className="block font-semibold mb-1" htmlFor="price">
            Price per Night (USD)
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={newListing.price}
            onChange={handleChange}
            required
            className="w-full border border-gray-300 rounded-md p-2"
            placeholder="100"
          />
        </div>

        {/* Amenities */}
        <div>
          <label className="block font-semibold mb-1">Amenities</label>
          <div className="grid grid-cols-2 gap-2">
            {availableAmenities.map((amenity) => (
              <label key={amenity} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={newListing.amenities.includes(amenity)}
                  onChange={() => toggleAmenity(amenity)}
                  className="form-checkbox h-4 w-4 text-pink-600"
                />
                <span>{amenity}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit */}
        <button
          type="submit"
          className="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold rounded-xl shadow hover:from-pink-600 hover:to-purple-700 transition-all duration-200"
        >
          Add Listing
        </button>
      </form>
    </div>
  );
}

export default AddListingTab;
