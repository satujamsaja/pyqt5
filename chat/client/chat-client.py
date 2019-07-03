"""
Chat client
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QTextEdit, \
    QHBoxLayout, QPushButton, QMainWindow, QAction
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QCoreApplication
from connectDialog import ConnectDialog
import yaml
import socketio
import socketio.exceptions



class ChatClient(QMainWindow):

    def __init__(self):
        super().__init__()
        # Window
        self.setWindowTitle("Chat")

        # Socket IO
        self.sid = None
        self.join = False
        self.current_channel = None

        # Line edits.
        self.nickname = QLineEdit()
        self.nickname.setReadOnly(True)
        self.channel = QLineEdit()
        self.channel.setReadOnly(True)
        self.message = QLineEdit()
        self.message.setFixedWidth(150)
        self.message.setReadOnly(True)

        # Buttons.
        self.send = QPushButton("Send")
        self.send.clicked.connect(self.send_message)

        # Text area.
        self.chatbox = QTextEdit()
        self.chatbox.setReadOnly(True)

        # Init UI
        self.statusBar().showMessage("Disconnected")
        self.init_ui()
        self.show()

        # Server
        self.sio = socketio.Client()
        self.client_config = None

    """
    Chat top layout, nickname and channel.
    """
    def chat_layout(self):
        chat_box = QGroupBox("")
        chat_top_layout = QFormLayout()
        chat_top_layout.addRow(QLabel('Nickname:'), self.nickname)
        chat_top_layout.addRow(QLabel('Channel'), self.channel)
        chat_box.setLayout(chat_top_layout)
        return chat_box

    """
    Chat box message, message and send button.
    """
    def chat_bottom(self):
        text_group = QGroupBox("")
        text_box = QHBoxLayout()
        text_box.addWidget(self.message)
        text_box.addStretch()
        text_box.addWidget(self.send)
        text_group.setLayout(text_box)
        return text_group

    """
    Init chat ui.
    """
    def init_ui(self):
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.chat_layout())
        main_layout.addWidget(self.chatbox)
        main_layout.addWidget(self.chat_bottom())

        # Central widget
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Add menu.
        chat_connect = QAction('Connect', self)
        chat_connect.triggered.connect(self.chat_connect)
        chat_exit = QAction('Exit', self)
        chat_exit.triggered.connect(self.chat_exit)

        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        connect_menu = menu.addMenu('&Chat')
        connect_menu.addAction(chat_connect)
        connect_menu.addAction(chat_exit)

    """
    Chat connect dialog.
    """
    def chat_connect(self):
        connect_server_dialog = ConnectDialog()
        if connect_server_dialog.exec_():
            server = connect_server_dialog.server_url.text()
            port = connect_server_dialog.server_port.text()
            if server and port:
                # Save config.
                config = {
                    'server': server,
                    'port': port
                }

                with open('client.yml', 'w') as config_file:
                    yaml.dump(config, config_file)
                self.chat_connect_server()

    """
    Connect to chat server.
    """
    def chat_connect_server(self):
        with open('client.yml', 'r') as config:
            client_config = yaml.load(config, Loader=yaml.SafeLoader)
            if client_config:
                self.client_config = client_config

        # Start server.
        if self.client_config is not None:
            server = self.client_config.get('server')
            port = int(self.client_config.get('port'))
            try:
                chat_server = '{}:{}'.format(server, port)
                self.sio.connect(chat_server)
                self.sio.on('room', self.receive_response)
                self.nickname.setReadOnly(False)
                self.channel.setReadOnly(False)
                self.message.setReadOnly(False)
                self.statusBar().showMessage('Connected')
            except socketio.exceptions.ConnectionError as e:
                print(e)

    """
    Disconnect from chat server.
    TODO: need to find a way to prevent app crash.
    """
    def chat_exit(self):
        self.sio.emit('disconnect_request')
        self.sio.disconnect()
        QCoreApplication.quit()


    """
    Send message to chat room.
    """
    def send_message(self):
        msg = self.message.text()
        if msg != "" and self.channel.text():
            if self.current_channel is None and self.channel.text():
                self.current_channel = self.channel.text()
                self.sio.emit('join', {'room': self.current_channel})
                self.join = True
            elif self.current_channel != self.channel.text():
                self.sio.emit('leave', {'root': self.current_channel})
                self.current_channel = self.channel.text()
                self.sio.emit('join', {'room': self.current_channel})

            if self.current_channel:
                chat_prefix = "{}: {}".format(self.nickname.text(), msg)
                self.sio.emit('room_event', {'room': self.channel.text(), 'data': chat_prefix})
                self.chatbox.append(chat_prefix)
                self.chatbox.moveCursor(QTextCursor.End)
                self.message.clear()
        self.setWindowTitle("Chat: " + "@{} in #{}".format(self.nickname.text(), self.channel.text()))

    def receive_response(self, data):
        if data:
            self.chatbox.append(data.get('data'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatClient()
    sys.exit(app.exec_())





