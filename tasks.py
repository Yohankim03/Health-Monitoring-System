# tasks.py
from api.models import Measurement, DeviceAssignment, Report, Device
from extensions import db
from datetime import datetime
import logging

def generate_report_task(generated_by, patient_id):
    from app import app  # Move the import statement inside the function
    with app.app_context():
        logging.info(f"Generating report for patient {patient_id}")
        measurements = Measurement.query.filter_by(user_id=patient_id).all()
        device_assignments = DeviceAssignment.query.filter_by(patient_id=patient_id).all()

        report_content = "Patient Report\n\nMeasurements:\n"
        for measurement in measurements:
            report_content += f"Type: {measurement.type}, Value: {measurement.value} {measurement.unit}, Timestamp: {measurement.timestamp}\n"

        report_content += "\nDevices Assigned:\n"
        for assignment in device_assignments:
            device = Device.query.get(assignment.device_id)
            report_content += f"Device Name: {device.name}, Assigned On: {assignment.assigned_on}\n"

        new_report = Report(
            generated_by=generated_by,
            patient_id=patient_id,
            content=report_content
        )
        db.session.add(new_report)
        db.session.commit()
        logging.info(f"Report for patient {patient_id} generated successfully")
