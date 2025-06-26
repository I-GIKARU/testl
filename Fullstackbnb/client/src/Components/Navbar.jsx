import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <nav className="bg-pink-100 shadow-md px-6 py-4 flex items-center justify-between">
            <Link to="/" className="text-2xl font-extrabold text-pink-600">
                Airbnb Platform
            </Link>
            <div className="space-x-4">
                <Link to="/" className="text-pink-700 hover:text-pink-500 font-medium">Home</Link>
                <Link to="/Signup" className="text-pink-700 hover:text-pink-500 font-medium">Sign Up</Link>
                {/*<Link to="/user" className="text-pink-700 hover:text-pink-500 font-medium">Dashboard</Link>*/}
                {/*<Link to="/host" className="text-pink-700 hover:text-pink-500 font-medium">Host Panel</Link>*/}
                {/*<Link to="/admin" className="text-pink-700 hover:text-pink-500 font-medium">Admin</Link>*/}
                <Link to="/login" className="text-pink-700 hover:text-pink-500 font-medium">Login</Link>
                <Link to="/logout" className="text-pink-700 hover:text-pink-500 font-medium">Logout</Link>
            </div>
        </nav>
    );
}

export default Navbar;