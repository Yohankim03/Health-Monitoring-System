// /services/auth.js

import axios from 'axios';

const API_URL = 'http://localhost:5000/';

export const login = async (credentials) => {
    const response = await axios.post(`${API_URL}login`, credentials);
    if (response.data.accessToken) {
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('user');
};
