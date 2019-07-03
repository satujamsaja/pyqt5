from PyQt5.QtWidgets import QDialog, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QDialogButtonBox


class ConnectDialog(QDialog):

    def __init__(self):
        super().__init__()
        # Line edits.
        self.server_url = QLineEdit()
        self.server_url.setText("http://127.0.0.1")
        self.server_port = QLineEdit()
        self.server_port.setText("8080")

        # Button
        self.dialog_button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        self.dialog_button.accepted.connect(self.accept)
        self.dialog_button.rejected.connect(self.reject)

        self.connect_dialog()

    def connect_dialog(self):
        self.setWindowTitle("Connect to server")
        self.resize(300, 150)

        # Layout
        connect_group = QGroupBox()
        connect_group_layout = QFormLayout()
        connect_group_layout.addRow(QLabel("Server:"), self.server_url)
        connect_group_layout.addRow(QLabel("Port"), self.server_port)
        connect_group.setLayout(connect_group_layout)

        # Main layout.
        main_layout = QVBoxLayout()
        main_layout.addWidget(connect_group)
        main_layout.addWidget(self.dialog_button)
        self.setLayout(main_layout)

