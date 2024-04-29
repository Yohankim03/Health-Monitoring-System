import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function SignUp() {
    const [userData, setUserData] = useState({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_Name: '',
        dob: '',
        gender: '',
        phone_number: ''
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setUserData({...userData, [e.target.name]: e.target.value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/registration', userData);
            console.log('Registration successful:', response.data);
            navigate('/login');
        } catch (error) {
            console.error('Registration failed:', error);
        }
    };

    return (
        <div>
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input type="text" name="username" value={userData.username} onChange={handleChange} required />
                </label>
                <label>
                    Email:
                    <input type="email" name="email" value={userData.email} onChange={handleChange} required />
                </label>
                <label>
                    Password:
                    <input type="password" name="password" value={userData.password} onChange={handleChange} required />
                </label>
                <label>
                    First Name:
                    <input type="text" name="first_name" value={userData.first_name} onChange={handleChange} required />
                </label>
                <label>
                    Last Name:
                    <input type="text" name="last_name" value={userData.last_name} onChange={handleChange} required />
                </label>
                <label>
                    Date of Birth:
                    <input type="date" name="dob" value={userData.dob} onChange={handleChange} required />
                </label>
                <label>
                    Gender:
                    <select name="gender" value={userData.gender} onChange={handleChange} required>
                        <option value="">Select Gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </label>
                <label>
                    Phone Number:
                    <input type="text" name="phone_number" value={userData.phone_number} onChange={handleChange} />
                </label>
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default SignUp;
