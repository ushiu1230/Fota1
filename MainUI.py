import sys
import time
import concurrent.futures
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5 import uic
from FOTAServer_GetFile import *
# from listfolder import *
saved_file_name = []

def time_consuming_task(task_number):
    print(f"Task {task_number} started...")
    time.sleep(3)  # Simulate a time-consuming task
    print(f"Task {task_number} completed.")

class CyclicThread(QThread):
    cyclic_output = pyqtSignal(str)
    
    def run(self):
        saved_file_name = load_file_name()
        while True:
            file_result_information = get_file_from_cloud(saved_file_name)
            Get_file_status = file_result_information[1]
            if Get_file_status == "OK":
                saved_file_name = file_result_information[0]
            else:
                self.cyclic_output.emit("Could not get file")
            time.sleep(2)  # 2 seconds
            self.cyclic_output.emit("Cyclic task executed.")  # Replace this with any action you want to perform cyclically

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi("mainwindow.ui", self)      

        # Connect the button to the task function
        self.runButton.clicked.connect(self.run_threaded_task)

        # Create a QTimer for the cyclic task
        self.cyclic_thread = CyclicThread()
        self.cyclic_thread.cyclic_output.connect(self.on_cyclic_output)
        self.cyclic_thread.start()

    def on_cyclic_output(self, message):
        # Display the cyclic task output in the UI (e.g., in a text box)
        self.outputTextEdit.append(message)
        # Scroll to the end of the text box to see the latest output
        cursor = self.outputTextEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.outputTextEdit.setTextCursor(cursor)

    def run_threaded_task(self):
        # Start a separate thread to run the task
        self.worker_thread = WorkerThread()
        self.worker_thread.task_completed.connect(self.show_task_completed_message)
        self.worker_thread.start()

    def show_task_completed_message(self):
        QMessageBox.information(self, "Task Completed", "The time-consuming task is completed!")

class WorkerThread(QThread):
    task_completed = pyqtSignal()

    def run(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the time_consuming_task to the thread pool
            future = executor.submit(time_consuming_task, 1)
            # Wait for the task to complete
            concurrent.futures.wait([future])

        # Emit the signal to notify the main thread that the task is completed
        self.task_completed.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
