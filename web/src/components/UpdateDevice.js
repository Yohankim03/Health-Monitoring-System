import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './UpdateDevice.css'

function UpdateDeviceStatus() {
    const [devices, setDevices] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState('');
    const [newStatus, setNewStatus] = useState('');

    useEffect(() => {
        const fetchDevices = async () => {
            try {
                const response = await axios.get('http://localhost:5000/devices', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
                });
                setDevices(response.data);
            } catch (error) {
                console.error('Failed to fetch devices:', error);
            }
        };
        fetchDevices();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const encodedDeviceName = encodeURIComponent(selectedDevice);
        try {
            await axios.put(`http://localhost:5000/devices/${encodedDeviceName}/status`, {
                status: newStatus
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            alert('Device status updated successfully!');
            window.location.reload();
        } catch (error) {
            console.error('Failed to update device status:', error);
            alert('Failed to update device status.');
        }
    };
    
    return (
        <div className="update-device-status-container">
            <h2>Update Device Status</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Select Device:</label>
                    <select value={selectedDevice} onChange={e => setSelectedDevice(e.target.value)}>
                        <option value="">Select a device</option>
                        {devices.map(device => (
                            <option key={device.id} value={device.name}>
                                {device.name} (Current status: {device.status})
                            </option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>New Status:</label>
                    <input type="text" value={newStatus} onChange={e => setNewStatus(e.target.value)} required />
                </div>
                <button type="submit">Update Status</button>
            </form>
        </div>
    );
}

export default UpdateDeviceStatus;
