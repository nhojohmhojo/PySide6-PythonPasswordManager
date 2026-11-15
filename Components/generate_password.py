"""
Description: generate_password.py - Custom Component GeneratePassword
"""

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QSlider, QCheckBox, QApplication
from PySide6.QtCore import Qt
import secrets
import string
import pyperclip

class GeneratePassword(QWidget):

    def __init__(self, parent=None, form=None):
        super().__init__(parent)
        # Create Layout
        self.layout = QVBoxLayout(self)
        # Create Widgets
        self.generated_password = QLineEdit()
        self.generated_password.setReadOnly(True)
        self.generate_password_button = QPushButton("Generate Password")
        self.character_length_label = QLabel("Length: 16")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 50)
        self.slider.setValue(16)
        self.numbers_checkbox = QCheckBox("Numbers")
        self.special_characters_checkbox = QCheckBox("Special Characters")
        self.numbers_checkbox.setChecked(True)
        self.special_characters_checkbox.setChecked(True)
        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy)
        # Other Attributes
        self.form = form
        # Add Widgets
        self.layout.addWidget(self.generated_password)
        self.layout.addWidget(self.generate_password_button)
        self.layout.addWidget(self.character_length_label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.numbers_checkbox)
        self.layout.addWidget(self.special_characters_checkbox)
        self.layout.addWidget(self.copy_button)
        # Connect Signals
        self.slider.valueChanged.connect(self.update_length)
        self.generate_password_button.clicked.connect(self.generate_password)

    def update_length(self, value):
        self.character_length_label.setText(f"Length: {value}")

    def generate_password(self):
        min_length = self.slider.value()
        numbers = self.numbers_checkbox.isChecked()
        special_characters = self.special_characters_checkbox.isChecked()

        letters = string.ascii_letters
        digits = string.digits
        special = string.punctuation

        pool = letters

        if numbers:
            pool += digits

        if special_characters:
            pool += special

        # Guarantee required character types
        password = []

        if numbers:
            password.append(secrets.choice(digits))

        if special_characters:
            password.append(secrets.choice(special))

        # Fill remaining password length
        password += [
            secrets.choice(pool)
            for _ in range(min_length - len(password))
        ]

        # Shuffle characters
        secrets.SystemRandom().shuffle(password)

        # Display generated password
        self.generated_password.setText("".join(password))

    def copy(self):
        pyperclip.copy(self.generated_password.text())
