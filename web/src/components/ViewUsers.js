import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ViewUsers() {
    const [users, setUsers] = useState([]);

    // Function to fetch users
    const fetchUsers = async () => {
        try {
            const userDetails = JSON.parse(localStorage.getItem('userDetails'));
            const response = await axios.get(`http://localhost:5000/users/${userDetails.username}/view_users`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
            console.log("/users/username/view_users response: ", response.data);
            setUsers(response.data);  // Assuming the API returns an array of user objects
        } catch (err) {
            console.error('Failed to fetch users:', err);
        } finally {
        }
    };

    // Effect hook to fetch users on component mount
    useEffect(() => {
        fetchUsers();
    }, []);

    return (
        <div>
            <h2>Users List</h2>
            <div>

                <ul>
                    {users.map(user => (
                        <li key={user.id}>
                            Username: {user.username}, Name: {user.first_name} {user.last_name}, Email: {user.email}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default ViewUsers;
