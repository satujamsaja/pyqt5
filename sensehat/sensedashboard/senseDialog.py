from PyQt5.QtWidgets import QDialog, QGroupBox, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QDialogButtonBox

"""
Http API connect dialog.
"""
class HttpSourceDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configure HTTP API")

        # Line edits.
        self.source_url = QLineEdit()
        self.source_url.setText('http://127.0.0.1:5000/api/sense')
        self.source_url.setFixedWidth(200)

        # Buttons
        self.dialog_button = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        self.dialog_button.accepted.connect(self.accept)
        self.dialog_button.rejected.connect(self.reject)

        # Init Layout.
        self.init_dialog()

    def init_dialog(self):
        # Group box
        source_group = QGroupBox()
        source_group_layout = QFormLayout()
        source_group_layout.addRow(QLabel("Source url"), self.source_url)
        source_group.setLayout(source_group_layout)

        # Main layout.
        main_layout = QVBoxLayout()
        main_layout.addWidget(source_group)
        main_layout.addWidget(self.dialog_button)
        self.setLayout(main_layout)


"""
Serial port connection dialog.
"""
class SerialSourceDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configure Serial Port")
        self.resize(300, 300)
        self.show()

    def init_dialog(self):
        pass

