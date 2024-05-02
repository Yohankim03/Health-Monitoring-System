import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AssignRole.css'

function ManageUserRoles() {
    const [users, setUsers] = useState([]);
    const [allRoles, setAllRoles] = useState([]);
    const [selectedUser, setSelectedUser] = useState({ id: '', username: '' });
    const [userRoles, setUserRoles] = useState([]);

    // Refactored fetching function
    const fetchData = async () => {
        const userDetails = JSON.parse(localStorage.getItem('userDetails'));
        try {
            const usersResponse = await axios.get(`http://localhost:5000/users/${userDetails.username}/view_users`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            const rolesResponse = await axios.get('http://localhost:5000/admin/roles', {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setUsers(usersResponse.data);
            setAllRoles(rolesResponse.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleUserChange = (e) => {
        const userId = e.target.value;
        const user = users.find(u => u.id.toString() === userId);
        if (user) {
            setSelectedUser({ id: user.id, username: user.username });
            const rolesSet = new Set(user.roles.map(role => role.name));
            setUserRoles(rolesSet);
        }
    };

    const handleRoleChange = (roleName, isChecked) => {
        setUserRoles(prevRoles => {
            const newRoles = new Set(prevRoles);
            if (isChecked) {
                newRoles.add(roleName);
            } else {
                newRoles.delete(roleName);
            }
            return newRoles;
        });
    };

    const handleSubmit = async () => {
        try {
            await axios.put(`http://localhost:5000/admin/${selectedUser.username}/change_role`, {
                roles: Array.from(userRoles),
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            alert('Roles updated successfully!');
            // Refresh the page to reflect the changes
            window.location.reload();
        } catch (error) {
            console.error('Error updating roles:', error);
            alert('Failed to update roles.');
        }
    };

    return (
        <div className="roles-management-container">
            <h2>Manage User Roles</h2>
            <select onChange={handleUserChange} value={selectedUser.id}>
                <option value="">Select a User</option>
                {users.map(user => (
                    <option key={user.id} value={user.id}>
                        {user.username} - Roles: {user.roles.map(role => role.name).join(', ')}
                    </option>
                ))}
            </select>
            {selectedUser.id && (
                <div>
                    <h3>Assign Roles</h3>
                    {allRoles.map(role => (
                        <label key={role.id}>
                            <input
                                type="checkbox"
                                checked={userRoles.has(role.name)}
                                onChange={(e) => handleRoleChange(role.name, e.target.checked)}
                            />
                            {role.name}
                        </label>
                    ))}
                    <button onClick={handleSubmit}>Update Roles</button>
                </div>
            )}
        </div>
    );
    
}


export default ManageUserRoles;
