import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
    const navigate = useNavigate();
    const userDetails = JSON.parse(localStorage.getItem('userDetails'));

    const handleLogout = () => {
        localStorage.clear(); // Clear all local storage
        navigate('/login');
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <p>Welcome, {userDetails.first_name} {userDetails.last_name}!</p>
            <div>Email: {userDetails.email}</div>
            <div>Roles: {userDetails.roles.join(', ')}</div>
            {/* Render more user details or UI elements based on roles or permissions */}
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
}

export default Dashboard;
