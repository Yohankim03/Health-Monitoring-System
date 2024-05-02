import React from 'react';
import { useNavigate } from 'react-router-dom';
import EnterMeasurement from './EnterMeasurement';
import ViewMeasurements from './ViewMeasurement';
import ViewUsers from './ViewUsers';
import AssignDevice from './AssignDevice';
import ManageUserRoles from './AssignRole'
import UpdateDevice from './UpdateDevice'
import './Dashboard.css';

function Dashboard() {
    const navigate = useNavigate();
    let userDetails = { roles: [], first_name: '', last_name: '', email: '' };
    try {
        userDetails = JSON.parse(localStorage.getItem('userDetails')) || userDetails;
    } catch (error) {
        console.error('Failed to load user details:', error);
        navigate('/login'); // Redirect to login if userDetails are corrupted or missing
    }
    
    const hasPatientRole = userDetails.roles.includes('Patient');
    const hasMedicalProRole = userDetails.roles.includes('Medical Professional');
    const hasAdminRole = userDetails.roles.includes('Admin');

    const handleLogout = () => {
        localStorage.clear(); // Clear all local storage
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>
            <div className="user-details">
                <p>Welcome, {userDetails.first_name} {userDetails.last_name}!</p>
                <div>Email: {userDetails.email}</div>
                <div>Roles: 
                    <div className="role-list">
                        {userDetails.roles.map(role => (
                            <span className="role-item" key={role}>{role}</span>
                        ))}
                    </div>
                </div>
            </div>
            
            {/* Conditional components based on user roles */}
            {(hasPatientRole || hasMedicalProRole) && (
                <div className="conditional-area">
                    <EnterMeasurement />
                </div>
            )}
            {(hasPatientRole || hasMedicalProRole) && (
                <div className="conditional-area">
                    <ViewMeasurements />
                </div>
            )}
            {hasMedicalProRole && (
                <div className="conditional-area">
                    <ViewUsers />
                </div>
            )}
            {hasMedicalProRole && (
                <div className="conditional-area">
                    <AssignDevice />
                </div>
            )}
            {hasAdminRole && (
                <div className="conditional-area">
                    <ManageUserRoles />
                </div>
            )}
            {hasAdminRole && (
                <div className="conditional-area">
                    <UpdateDevice />
                </div>
            )}
            
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
    
    
}

export default Dashboard;


