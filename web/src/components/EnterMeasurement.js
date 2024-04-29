import React, { useState } from 'react';
import axios from 'axios';

function EnterMeasurement() {
    const [measurement, setMeasurement] = useState({
        type: '',
        value: '',
        unit: ''
    });

    const handleChange = (e) => {
        setMeasurement({
            ...measurement,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const userDetails = JSON.parse(localStorage.getItem('userDetails'));
            const response = await axios.post(`http://localhost:5000/users/${userDetails.username}/addmeasurements`, measurement, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
            console.log('Measurement Added:', response.data);
            alert('Measurement added successfully!');
            // Reset form
            setMeasurement({ type: '', value: '', unit: '' });
        } catch (error) {
            console.error('Error adding measurement:', error);
            alert('Failed to add measurement.');
        }
    };

    return (
        <div>
            <h2>Enter Medical Measurement</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Measurement Type:</label>
                    <input
                        type="text"
                        name="type"
                        value={measurement.type}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Value:</label>
                    <input
                        type="number"
                        name="value"
                        value={measurement.value}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label>Units:</label>
                    <input
                        type="text"
                        name="unit"
                        value={measurement.unit}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit">Submit Measurement</button>
            </form>
        </div>
    );
}

export default EnterMeasurement;
