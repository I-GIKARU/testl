
import { Heart } from "lucide-react";
import React from "react";

function FavoritesTab({ mockListings, favorites, toggleFavorite }) {

  return (
    <div>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-800">My Favorites</h1>
          <div className="text-2xl">❤️</div>
        </div>

        {favorites.length === 0 ? (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-12 text-center shadow-lg border border-white/50">
            <Heart size={64} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-bold text-gray-800 mb-2">No favorites yet</h3>
            <p className="text-gray-600">Save properties you love for easy access later!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockListings.filter(listing => favorites.includes(listing.id)).map((listing) => (
              <div key={listing.id} className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-white/50 overflow-hidden">
                <div className="h-48 bg-gradient-to-br from-blue-200 via-purple-200 to-pink-200 flex items-center justify-center text-6xl">
                  {listing.image}
                </div>
                <div className="p-6">
                  <h3 className="font-bold text-lg text-gray-800 mb-2">{listing.title}</h3>
                  <p className="text-gray-600 mb-4">{listing.location}</p>
                  <div className="flex items-center justify-between">
                    <div className="text-xl font-bold text-gray-800">${listing.price}/night</div>
                    <button
                      onClick={() => toggleFavorite(listing.id)}
                      className="p-2 text-red-500 bg-red-50 rounded-full hover:bg-red-100 transition-all duration-200"
                    >
                      <Heart size={20} fill="currentColor" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default FavoritesTab;