from PyQt5.QtCore import QThread, pyqtSignal
import serial
import time


class SenseSerialThread(QThread):
    serial_data = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.serial_port = None
        self.serial_baud = None
        self.serial_start = False
        self.interval = 1

    def run(self):
        while self.serial_start:
            # Delay 2 second for sensor reading.
            connect = serial.Serial(self.serial_port, int(self.serial_baud))
            data = connect.readline()
            self.serial_data.emit(data.decode("utf-8"))


