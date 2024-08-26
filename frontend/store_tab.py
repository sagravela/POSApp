from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from .utils import display_table, populate_items, filter_search, item_selected
from backend.services import save_item, remove_item_by_name

class StoreTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Store Filter Search Box and Item Table display
        self.filter_search, self.item_table = display_table(self)

        # Connect the input search with the table
        self.filter_search.textChanged.connect(lambda: filter_search(self.filter_search, self.item_table))

        # Connect to the selection change event
        self.item_table.selectionModel().selectionChanged.connect(lambda: self.selection(self.item_table))

        # Populate items
        populate_items(self.item_table)

        # Add to layout
        self.layout.addWidget(QLabel("Search Item:"))
        self.layout.addWidget(self.filter_search)
        self.layout.addWidget(QLabel("Items:"))
        self.layout.addWidget(self.item_table)

        # Item Name
        self.item_name_label = QLabel("Item Name:")
        self.item_name_input = QLineEdit()
        self.item_name_input.textChanged.connect(self.is_edited)
        self.layout.addWidget(self.item_name_label)
        self.layout.addWidget(self.item_name_input)

        # Item Price
        self.item_price_label = QLabel("Item Price:")
        self.item_price_input = QLineEdit()
        # Set a QDoubleValidator for the price input to ensure it's a valid float
        price_validator = QDoubleValidator(0.00, 100000.00, 2, self)
        price_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.item_price_input.setValidator(price_validator)
        self.item_price_input.textChanged.connect(self.is_edited)
        self.layout.addWidget(self.item_price_label)
        self.layout.addWidget(self.item_price_input)

        # Item Stock
        self.item_stock_label = QLabel("Item Stock:")
        self.item_stock_input = QSpinBox()
        # Ensure stock is an integer greater than or equal to 0
        self.item_stock_input.setMinimum(0)
        self.item_stock_input.setMaximum(1000000)
        self.item_stock_input.textChanged.connect(self.is_edited)
        self.layout.addWidget(self.item_stock_label)
        self.layout.addWidget(self.item_stock_input)

        # Remove Item Button
        self.remove_item_button = QPushButton("Remove Item")
        self.remove_item_button.clicked.connect(self.delete_item)
        self.remove_item_button.setEnabled(False)  # Initially disable the button
        self.layout.addWidget(self.remove_item_button)

        # Edit field button
        self.edit_item_button = QPushButton("Edit/Add Item")
        self.edit_item_button.clicked.connect(self.edit_add_item)
        self.edit_item_button.setEnabled(False)  # Initially disable the button
        self.layout.addWidget(self.edit_item_button)

        self.name, self.price, self.stock = None, None, None

    def selection(self, item_table):
        self.name, self.price, self.stock = item_selected(item_table)
        if self.name:
            self.item_name_input.setText(self.name)
            self.item_price_input.setText(str(self.price))
            self.item_stock_input.setValue(self.stock)
        self.remove_item_button.setEnabled(True)
        self.edit_item_button.setEnabled(False)

    def is_edited(self):
        # Normalize the input: replace comma with dot
        name, price, stock = self.item_name_input.text(), self.item_price_input.text(), self.item_stock_input.value()

        # Verify if there is selection and edition
        if self.name and self.price and self.stock:            
            if self.name != name or price != self.price or self.stock != stock:
                self.edit_item_button.setEnabled(True)

        # Verify if price is correctly inserted
        normalized_price = price.replace(',', '.')        
        # Temporarily set the normalized text to the input field to perform validation
        self.item_price_input.setText(normalized_price)

        if name and self.item_price_input.hasAcceptableInput():
            self.edit_item_button.setEnabled(True)
        else:
            self.edit_item_button.setEnabled(False)

    def delete_item(self):
        item_name = self.item_name_input.text()

        if item_name:
            # Call the backend function to remove the item
            remove_item_by_name(item_name)

            # Inform the user
            QMessageBox.information(self, "Success", f"Item '{item_name}' deleted successfully!")

            # Refresh table to reflect changes
            populate_items(self.item_table)

            # Clear input fields
            self.item_name_input.clear()
            self.item_price_input.clear()
            self.item_stock_input.setValue(0)
        else:
            QMessageBox.warning(self, "Warning", "Please select a item to delete.")

    def edit_add_item(self):
        name, price, stock = self.item_name_input.text(), self.item_price_input.text(), self.item_stock_input.value()

        # Ensure a item is selected
        if not name:
            QMessageBox.warning(self, "Warning", "No item selected for editing.")
            return

        # Update item in the database
        save_item(name, price, stock)  # Assuming save_item can handle updates

        QMessageBox.information(self, "Success", "Item updated successfully!")

        # Refresh the item table to reflect the changes
        populate_items(self.item_table)

        # Clear the input fields
        self.item_name_input.clear()
        self.item_price_input.clear()
        self.item_stock_input.setValue(0)

        # Disable the edit button after updating
        self.edit_item_button.setEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # Deselect all rows in the table
            self.item_table.clearSelection()
            
            # Clear input fields
            self.item_name_input.clear()
            self.item_price_input.clear()
            self.item_stock_input.setValue(0)
            
            # Optionally, disable the edit button
            self.remove_item_button.setEnabled(False)
            self.edit_item_button.setEnabled(False)