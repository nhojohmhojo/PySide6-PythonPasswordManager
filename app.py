"""
Name: John R.
Date: 11/14/2026
Description: Python Password Manager with PySide6 GUI
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QCheckBox, QLabel
from PySide6.QtCore import Qt
from Components.header import Header
from Components.password_table import PasswordTable
from Components.form import Form
from Components.generate_password import GeneratePassword
from themes import LIGHT_THEME, DARK_THEME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__version__ = "0.0.1"
        # Window Setup
        self.setWindowTitle("Python Password Manager")
        self.setFixedSize(550, 660)
        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # Main Layout
        self.layout = QVBoxLayout(self.central_widget)
        # Custom Components
        self.password_table = PasswordTable(self)
        self.form = Form(self, self.password_table.table)
        self.generate_password = GeneratePassword(self, self.form)
        self.header = Header(self, self.password_table.table, self.form, self.generate_password)
        # Give Form access to Header
        self.form.header = self.header
        # Dark Mode
        self.dark_mode_switch = QCheckBox("Dark Mode")
        self.dark_mode_switch.toggled.connect(self.toggle_dark_mode)
        # Set default theme
        self.setStyleSheet(LIGHT_THEME)
        # Add Custom Components
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.password_table)
        self.layout.addWidget(self.form)
        self.layout.addWidget(self.generate_password, alignment=Qt.AlignmentFlag.AlignCenter)
        # Add Dark Mode Switch
        self.layout.addWidget(self.dark_mode_switch, alignment=Qt.AlignmentFlag.AlignCenter)
        # Version
        self.version_label = QLabel(f"v{self.__version__}")
        self.layout.addWidget(self.version_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def toggle_dark_mode(self, checked):
        if checked:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)


app = QApplication()

window = MainWindow()
window.show()

app.exec()