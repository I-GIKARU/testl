import React, { useState, useEffect } from 'react';
import { Calendar } from "lucide-react";
import { toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

function BookingsTab({ bookings, onCancelBooking, onBrowseListings }) {
  const [cancellingBookings, setCancellingBookings] = useState(new Set());

  const handleCancelBooking = async (bookingId) => {
    if (cancellingBookings.has(bookingId)) return;

    setCancellingBookings(prev => new Set(prev).add(bookingId));

    try {
      const token = localStorage.getItem('token');

      if (!token) {
        toast.error("Please log in to cancel bookings");
        setCancellingBookings(prev => {
          const newSet = new Set(prev);
          newSet.delete(bookingId);
          return newSet;
        });
        return;
      }

      const res = await fetch(`http://127.0.0.1:5000/bookings/${bookingId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      const data = await res.json();

      if (res.ok) {
        toast.success(data.message || "Booking cancelled successfully!");
        onCancelBooking(bookingId);
      } else {
        if (res.status === 404) {
          toast.error("Booking not found");
        } else if (res.status === 401) {
          toast.error("Unauthorized. Please log in again.");
        } else if (res.status === 403) {
          toast.error("You don't have permission to cancel this booking");
        } else {
          toast.error(data.error || "Failed to cancel booking");
        }
      }
    } catch (err) {
      console.error("Network error:", err);
      toast.error("Network error. Please check your connection and try again.");
    } finally {
      setCancellingBookings(prev => {
        const newSet = new Set(prev);
        newSet.delete(bookingId);
        return newSet;
      });
    }
  };

  return (
    <div>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-800">My Bookings</h1>
          <div className="text-2xl">📆</div>
        </div>

        {bookings.length === 0 ? (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-12 text-center shadow-lg border border-white/50">
            <Calendar size={64} className="mx-auto text-gray-400 mb-4" />
            <h3 className="text-xl font-bold text-gray-800 mb-2">No bookings yet</h3>
            <p className="text-gray-600 mb-4">Start exploring and book your first stay!</p>
            <button
              onClick={onBrowseListings}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200"
            >
              Browse Listings
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {bookings.map((booking) => {
              const isCancelling = cancellingBookings.has(booking.id);

              return (
                <div key={booking.id} className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="text-4xl">{booking.listing?.image || "🏠"}</div>
                      <div>
                        <h3 className="font-bold text-lg text-gray-800">{booking.listing?.title || booking.title}</h3>
                        <p className="text-gray-600">{booking.listing?.location}</p>
                        <div className="flex items-center space-x-4 text-sm text-gray-500 mt-1">
                          <span>{booking.check_in} to {booking.check_out}</span>
                          <span>{booking.guests} guests</span>
                          <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                            {booking.status || "confirmed"}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-gray-800">${booking.total_price}</div>
                      <button
                        onClick={() => handleCancelBooking(booking.id)}
                        disabled={isCancelling}
                        className={`mt-2 px-4 py-2 border rounded-lg transition-all duration-200 ${
                          isCancelling 
                            ? "text-gray-400 border-gray-200 bg-gray-50 cursor-not-allowed" 
                            : "text-red-600 border-red-200 hover:bg-red-50"
                        }`}
                      >
                        {isCancelling ? "Cancelling..." : "Cancel"}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default BookingsTab;
