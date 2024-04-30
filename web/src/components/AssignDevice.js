import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AssignDeviceToPatient() {
    const [devices, setDevices] = useState([]);
    const [patients, setPatients] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState('');
    const [selectedPatient, setSelectedPatient] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchDevices = async () => {
            const response = await axios.get('http://localhost:5000/devices'); // List the devices 
            setDevices(response.data);
        };

        const fetchPatients = async () => {
            const userDetails = JSON.parse(localStorage.getItem('userDetails'));
            const response = await axios.get(`http://localhost:5000/users/${userDetails.username}/view_users`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            }); 
            setPatients(response.data);
            console.log("fetchPateints response: ", response.data)
        };

        fetchDevices();
        fetchPatients();
    }, []);

    const handleAssignDevice = async () => {
        if (!selectedDevice || !selectedPatient) {
            alert('Please select both a device and a patient.');
            return;
        }

        try {
            setLoading(true);
            const response = await axios.post('http://localhost:5000/devices/assign', {
                device_id: selectedDevice,
                patient_id: selectedPatient
            });
            console.log("Assign Device response: ", response.data)
            alert('Device assigned successfully!');
        } catch (error) {
            console.error('Failed to assign device:', error);
            alert('Failed to assign device.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Assign Device to Patient</h2>
            <div>
                <label>
                    Select Device:
                    <select
                        value={selectedDevice}
                        onChange={e => setSelectedDevice(e.target.value)}
                    >
                        <option value="">Select a Device</option>
                        {devices.map(device => (
                            <option key={device.id} value={device.id}>{device.name}</option>
                        ))}
                    </select>
                </label>
            </div>
            <div>
                <label>
                    Select Patient:
                    <select
                        value={selectedPatient}
                        onChange={e => setSelectedPatient(e.target.value)}
                    >
                        <option value="">Select a Patient</option>
                        {patients.map(patient => (
                            <option key={patient.id} value={patient.id}>{patient.first_name}</option>
                        ))}
                    </select>
                </label>
            </div>
            <button onClick={handleAssignDevice} disabled={loading}>
                {loading ? 'Assigning...' : 'Assign Device'}
            </button>
        </div>
    );
}

export default AssignDeviceToPatient;
