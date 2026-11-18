
"""
Description: form.py - Custom Component Form
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QTableWidgetItem
import pyperclip
from styles import TEAL_BUTTON_STYLE


class Form(QWidget):

    def __init__(self, parent=None, password_table=None):
        super().__init__(parent)

        # Create Layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Other Attributes
        self.password_table = password_table
        self.header = None
        self.editing_row = None

        # Create Widgets
        self.website_url_line_edit = QLineEdit()
        self.website_url_line_edit.setPlaceholderText("Website URL")

        self.username_line_edit = QLineEdit()
        self.username_line_edit.setPlaceholderText("Username")

        self.password_line_edit = QLineEdit()
        self.password_line_edit.setPlaceholderText("Password")

        self.paste_button = QPushButton("Paste")
        self.paste_button.clicked.connect(self.paste)

        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(TEAL_BUTTON_STYLE)

        # Connect Signals
        self.save_button.clicked.connect(self.handle_save_button)

        # Add Widgets
        self.layout.addWidget(self.website_url_line_edit)
        self.layout.addWidget(self.username_line_edit)
        self.layout.addWidget(self.password_line_edit)
        self.layout.addWidget(self.paste_button)
        self.layout.addWidget(self.save_button)

    def paste(self):
        clipboard_text = pyperclip.paste()
        self.password_line_edit.setText(clipboard_text)

    def handle_save_button(self):
        if self.editing_row is not None:
            self.update_record()
        else:
            self.save_record()

    def save_record(self):

        website = self.website_url_line_edit.text().strip()
        username = self.username_line_edit.text().strip()
        password = self.password_line_edit.text().strip()

        # Validate Inputs
        if not website or not username or not password:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        # Get Current Row
        row = self.password_table.rowCount()

        # Insert New Row
        self.password_table.insertRow(row)

        # Website
        self.password_table.setItem(row, 0, QTableWidgetItem(website))

        # Username
        self.password_table.setItem(row, 1, QTableWidgetItem(username))

        # Password (Initially Hidden)
        password_item = QTableWidgetItem("•" * len(password))
        password_item.setData(Qt.ItemDataRole.UserRole, password)

        self.password_table.setItem(row, 2, password_item)

        # Show / Hide Button
        toggle_button = QPushButton("Show")
        toggle_button.clicked.connect(lambda checked=False, r=row: self.toggle_password(r))

        self.password_table.setCellWidget(row, 3, toggle_button)

        # Clear Inputs
        self.clear_fields()

        # Success Message
        QMessageBox.information(self, "Password Saved", "You've successfully saved a password!")

    def toggle_password(self, row):

        password_item = self.password_table.item(row, 2)
        toggle_button = self.password_table.cellWidget(row, 3)

        if password_item is None or toggle_button is None:
            return

        password = password_item.data(Qt.ItemDataRole.UserRole)

        if toggle_button.text() == "Show":
            password_item.setText(password)
            toggle_button.setText("Hide")
        else:
            password_item.setText("•" * len(password))
            toggle_button.setText("Show")

    def populate_fields(self, website, username, password, row):

        self.editing_row = row

        self.website_url_line_edit.setText(website)
        self.username_line_edit.setText(username)
        self.password_line_edit.setText(password)

    def update_record(self):

        website = self.website_url_line_edit.text().strip()
        username = self.username_line_edit.text().strip()
        password = self.password_line_edit.text().strip()

        # Validate Inputs
        if not website or not username or not password:
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return

        if self.editing_row is None:
            return

        row = self.editing_row

        # Update Website
        self.password_table.setItem(row, 0, QTableWidgetItem(website))

        # Update Username
        self.password_table.setItem(row, 1, QTableWidgetItem(username))

        # Update Password (Initially Hidden)
        password_item = QTableWidgetItem("•" * len(password))
        password_item.setData(Qt.ItemDataRole.UserRole, password)

        self.password_table.setItem(row, 2, password_item)

        # Reset Show / Hide Button
        toggle_button = self.password_table.cellWidget(row, 3)

        if toggle_button is not None:
            toggle_button.setText("Show")

        # Exit Edit Mode
        self.editing_row = None

        # Reset Button Text
        self.save_button.setText("Save")
        self.save_button.setStyleSheet(TEAL_BUTTON_STYLE)

        if self.header is not None:
            self.header.reset_edit_button()

        # Clear Form
        self.clear_fields()

        # Success Message
        QMessageBox.information(
            self,
            "Update Successful",
            "You've successfully updated your password!"
        )

    def clear_fields(self):

        self.website_url_line_edit.clear()
        self.username_line_edit.clear()
        self.password_line_edit.clear()
