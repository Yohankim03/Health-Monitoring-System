import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.models import User, Report, Device, Measurement, DeviceAssignment  # Adjust imports as needed
from queue_manager import task_queue
from tasks import generate_report_task
from flask_testing import TestCase

class TestReportGeneration(TestCase):
    def test_report_generation_enqueue(self):
        task_queue.put((generate_report_task, (1, 1)))  # Adjust as necessary

        # Directly process the task
        task, args = task_queue.get_nowait()
        task(*args)
        task_queue.task_done()

        report = Report.query.first()
        assert report is not None
        assert "Patient Report" in report.content
        
if __name__ == "__main__":
    pytest.main()
