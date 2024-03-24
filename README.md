# Health Monitoring System API

The Health Monitoring System API is a Flask-based RESTful API designed to support the remote health monitoring of patients. It enables medical professionals to manage patient data, medical devices, and receive notifications about patient health metrics.

## Features

- **Authentication**: Securely manage user sessions and access.
- **Data Reading**: Record and retrieve health measurements.
- **Device Interface**: Assign and manage medical devices.
- **Notification**: Send alerts and reminders to medical professionals and patients.
- **Report Generation**: Asynchronously generate patient reports.
- **User Management**: Administer user accounts and roles.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have the following installed:

- Python 3.8+
- Pip (Python package manager)
- Docker

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

Clone the repository to your local machine:

```sh
git clone https://yourrepository.com/yourproject.git
cd yourproject
pip install -r requirements.txt
flask db upgrade
flask run
```

Or using Docker:
```sh
docker build -t health-monitoring-system .
docker run -d -p 5000:5000 health-monitoring-system
```

## Endpoints

### Authentication

#### User Registration

- **POST** `/registration`

Register a new user.

```json
{
  "username": "john_doe",
  "password": "your_password",
  "email": "john_doe@example.com"
}
```

#### User Login

- **POST** `/login`

Login into a user

```json
{
  "username": "john_doe",
  "password": "your_password"
}
```

### Notification
- **POST/GET** `/notification`
Create a new notification or retrieve notifications for the user.
POST Payload:
```json
{
  "user_id": 1,
  "message": "Your appointment is coming up tomorrow."
}
```
GET Response:
```json
{
  "patient_id": 1,
  "type": "blood_pressure",
  "value": 120.5,
  "unit": "mmHg"
}
```

### Data Reading
Record Measurement
- **POST** `/measurements`
Record a new measurement for a patient.
```json
{
  "patient_id": 1,
  "type": "blood_pressure",
  "value": 120.5,
  "unit": "mmHg"
}
```
List Measurements for User
- **GET** `/users/<int:user_id>/measurements`
Retrieve all measurements recorded for a user.

### Device Interface
Add Device
- **POST** `/devices`
Add a new device to the system.
```json
{
  "name": "Heart Rate Monitor",
  "device_type": "monitor",
  "description": "Monitors heart rate."
}
```

Assign Device to Patient
- **POST** `/devices/assign`
```json
{
  "patient_id": 1,
  "device_id": 2
}
```

### Device Interface

Add Device

- **POST** `/devices`

Add a new device to the system.

```json
{
  "name": "Heart Rate Monitor",
  "device_type": "monitor",
  "description": "Monitors heart rate."
}
```

Assign Device to Patient

- **POST** `/devices/assign`

Assign a device to a patient.

```json
{
  "patient_id": 1,
  "device_id": 2
}
```

### Device Interface

Add Device

- **POST** `/reports`

Generate a report for a patient.

```json
{
  "generated_by": 1,
  "patient_id": 1
}
```

### User Management

List Users

- **Get** `/users`

Retrieve a list of all users and their details.

Delete User

- **DELETE ** `/users/<int:id>/delete`

Remove a user from the system.