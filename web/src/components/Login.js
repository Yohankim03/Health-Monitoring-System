// src/components/Login.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setCredentials({...credentials, [e.target.name]: e.target.value});
    };

    const handleBack = (e) => {
        navigate('/');
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/login', credentials);
            if (response.data.access_token) {
                localStorage.setItem('accessToken', response.data.access_token);
                localStorage.setItem('userDetails', JSON.stringify(response.data.user));  // Storing user details securely
                navigate('/dashboard');
            } else {
                console.error('Login failed: No access token received');
            }
        } catch (error) {
            console.error('Login failed:', error.response ? error.response.data : error);
        }
    };

    return (
        <div className ='login-container'>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input type="text" name="username" value={credentials.username} onChange={handleChange} />
                </label>
                <label>
                    Password:
                    <input type="password" name="password" value={credentials.password} onChange={handleChange} />
                </label>
                <button type="submit">Login</button>
            </form>
            <button onClick={handleBack}>Back Home</button>
        </div>
    );
}

export default Login;
