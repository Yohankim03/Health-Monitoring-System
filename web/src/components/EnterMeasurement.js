// import React, { useState } from 'react';
// import axios from 'axios';

// function EnterMeasurement() {
//     const [measurement, setMeasurement] = useState({
//         type: '',
//         value: '',
//         unit: ''
//     });

//     const handleChange = (e) => {
//         setMeasurement({
//             ...measurement,
//             [e.target.name]: e.target.value
//         });
//     };

//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             const userDetails = JSON.parse(localStorage.getItem('userDetails'));
//             const response = await axios.post(`http://localhost:5000/users/${userDetails.username}/addmeasurements`, measurement, {
//                 headers: {
//                     Authorization: `Bearer ${localStorage.getItem('accessToken')}`
//                 }
//             });
//             console.log('Measurement Added:', response.data);
//             alert('Measurement added successfully!');
//             // Reset form
//             setMeasurement({ type: '', value: '', unit: '' });
//         } catch (error) {
//             console.error('Error adding measurement:', error);
//             alert('Failed to add measurement.');
//         }
//     };

//     return (
//         <div>
//             <h2>Enter Medical Measurement</h2>
//             <form onSubmit={handleSubmit}>
//                 <div>
//                     <label>Measurement Type:</label>
//                     <input
//                         type="text"
//                         name="type"
//                         value={measurement.type}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>
//                 <div>
//                     <label>Value:</label>
//                     <input
//                         type="number"
//                         name="value"
//                         value={measurement.value}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>
//                 <div>
//                     <label>Units:</label>
//                     <input
//                         type="text"
//                         name="unit"
//                         value={measurement.unit}
//                         onChange={handleChange}
//                         required
//                     />
//                 </div>
//                 <button type="submit">Submit Measurement</button>
//             </form>
//         </div>
//     );
// }

// export default EnterMeasurement;

import React, { useState } from 'react';
import { useEffect } from 'react';
import axios from 'axios';

function EnterMeasurement() {
    const [measurement, setMeasurement] = useState({
        patientId: '', // Only needed if the user is a medical professional
        type: '',
        value: '',
        unit: ''
    });
    
    const [patients, setPatients] = useState([]); // To store the list of patients
    const [isMedicalProfessional, setIsMedicalProfessional] = useState(false);
    

    const handleChange = (e) => {
        setMeasurement({
            ...measurement,
            [e.target.name]: e.target.value
        });
    };

    useEffect(() => {
        const userDetails = JSON.parse(localStorage.getItem('userDetails'));
        setIsMedicalProfessional(userDetails.roles.includes('Medical Professional'));
    
        if (userDetails.roles.includes('Medical Professional')) {
            const fetchPatients = async () => {
                const userDetails = JSON.parse(localStorage.getItem('userDetails'));
                const response = await axios.get(`http://localhost:5000/users/${userDetails.username}/view_users`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                    }
                }); 
                setPatients(response.data.map(patient => ({
                    id: patient.id,
                    name: patient.first_name, // Assuming you want to display first name in the dropdown
                    username: patient.username // Ensure username is also fetched
                })));
                console.log("fetchPateints response: ", response.data)
            };
            
            fetchPatients();
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        let postData;
        let url;
    
        // Check if the user is a medical professional and selecting a patient
        if (isMedicalProfessional && measurement.patientId) {
            const selectedPatient = patients.find(p => p.id === parseInt(measurement.patientId));
            if (!selectedPatient) {
                alert('Invalid patient selected.');
                return;
            }
            postData = {
                ...measurement,
                patientId: selectedPatient.id 
            };
            url = `http://localhost:5000/users/${selectedPatient.username}/addmeasurements`;
        } else if (!isMedicalProfessional) {
            // If the user is a patient, use their own username
            const userDetails = JSON.parse(localStorage.getItem('userDetails'));
            postData = {
                ...measurement,
                patientId: userDetails.id 
            };
            url = `http://localhost:5000/users/${userDetails.username}/addmeasurements`;
        } else {
            alert('Please select a patient.');
            return;
        }
    
        try {
            const response = await axios.post(url, postData, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('accessToken')}`
                }
            });
            console.log('Measurement Added:', response.data);
            alert('Measurement added successfully!');
            setMeasurement({ patientId: '', type: '', value: '', unit: '' });
        } catch (error) {
            console.error('Error adding measurement:', error);
            alert('Failed to add measurement.');
        }
    };
    

    return (
        <div>
            <h2>Enter Medical Measurement</h2>
            <form onSubmit={handleSubmit}>
                {isMedicalProfessional && (
                    <div>
                        <label>Patient:</label>
                        <select
                            name="patientId"
                            value={measurement.patientId}
                            onChange={handleChange}
                            required={isMedicalProfessional}
                        >
                            <option value="">Select a Patient</option>
                            {patients.map(patient => (
                                <option key={patient.id} value={patient.id}>
                                    {patient.name}
                                </option>
                            ))}
                        </select>
                    </div>
                )}
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