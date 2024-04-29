import React from 'react';
import { useNavigate } from 'react-router-dom';
import EnterMeasurement from './EnterMeasurement';
import ViewMeasurements from './ViewMeasurement';

function Dashboard() {
    const navigate = useNavigate();
    const userDetails = JSON.parse(localStorage.getItem('userDetails'));
    const hasPatientRole = userDetails.roles.includes('Patient')

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
            
            {/* Has Patient role */}
            {hasPatientRole && <EnterMeasurement />}
            {hasPatientRole && <ViewMeasurements />}

            <button onClick={handleLogout}>Logout</button>
        </div>
    );
}

export default Dashboard;
