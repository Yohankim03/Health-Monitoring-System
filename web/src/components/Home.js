// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
    return (
        <div>
            <h1>Welcome to the Health Monitoring System</h1>
            <p>This is the home page.</p>
            <Link to="/login">Login</Link> | <Link to="/signup">Sign Up</Link>
        </div>
    );
}

export default Home;
