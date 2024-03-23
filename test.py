# # test_app.py
# import unittest
# from app import app
# from queue import Empty
# from api import *
# import threading
# import queue

# url = "http://127.0.0.1:5000/"
# task_queue = queue.Queue()

# class TaskQueueTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True
    
#     def test_create_report(self):
#         response = self.app.post(url+'reports', json={"generated_by": '1', "patient_id": '4'})
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json, {
#             "id": 12,
#             "generated_by": 1,
#             "patient_id": 4,
#             "content": "Patient Report\n\nMeasurements:\nType: Blood Pressure, Value: 90.0 mmH, Timestamp: 2024-03-21 16:55:26.134204\n\nDevices Assigned:\nDevice Name: Heart Rate Monitor, Assigned On: 2024-03-21 18:37:30.815738\n",
#             "timestamp": "03-21-2024"
#         })
        
#         # Attempt to get a task from the queue for verification
#         try:
#             task_func, args, kwargs = task_queue.get_nowait()
#             self.assertEqual(task_func.__name__, 'generate_report')
#             self.assertEqual(args, (1,))
#         except Empty:
#             self.fail("Task queue was empty, expected a task to be queued.")

#     # def test_send_notification(self):
#     #     response = self.app.post('/send_notification/1/hello')
#     #     self.assertEqual(response.status_code, 202)
#     #     self.assertEqual(response.json, {'message': 'Notification sending queued'})
#     #     # Attempt to get a task from the queue for verification
#     #     try:
#     #         task_func, args, kwargs = app.task_queue.get_nowait()
#     #         self.assertEqual(task_func.__name__, 'send_notification')
#     #         self.assertEqual(args, (1, 'hello'))
#     #     except Empty:
#     #         self.fail("Task queue was empty, expected a task to be queued.")

# {'content': 'Patient Report\n'
#              '\n'
#              'Measurements:\n'
#              'Type: Blood Pressure, Value: 90.0 mmH, Timestamp: 2024-03-21 '
#              '16:55:26.134204\n'
#              '\n'
#              'Devices Assigned:\n'
#              'Device Name: Heart Rate Monitor, Assigned On: 2024-03-21 '
#              '18:37:30.815738\n',
#   'generated_by': 1,
#   'id': 4,
#   'patient_id': 4,
#   'timestamp': 'Thu, 21 Mar 2024 21:50:02 -0000'}