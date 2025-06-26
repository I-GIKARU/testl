import React from 'react';
import { useState } from 'react';

function BookingForm({ pricePerNight = 100 }) {
  const [checkIn, setCheckIn] = useState('');
  const [checkOut, setCheckOut] = useState('');
  const [guests, setGuests] = useState(1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Booking submitted:', { checkIn, checkOut, guests });

    const bookingData = {
      check_in: checkIn,
      check_out: checkOut,
      guests: parseInt(guests)
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingData),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Booking response:', result);
      alert('Booking request submitted! (real backend)');
    } catch (error) {
      console.error('Error submitting booking:', error);
      alert('Failed to submit booking. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h3 className="text-lg font-bold text-pink-600">Book This Stay</h3>

      <div className="flex flex-col">
        <label className="text-sm font-medium">Check-In</label>
        <input
          type="date"
          value={checkIn}
          onChange={(e) => setCheckIn(e.target.value)}
          className="border rounded px-3 py-2"
          required
        />
      </div>
      
      <div className="flex flex-col">
        <label className="text-sm font-medium">Check-Out</label>
        <input
          type="date"
          value={checkOut}
          onChange={(e) => setCheckOut(e.target.value)}
          className="border rounded px-3 py-2"
          required
        />
      </div>

      <div className="flex flex-col">
        <label className="text-sm font-medium">Guests</label>
        <input
          type="number"
          min="1"
          value={guests}
          onChange={(e) => setGuests(e.target.value)}
          className="border rounded px-3 py-2"
        />
      </div>

      <div className="text-right font-semibold text-gray-700">
        Total: ${pricePerNight} x {guests} guests
      </div>

      <button
        type="submit"
        className="w-full bg-pink-600 text-white py-2 rounded hover:bg-pink-700 transition"
      >
        Request to Book
      </button>
    </form>
  );
}

export default BookingForm;
