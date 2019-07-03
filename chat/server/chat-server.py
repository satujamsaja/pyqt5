"""
Chat Server
"""
import sys
from PyQt5.QtWidgets import QApplication, QGroupBox, QTextEdit, QMainWindow, QVBoxLayout, QWidget, QFormLayout, \
    QLineEdit, QLabel, QHBoxLayout, QPushButton
from chatThread import ChatThread
import yaml
import socketio, socketio.exceptions

class ChatServer(QMainWindow):

    def __init__(self):
        super().__init__()

        # Line edits.
        self.server_ip = QLineEdit()
        self.server_ip.setText("127.0.0.1")
        self.server_port = QLineEdit()
        self.server_port.setText("8080")
        self.server_message = QLineEdit()
        self.server_message.setPlaceholderText("Enter global message")

        # Buttons
        self.server_message_btn = QPushButton("Send")
        self.server_start_stop_btn = QPushButton("Start server")
        self.server_start_stop_btn.clicked.connect(self.server_start)

        # Text edit.
        self.server_log = QTextEdit()

        # Init UI
        self.setWindowTitle("Chat Server")
        self.statusBar().showMessage('Stopped')
        self.init_ui()
        self.show()

        # Init server.
        self.sio = socketio.Client()
        self.server_started = False
        self.chat_thread = ChatThread()
        self.sid = None
        self.server_config = None

        # Read server config.
        self.server_config_read()

    """
    Init UI
    """
    def init_ui(self):
        config_group = QGroupBox("SERVER CONFIGS")
        config_layout = QFormLayout()
        config_layout.addRow(QLabel('Server IP: '), self.server_ip)
        config_layout.addRow(QLabel('Server Port: '), self.server_port)
        config_group.setLayout(config_layout)
        server_message_layout = QHBoxLayout()
        server_message_layout.addWidget(self.server_message)
        server_message_layout.addWidget(self.server_message_btn)
        server_button_group = QGroupBox("SERVER CONTROL")
        server_button_layout = QHBoxLayout()
        server_button_layout.addWidget(self.server_start_stop_btn)
        server_button_group.setLayout(server_button_layout)
        main_layout = QVBoxLayout()
        main_layout.addWidget(config_group)
        main_layout.addWidget(server_button_group)

        # Central widget.
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    """
    Start server.
    """
    def server_start(self):
        # Save config.
        self.server_config_save()
        if self.server_started is False:
            self.chat_thread.start()
            self.server_start_stop_btn.setText("Stop server")
            self.server_started = True
            self.statusBar().showMessage("Started")
            self.server_log.append("Server started.")
        else:
            self.chat_thread.terminate()
            self.server_start_stop_btn.setText("Start server")
            self.server_log.append("Server stopped.")
            self.statusBar().showMessage("Stopper")
            self.server_started = False
    """
    Save server config.
    """
    def server_config_save(self):
        config = {
            'host': self.server_ip.text(),
            'port': self.server_port.text()
        }

        with open('server.yml', 'w') as config_file:
            yaml.dump(config, config_file)

    """
    Read server config.
    """
    def server_config_read(self):
        with open('server.yml', 'r') as config:
            server_config = yaml.load(config, Loader=yaml.SafeLoader)
            if server_config:
                self.server_config = server_config


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatServer()
    sys.exit(app.exec_())
