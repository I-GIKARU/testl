import React, { useState, useEffect } from 'react';

// Tabs
import OverviewTab from '../tabs/OverviewTab.jsx';
import ListingsTab from '../tabs/ListingsTab.jsx';
import AddListingTab from '../tabs/AddListingTab.jsx';
import BookingsTab from '../tabs/BookingsTab.jsx';
import EarningsTab from '../tabs/EarningsTab.jsx';
import InsightsTab from '../tabs/InsightsTab.jsx';
import Sidebar from '../tabs/Sidebar.jsx';

function HostDashboard() {
  const [selectedTab, setSelectedTab] = useState('overview');
  const [animateCards, setAnimateCards] = useState(false);

  const [listings, setListings] = useState([]);
  const [bookingRequests, setBookingRequests] = useState([]);

  const [newListing, setNewListing] = useState({
    title: '',
    location: '',
    price: '',
    bedrooms: 1,
    bathrooms: 1,
    maxGuests: 1,
    description: '',
    amenities: [],
    status: 'Active',
    images: ['🏠'],
    rating: 0,
    reviews: 0,
    bookings: 0,
    revenue: 0,
  });

  // Fetch listings and booking requests on mount or tab change
  useEffect(() => {
    setAnimateCards(true);

    // Fetch listings
    fetch('http://127.0.0.1:5000/listings')
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setListings(data);
          } else {
            console.error('Invalid listings data:', data);
            setListings([]); // fallback to empty array
          }
        })
        .catch(err => {
          console.error('Error fetching listings:', err);
          setListings([]); // fallback to empty array on error
        });


    // Fetch booking requests
    fetch('http://127.0.0.1:5000/bookings')
      .then(res => res.json())
      .then(data => setBookingRequests(data))
      .catch(err => console.error('Error fetching booking requests:', err));
  }, [selectedTab]);

  const totalRevenue = listings.reduce((sum, l) => sum + (l.revenue || 0), 0);
  const totalBookings = listings.reduce((sum, l) => sum + (l.bookings || 0), 0);
  const averageRating =
    listings.length > 0
      ? listings.reduce((sum, l) => sum + (l.rating || 0), 0) / listings.length
      : 0;

  // Handlers for booking requests
  const handleApproveRequest = (id) =>
    setBookingRequests((prev) =>
      prev.map((req) =>
        req.id === id ? { ...req, status: 'Approved' } : req
      )
    );

  const handleRejectRequest = (id) =>
    setBookingRequests((prev) =>
      prev.map((req) =>
        req.id === id ? { ...req, status: 'Rejected' } : req
      )
    );

  // Add or update listing handler
  const handleAddListing = (e) => {
    e.preventDefault();

    if (newListing.id) {
      // Editing existing listing
      setListings(listings.map(l => (l.id === newListing.id ? newListing : l)));
    } else {
      // Adding new listing
      const newId = listings.length > 0 ? Math.max(...listings.map(l => l.id)) + 1 : 1;
      setListings([...listings, { ...newListing, id: newId }]);
    }

    // Reset form and go back to listings tab
    setNewListing({
      title: '',
      location: '',
      price: '',
      bedrooms: 1,
      bathrooms: 1,
      maxGuests: 1,
      description: '',
      amenities: [],
      status: 'Active',
      images: ['🏠'],
      rating: 0,
      reviews: 0,
      bookings: 0,
      revenue: 0,
    });

    setSelectedTab('listings');
  };

  const toggleAmenity = (amenity) =>
    setNewListing((prev) => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter((a) => a !== amenity)
        : [...prev.amenities, amenity],
    }));

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active':
      case 'Approved':
        return 'bg-green-100 text-green-800';
      case 'Inactive':
        return 'bg-gray-100 text-gray-800';
      case 'Pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'Rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // --- New handlers for managing listings ---

  const handleEditListing = (id) => {
    const listingToEdit = listings.find(l => l.id === id);
    if (listingToEdit) {
      setNewListing(listingToEdit);
      setSelectedTab('add-listing');
    }
  };

  const handleDeleteListing = (id) => {
    if (window.confirm('Are you sure you want to delete this listing?')) {
      setListings(listings.filter(l => l.id !== id));
    }
  };

  const handleToggleListingStatus = (id) => {
    setListings(listings.map(l =>
      l.id === id
        ? { ...l, status: l.status === 'Active' ? 'Inactive' : 'Active' }
        : l
    ));
  };

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-50">
      <Sidebar selectedTab={selectedTab} setSelectedTab={setSelectedTab} />

      <main className="flex-1 p-8">
        {selectedTab === 'overview' && (
          <OverviewTab
            listings={listings}
            totalRevenue={totalRevenue}
            totalBookings={totalBookings}
            averageRating={averageRating}
            setSelectedTab={setSelectedTab}
            animate={animateCards}
          />
        )}

        {selectedTab === 'listings' && (
          <ListingsTab
            listings={listings}
            animate={animateCards}
            getStatusColor={getStatusColor}
            onEdit={handleEditListing}
            onDelete={handleDeleteListing}
            onToggleStatus={handleToggleListingStatus}
          />
        )}

        {selectedTab === 'add-listing' && (
          <AddListingTab
            newListing={newListing}
            setNewListing={setNewListing}
            toggleAmenity={toggleAmenity}
            handleAddListing={handleAddListing}
            setSelectedTab={setSelectedTab}
            animate={animateCards}
          />
        )}

        {selectedTab === 'bookings' && (
          <BookingsTab
            bookings={bookingRequests}
            onCancelBooking={(id) => {
              // implement cancellation if needed
              setBookingRequests((prev) => prev.filter(b => b.id !== id));
            }}
            onBrowseListings={() => setSelectedTab('listings')}
            animate={animateCards}
          />
        )}

        {selectedTab === 'earnings' && (
          <EarningsTab
            listings={listings}
            totalRevenue={totalRevenue}
            totalBookings={totalBookings}
            animate={animateCards}
          />
        )}

        {selectedTab === 'insights' && (
          <InsightsTab listings={listings} animate={animateCards} />
        )}
      </main>
    </div>
  );
}

export default HostDashboard;
