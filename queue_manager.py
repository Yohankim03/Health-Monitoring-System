import threading
from queue import Queue
import logging
# from your_application import create_report, send_notification  # Import your report generation and notification sending functions
logging.basicConfig(level=logging.INFO)
task_queue = Queue()

def worker():
    while True:
        task, args = task_queue.get()
        logging.info(f"Starting task with args {args}")
        try:
            task(*args)
            logging.info("Task completed successfully")
        except Exception as e:
            logging.error(f"Error executing task: {e}")
        finally:
            task_queue.task_done()

# Start a thread that runs the worker function
worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()