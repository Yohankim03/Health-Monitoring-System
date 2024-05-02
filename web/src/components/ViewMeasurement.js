import React, { useState } from 'react';
import axios from 'axios';
import './ViewMeasurement.css'

function ViewMeasurements() {
    const [measurements, setMeasurements] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasFetched, setHasFetched] = useState(false);  // Track if the fetch operation was triggered

    const fetchMeasurements = async () => {
        setLoading(true);
        setHasFetched(true);  // Set to true when fetching begins
        try {
            const userDetails = JSON.parse(localStorage.getItem('userDetails'));
            const response = await axios.get(`http://localhost:5000/users/${userDetails.username}/measurements`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
            setMeasurements(response.data);  // Assuming the API returns an array of measurements
            setLoading(false);
        } catch (error) {
            console.error('Failed to fetch measurements:', error);
            setLoading(false);
        }
    };

    return (
        <div className="measurements-container">
            <h2>View Your Medical Measurements</h2>
            <button onClick={fetchMeasurements} disabled={loading}>
                {loading ? 'Loading...' : 'Show Measurements'}
            </button>
            <div>
                {hasFetched && (measurements.length > 0 ? (
                    <ul>
                        {measurements.map(measurement => (
                            <li key={measurement.id}>
                                {measurement.type}: {measurement.value} {measurement.unit}, Recorded: {measurement.timestamp}
                            </li>
                        ))}
                    </ul>
                ) : (
                    !loading && <p>No measurements to display.</p>
                ))}
            </div>
        </div>
    );
}

export default ViewMeasurements;
