// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
    return (
        <div className="home-container">
            <h1>Welcome to the Health Monitoring System</h1>
            <p>Returning users please log in. New users please sign up.</p>
            <Link to="/login">Login</Link> 
            <Link to="/signup">Sign Up</Link>
        </div>
    );
}

export default Home;
