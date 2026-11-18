"""
Description: header.py - Custom Component Header
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from styles import TEAL_BUTTON_STYLE, RED_BUTTON_STYLE

class Header(QWidget):
    def __init__(self, parent=None, password_table=None, form=None, generate_password=None):
        super().__init__(parent)
        # Create Layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # Other Attributes
        self.password_table = password_table
        self.form = form
        self.generate_password = generate_password
        # Create Widgets
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search passwords...")
        self.clear_button = QPushButton("Clear")
        self.delete_button = QPushButton("Delete")
        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet(TEAL_BUTTON_STYLE)
        self.edit_button.clicked.connect(self.edit_record)
        # Connect Signals
        self.searchbar.textChanged.connect(self.live_search)
        self.clear_button.clicked.connect(self.clear)
        self.delete_button.clicked.connect(self.delete_record)
        # Add Widgets
        self.layout.addWidget(self.searchbar)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.edit_button)

    def live_search(self, text):
        search_text = text.strip().lower()

        for row in range(self.password_table.rowCount()):

            match_found = False

            # Search Website, Username, and Password columns
            for column in range(self.password_table.columnCount()):

                item = self.password_table.item(row, column)

                if item and search_text in item.text().lower():
                    match_found = True
                    break

            # Show matching rows and hide nonmatching rows
            self.password_table.setRowHidden(row, not match_found)

    def clear(self):
        self.searchbar.clear()
        self.form.website_url_line_edit.clear()
        self.form.username_line_edit.clear()
        self.form.password_line_edit.clear()
        self.generate_password.generated_password.clear()



    def delete_record(self):
        selected_rows = self.password_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a record to delete.")
            return

        # Confirm deletion
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {len(selected_rows)} record(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        # Delete selected rows
        deleted_count = len(selected_rows)

        for index in sorted(selected_rows, reverse=True):
            self.password_table.removeRow(index.row())

        # Display success message
        QMessageBox.information(
            self,
            "Deletion Successful",
            f"Successfully deleted {deleted_count} record(s)."
        )

    def edit_record(self):

        # Cancel editing
        if self.edit_button.text() == "Cancel":
            self.form.clear_fields()
            self.form.editing_row = None

            # Reset buttons
            self.reset_edit_button()
            self.form.save_button.setText("Save")
            self.form.save_button.setStyleSheet(TEAL_BUTTON_STYLE)
            return

        # Get selected row
        selected_rows = self.password_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a record to edit."
            )
            return

        row = selected_rows[0].row()

        # Retrieve record information
        website = self.password_table.item(row, 0).text()
        username = self.password_table.item(row, 1).text()

        password_item = self.password_table.item(row, 2)
        password = password_item.data(Qt.ItemDataRole.UserRole)

        # Populate form fields
        self.form.populate_fields(website, username, password, row)

        # Switch to edit mode
        self.edit_button.setText("Cancel")
        self.edit_button.setStyleSheet(RED_BUTTON_STYLE)

        self.form.save_button.setText("Update")
        self.form.save_button.setStyleSheet(RED_BUTTON_STYLE)

    def reset_edit_button(self):
        self.edit_button.setText("Edit")
        self.edit_button.setStyleSheet(TEAL_BUTTON_STYLE)