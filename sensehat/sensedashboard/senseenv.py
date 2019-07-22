import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QLCDNumber, QGroupBox, QWidget, \
    QFormLayout, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import QTimer, pyqtSlot
import pyqtgraph as pg
from senseDialog import SerialSourceDialog, HttpSourceDialog
from senseSerialThread import SenseSerialThread
import requests
import serial


class SenseEnvironment(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sense Environment")
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOptions(antialias=True)

        # Plot
        self.plot_temp = pg.PlotWidget()
        self.plot_temp.showGrid(x=True, y=True)
        self.plot_temp.setLabel('left', 'temp', 'C')
        self.plot_temp.setLabel('bottom', 'time', 's')
        self.plot_humidity = pg.PlotWidget()
        self.plot_humidity.showGrid(x=True, y=True)
        self.plot_humidity.setLabel('left', 'humidity', '%')
        self.plot_humidity.setLabel('bottom', 'time', 's')
        self.plot_pressure = pg.PlotWidget()
        self.plot_pressure.showGrid(x=True, y=True)
        self.plot_pressure.setLabel('left', 'pressure', 'Millibars')
        self.plot_pressure.setLabel('bottom', 'time', 's')

        # LCD Number
        self.temp_value = QLCDNumber()
        self.humidity_value = QLCDNumber()
        self.pressure_value = QLCDNumber()

        # Buttons.
        self.data_source = ['Select source', 'Serial port', 'HTTP API']
        self.data_source_btn = QComboBox()
        for source in self.data_source:
            self.data_source_btn.addItem(source)
        self.data_source_btn.currentIndexChanged.connect(self.source_data)
        self.control_btn = QPushButton("Start plot")
        self.control_btn.clicked.connect(self.plot_start)
        self.save_btn = QPushButton("Save log")
        self.plot_start = False

        # val
        self.cnt = 0
        self.temp = 0
        self.humidity = 0
        self.pressure = 0

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_update)
        self.interval = 1

        # QLine edit.
        self.interval_field = QLineEdit()
        self.interval_field.setText(str(self.interval))

        # Init serial thread.
        self.thread = SenseSerialThread(self)

        # Source
        self.source_url = None
        self.source = None
        self.serial_port = None
        self.serial_baud = None

        self.init_dashboard_ui()
        self.show()

    def init_dashboard_ui(self):
        # Temperature
        dashboard_layout = QVBoxLayout()
        dashboard_layout_temp_group = QGroupBox("TEMPERATURE")
        dashboard_layout_temp_group.setFixedHeight(250)
        dashboard_layout_temp_layout_btm = QFormLayout()
        dashboard_layout_temp_layout_btm.addRow(QLabel('Current temperature:'), self.temp_value)
        dashboard_layout_temp_layout = QVBoxLayout()
        dashboard_layout_temp_layout.addWidget(self.plot_temp)
        dashboard_layout_temp_layout.addLayout(dashboard_layout_temp_layout_btm)
        dashboard_layout_temp_group.setLayout(dashboard_layout_temp_layout)

        # Humidity.
        dashboard_layout_humidity_group = QGroupBox("HUMIDITY")
        dashboard_layout_humidity_group.setFixedHeight(250)
        dashboard_layout_humidity_layout_btm = QFormLayout()
        dashboard_layout_humidity_layout_btm.addRow(QLabel('Current humidity:'), self.humidity_value)
        dashboard_layout_humidity_layout = QVBoxLayout()
        dashboard_layout_humidity_layout.addWidget(self.plot_humidity)
        dashboard_layout_humidity_layout.addLayout(dashboard_layout_humidity_layout_btm)
        dashboard_layout_humidity_group.setLayout(dashboard_layout_humidity_layout)

        # Pressure.
        dashboard_layout_pressure_group = QGroupBox("PRESSURE")
        dashboard_layout_pressure_group.setFixedHeight(250)
        dashboard_layout_pressure_layout_btm = QFormLayout()
        dashboard_layout_pressure_layout_btm.addRow(QLabel('Current pressure:'), self.pressure_value)
        dashboard_layout_pressure_layout = QVBoxLayout()
        dashboard_layout_pressure_layout.addWidget(self.plot_pressure)
        dashboard_layout_pressure_layout.addLayout(dashboard_layout_pressure_layout_btm)
        dashboard_layout_pressure_group.setLayout(dashboard_layout_pressure_layout)

        # Configure
        dashboard_layout_tools_group = QGroupBox("CONFIGURATION")
        dashboard_layout_tools_layout = QHBoxLayout()
        dashboard_layout_tools_layout.addWidget(self.data_source_btn)
        dashboard_layout_tools_layout.addWidget(QLabel("Set interval"))
        dashboard_layout_tools_layout.addWidget(self.interval_field)
        dashboard_layout_tools_layout.addWidget(QLabel("second"))
        dashboard_layout_tools_layout.addWidget(self.control_btn)
        dashboard_layout_tools_layout.addWidget(self.save_btn)
        dashboard_layout_tools_group.setLayout(dashboard_layout_tools_layout)


        # Layouts.
        dashboard_layout.addWidget(dashboard_layout_temp_group)
        dashboard_layout.addWidget(dashboard_layout_humidity_group)
        dashboard_layout.addWidget(dashboard_layout_pressure_group)
        dashboard_layout.addWidget(dashboard_layout_tools_group)

        central_widget = QWidget(self)
        central_widget.setLayout(dashboard_layout)
        self.setCentralWidget(central_widget)

    """
    Update plot.
    """
    def plot_update(self):
        if self.source is not None:
            if self.source == 'HTTP API':
                data = self.source_http()
                if data is not None:
                    self.cnt += 1
                    self.temp = data.get('temperature')
                    self.humidity = data.get('humidity')
                    self.pressure = data.get('pressure')
                    self.temp_value.display(self.temp)
                    self.humidity_value.display(self.humidity)
                    self.pressure_value.display(self.pressure)
                    self.plot_temp.plot([self.cnt], [self.temp], pen=None, symbol="+", symbolSize=10)
                    self.plot_humidity.plot([self.cnt], [self.humidity], pen=None, symbol="+", symbolSize=10)
                    self.plot_pressure.plot([self.cnt], [self.pressure], pen=None, symbol="+", symbolSize=10)
                    QApplication.processEvents()

    """
    Update plot serial.
    """
    def plot_update_serial(self):
        pass

    """
    Start/stop plotting.
    """
    def plot_start(self):
        if self.source == 'HTTP API':
            self.interval = int(self.interval_field.text())
            if self.plot_start is not True:
                self.timer.start(self.interval)
                self.control_btn.setText("Stop plot")
                self.plot_start = True
            else:
                self.timer.stop()
                self.control_btn.setText("Start plot")
                self.plot_start = False

        if self.source == 'Serial port':
            if self.plot_start is not True:
                self.thread.interval = self.interval
                self.thread.serial_port = self.serial_port
                self.thread.serial_baud = self.serial_baud
                self.thread.serial_start = True
                self.thread.serial_data.connect(self.source_serial_port)
                self.thread.start()
                self.control_btn.setText("Stop plot")
                self.plot_start = True
            else:
                self.thread.serial_start = False
                self.thread.quit()
                self.thread.wait()
                self.control_btn.setText("Start plot")
                self.plot_start = False

    """
    Select source data.
    """
    def source_data(self, opt):
        selected = self.data_source[opt]
        self.source = selected
        if selected == 'Serial port':
            serial_source = SerialSourceDialog()
            if serial_source.exec_():
                self.serial_port = serial_source.source_port.text()
                self.serial_baud = int(serial_source.source_baud.text())

        if selected == 'HTTP API':
            http_source = HttpSourceDialog()
            if http_source.exec_():
                source_url = http_source.source_url.text()
                self.source_url = source_url

    """
    Get data via http.
    """
    def source_http(self):
        data = None
        try:
            response = requests.get(self.source_url)
            if response.status_code == 200:
                data = response.json()
                print(data)
        except requests.exceptions.ConnectionError as e:
            print(e)

        return data

    """
    Get data via serial port.
    """
    @pyqtSlot(str)
    def source_serial_port(self, data):
        self.cnt += self.interval
        data_str = data.split(",")
        self.temp = data_str[0]
        self.humidity = data_str[1]
        self.pressure = data_str[2]
        self.temp_value.display(self.temp)
        self.humidity_value.display(self.humidity)
        self.pressure_value.display(self.pressure)
        self.plot_temp.plot([self.cnt], [self.temp], pen=None, symbol="+", symbolSize=10)
        self.plot_humidity.plot([self.cnt], [self.humidity], pen=None, symbol="+", symbolSize=10)
        self.plot_pressure.plot([self.cnt], [self.pressure], pen=None, symbol="+", symbolSize=10)
        QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SenseEnvironment()
    sys.exit(app.exec_())
