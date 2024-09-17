from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QTableWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QSpinBox, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QDoubleValidator, QIcon, QKeyEvent
from .utils import display_table, populate_table, filter_search, item_selected
from backend.services import save_item, remove_item_by_name
from backend.path import get_resource_path
import os

class StoreTab(QWidget):
    """
    Class representing the Store management tab in the application.
    Allows users to filter, view, add, edit, and remove items from the store inventory.
    """
    def __init__(self, parent: QMainWindow =None):
        """
        Initializes the Store tab and sets up the layout, widgets, and connections.

        This method sets up the vertical layout, item filter search box, item table,
        and input fields for item name, price, and stock. It also initializes buttons
        for adding, editing, and removing items and their respective signals.

        Parameters
        ----------
        parent : QMainWindow, optional
            The parent widget for the Store tab. Defaults to None.
        """
        super().__init__(parent)

        self.v_layout = QVBoxLayout(self)

        # Empty widget to fill the space
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Store Filter Search Box and Item Table display
        self.filter_search, self.item_table = display_table(self)

        # Connect the input search with the table
        self.filter_search.textChanged.connect(lambda: filter_search(self.filter_search, self.item_table))

        # Connect to the selection change event
        self.item_table.selectionModel().selectionChanged.connect(lambda: self.selection(self.item_table))

        # Populate items
        populate_table(self.item_table)

        # Add to layout
        self.v_layout.addWidget(self.filter_search)
        self.v_layout.addWidget(self.item_table)
        self.v_layout.addItem(self.spacer)

        # Horizontal Layout as container
        self.grid_layout = QGridLayout()

        # Item Name
        self.item_name_label = QLabel("Item Name:")
        self.item_name_input = QLineEdit()
        self.item_name_input.textChanged.connect(self.is_edited)
        self.grid_layout.addWidget(self.item_name_label, 0, 0)
        self.grid_layout.addWidget(self.item_name_input, 1, 0)

        # Item Price
        self.item_price_label = QLabel("Item Price:")
        self.item_price_input = QLineEdit()
        # Set a QDoubleValidator for the price input to ensure it's a valid float
        price_validator = QDoubleValidator(0.00, 100000.00, 2, self)
        price_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.item_price_input.setValidator(price_validator)
        self.item_price_input.textChanged.connect(self.is_edited)
        self.grid_layout.addWidget(self.item_price_label, 0, 1)
        self.grid_layout.addWidget(self.item_price_input, 1, 1)

        # Item Stock
        self.item_stock_label = QLabel("Item Stock:")
        self.item_stock_input = QSpinBox()
        # Ensure stock is an integer greater than or equal to 0
        self.item_stock_input.setMinimum(0)
        self.item_stock_input.setMaximum(1000000)
        self.item_stock_input.textChanged.connect(self.is_edited)
        self.grid_layout.addWidget(self.item_stock_label, 0, 2)
        self.grid_layout.addWidget(self.item_stock_input, 1, 2)

        # Remove Item Button
        self.remove_item_button = QPushButton("  Remove Item")
        self.remove_item_button.setObjectName("removeItemButton")
        remove_icon = get_resource_path(os.path.join("assets", "remove.png"))
        self.remove_item_button.setIcon(QIcon(remove_icon))
        self.remove_item_button.setIconSize(QSize(20, 20))
        self.remove_item_button.clicked.connect(self.delete_item)
        self.remove_item_button.setEnabled(False)  # Initially disable the button
        self.grid_layout.addWidget(self.remove_item_button, 0, 3)

        # Edit field button
        self.edit_item_button = QPushButton("  Edit/Add Item")
        self.edit_item_button.setObjectName("editItemButton")
        add_edit_icon = get_resource_path(os.path.join("assets", "add_edit.png"))
        self.edit_item_button.setIcon(QIcon(add_edit_icon))
        self.edit_item_button.setIconSize(QSize(20, 20))
        self.edit_item_button.clicked.connect(self.edit_add_item)
        self.edit_item_button.setEnabled(False)  # Initially disable the button
        self.grid_layout.addWidget(self.edit_item_button, 1, 3)

        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addItem(self.spacer)

        self.name, self.price, self.stock = None, None, None

    def selection(self, item_table: QTableWidget):
        """
        Handles item selection from the table and updates the input fields accordingly.

        When a row is selected in the item table, this method retrieves the item's
        name, price, and stock and populates the respective input fields. It also
        enables the 'Remove Item' button and disables the 'Edit/Add Item' button until
        an edit is detected.

        Parameters
        ----------
        item_table : QTableWidget
            The table widget displaying the list of available items in store.
        """
        self.name, self.price, self.stock = item_selected(item_table)
        if self.name:
            self.item_name_input.setText(self.name)
            self.item_name_input.setEnabled(False)
            self.item_price_input.setText(str(self.price))
            self.item_stock_input.setValue(self.stock)
        self.remove_item_button.setEnabled(True)
        self.edit_item_button.setEnabled(False)

    def is_edited(self):
        """
        Monitors the input fields for any changes and enables the 'Edit/Add Item' button.

        This method checks if the current values in the input fields differ from the
        originally selected item's values (name, price, stock). It also validates
        the price input to ensure it contains a valid floating-point number.

        If changes are detected and the input is valid, the 'Edit/Add Item' button
        is enabled; otherwise, it remains disabled.
        """
        name, price, stock = self.item_name_input.text(), self.item_price_input.text(), self.item_stock_input.value()

        # Verify if there is selection and edition
        if self.name and self.price and self.stock:            
            if self.name != name or price != self.price or self.stock != stock:
                self.edit_item_button.setEnabled(True)

        # Normalize the input: replace comma with dot
        normalized_price = price.replace(',', '.')        
        # Temporarily set the normalized text to the input field to perform validation
        self.item_price_input.setText(normalized_price)

        if name and self.item_price_input.hasAcceptableInput():
            self.edit_item_button.setEnabled(True)
        else:
            self.edit_item_button.setEnabled(False)

    def delete_item(self):
        """
        Deletes the selected item from the store inventory.

        This method retrieves the name of the currently selected item and removes
        it from the database. Upon successful deletion, a message box informs the user,
        and the item table is refreshed. The input fields are also cleared after the
        deletion.

        Raises
        ------
        QMessageBox
            Displays a confirmation message after successful deletion.
        """        
        item_name = self.item_name_input.text()

        # Call the backend function to remove the item
        remove_item_by_name(item_name)

        # Inform the user
        QMessageBox.information(self, "Success", f"Item '{item_name}' deleted successfully!")

        # Refresh tab
        self.refresh()

    def edit_add_item(self):
        """
        Adds or edits an item in the store inventory.

        This method saves the current values from the input fields (name, price, stock)
        to the database. If the item already exists, it is updated; otherwise, a new
        entry is created. Upon successful save, a message box confirms the action, the
        item table is refreshed, and the input fields are cleared.

        Raises
        ------
        QMessageBox
            Displays a confirmation message after the item is successfully added or edited.
        """
        name, price, stock = self.item_name_input.text(), self.item_price_input.text(), self.item_stock_input.value()
        
        # Update item in the database
        save_item(name, price, stock)  # Assuming save_item can handle updates

        QMessageBox.information(self, "Success", "Item updated successfully!")

        # Refresh tab
        self.refresh()

    def refresh(self):
        """
        It refreshes the table, clears the item table selection, input fields, and disable some buttons.
        """
        # Refresh the item table to reflect the changes
        populate_table(self.item_table)

        # Deselect all rows in the table
        self.item_table.clearSelection()
        
        # Clear input fields
        self.filter_search.clear()
        self.item_name_input.clear()
        self.item_price_input.clear()
        self.item_stock_input.setValue(0)
        
        # Enable input name
        self.item_name_input.setEnabled(True)

        # Disable buttons
        self.remove_item_button.setEnabled(False)
        self.edit_item_button.setEnabled(False)

    def keyPressEvent(self, event: QKeyEvent):
        """
        This method is triggered when the user presses the Escape key. 

        Parameters
        ----------
        event : QKeyEvent
            The key event that triggers the method.
        """
        if event.key() == Qt.Key.Key_Escape:
            self.refresh()
