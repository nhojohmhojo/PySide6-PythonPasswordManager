"""
Description: password_table.py - Custom Component PasswordTable
"""

import csv
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, \
    QMessageBox, QHeaderView


class PasswordTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create Layout
        self.layout = QVBoxLayout(self)

        # Create Widgets
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)

        self.headers = ["Website", "Username", "Password", "Toggle"]
        self.table.setHorizontalHeaderLabels(self.headers)
        # Stretch Website, Username, and Password columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Make Toggle column smaller
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        # Set Column Width
        self.table.setColumnWidth(3, 80)
        # Hide row index
        self.table.verticalHeader().setVisible(False)
        # Make cells read-only
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Select row
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        # Allow multiple row selections
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # Import CSV
        self.import_button = QPushButton("Import CSV")
        self.import_button.clicked.connect(self.import_csv)

        # Add Widgets to Layout
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.import_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_toggle_button(self, row):
        """Create a Show/Hide button for a password row."""

        toggle_button = QPushButton("Show")
        toggle_button.clicked.connect(self.toggle_password)

        self.table.setCellWidget(row, 3, toggle_button)

    def toggle_password(self):
        """Show or hide the password belonging to the clicked button."""

        toggle_button = self.sender()

        if not isinstance(toggle_button, QPushButton):
            return

        # Find the button's current row
        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 3) == toggle_button:
                break
        else:
            return

        password_item = self.table.item(row, 2)

        if not password_item:
            return

        password = password_item.data(Qt.ItemDataRole.UserRole)

        if password is None:
            return

        if toggle_button.text() == "Show":
            password_item.setText(password)
            toggle_button.setText("Hide")
        else:
            password_item.setText("•" * len(password))
            toggle_button.setText("Show")

    def import_csv(self):
        # Open File Dialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Import CSV", "", "CSV Files (*.csv)")

        if not file_path:
            return

        # Accepted CSV heading names
        synonym_map = {
            "website": ["website", "site", "url", "domain", "web address"],
            "username": ["username", "user", "login", "email", "account"],
            "password": ["password", "pass", "pwd", "secret"]
        }

        try:
            with open(
                    file_path, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                # Normalize CSV headings
                headers = {
                    header.strip().lower(): header
                    for header in (reader.fieldnames or [])
                    if header
                }

                # Map CSV headings to standard field names
                column_map = {}

                for field, synonyms in synonym_map.items():
                    for synonym in synonyms:
                        if synonym in headers:
                            column_map[field] = headers[synonym]
                            break

                # Validate CSV headings
                if len(column_map) != len(synonym_map):
                    QMessageBox.warning(self, "Invalid CSV","CSV must contain Website, Username, and Password columns.")
                    return

                imported = 0

                for record in reader:
                    website = (record.get(column_map["website"]) or "").strip()
                    username = (record.get(column_map["username"]) or "").strip()
                    password = (record.get(column_map["password"]) or "").strip()

                    if not website or not username or not password:
                        continue

                    # Get Current Row
                    row = self.table.rowCount()

                    # Insert New Row
                    self.table.insertRow(row)
                    # Website
                    self.table.setItem(row, 0, QTableWidgetItem(website))
                    # Username
                    self.table.setItem(row, 1, QTableWidgetItem(username))

                    # Password (Initially Hidden)
                    password_item = QTableWidgetItem("•" * len(password))
                    password_item.setData(Qt.ItemDataRole.UserRole, password)
                    self.table.setItem(row, 2, password_item)
                    # Create Show / Hide Button
                    self.create_toggle_button(row)

                    imported += 1

            QMessageBox.information(
                self,
                "Import Complete",
                f"Successfully imported {imported} records."
            )

        except (OSError, UnicodeError, csv.Error) as error:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Could not import CSV file:\n{error}"
            )