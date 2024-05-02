import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './ViewMeasurement.css'

function ViewMeasurements() {
    const [measurements, setMeasurements] = useState([]);
    const [patients, setPatients] = useState([]);
    const [selectedPatient, setSelectedPatient] = useState('');
    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [hasFetched, setHasFetched] = useState(false);

    const userDetails = JSON.parse(localStorage.getItem('userDetails'));

    const isMedicalProfessional = userDetails.roles.includes('Medical Professional');

    const fetchPatients = useCallback(async () => {
        try {
            const response = await axios.get(`http://localhost:5000/users/${userDetails.username}/view_users`, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setPatients(response.data);
        } catch (error) {
            console.error('Failed to fetch patients:', error);
        }
    }, [userDetails.username]);

    const fetchMeasurements = useCallback(async () => {
        if (isMedicalProfessional && !selectedPatient) {
            setErrorMessage('Please select a patient first.');
            setMeasurements([]);
            return;
        }

        setLoading(true);
        setHasFetched(true);
        setErrorMessage('');
        const patientUsername = isMedicalProfessional ? selectedPatient : userDetails.username;

        try {
            const apiUrl = `http://localhost:5000/users/${encodeURIComponent(patientUsername)}/measurements`;
            const response = await axios.get(apiUrl, {
                headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` }
            });
            setMeasurements(response.data);
        } catch (error) {
            console.error('Failed to fetch measurements:', error);
            setErrorMessage('Failed to fetch measurements.');
            setMeasurements([]);
        } finally {
            setLoading(false);
        }
    }, [selectedPatient, userDetails.username, isMedicalProfessional]);

    useEffect(() => {
        if (isMedicalProfessional) {
            fetchPatients();
        }
    }, [fetchPatients, isMedicalProfessional]);

    return (
        <div className="measurements-container">
            <h2>View Medical Measurements</h2>
            {isMedicalProfessional && (
                <div>
                    <label htmlFor="patient-select">Select Patient:</label>
                    <select id="patient-select" onChange={e => setSelectedPatient(e.target.value)} value={selectedPatient}>
                        <option value="">Select a patient</option>
                        {patients.map(patient => (
                            <option key={patient.id} value={patient.username}>
                                {patient.first_name} - {patient.username}
                            </option>
                        ))}
                    </select>
                </div>
            )}
            <button onClick={fetchMeasurements} disabled={loading}>
                {loading ? 'Loading...' : 'Show Measurements'}
            </button>
            <div>
                {errorMessage && <p>{errorMessage}</p>}
                {hasFetched && measurements.length > 0 ? (
                    <ul>
                        {measurements.map(measurement => (
                            <li key={measurement.id}>
                                {measurement.type}: {measurement.value} {measurement.unit}, Recorded: {measurement.timestamp}
                            </li>
                        ))}
                    </ul>
                ) : !loading && !errorMessage && <p>No measurements to display.</p>}
            </div>
        </div>
    );
}

export default ViewMeasurements;
