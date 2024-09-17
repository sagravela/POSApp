from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QSpinBox, QSizePolicy, 
    QSpacerItem, QListWidget, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QDoubleValidator, QKeyEvent
from .utils import display_table, populate_table, filter_search, item_selected
from backend.services import save_transaction, discount_stock
from backend.path import get_resource_path
import os, re


class POSTab(QWidget):
    """
    Class representing the Point of Sale (POS) tab in the application.
    Allows users to manage product selection, add items to cart, and perform transactions.
    """
    def __init__(self, parent: QMainWindow =None):
        """
        Initializes the POS tab and sets up the layout, widgets, and connections.

        This method is responsible for setting up the main vertical layout,
        search filter, item table, cart, quantity input, and buttons for managing
        transactions. It also initializes the default values and signals.

        Parameters
        ----------
        parent : QMainWindow, optional
            The parent widget for the POS tab. Defaults to None.
        """
        super().__init__(parent)
        
        # Main vertical layout for the entire POS tab
        self.v_layout = QVBoxLayout(self)

        # Spacer item for adding empty space in layouts
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Create search filter and item table for displaying products
        self.filter_search, self.item_table = display_table(self)
        
        # Connect the search box text change to the filter function
        self.filter_search.textChanged.connect(lambda: filter_search(self.filter_search, self.item_table))

        # Connect the selection change event to update selected item details
        self.item_table.selectionModel().selectionChanged.connect(lambda: self.selection(self.item_table))

        # Populate the table with items
        populate_table(self.item_table)

        # Layout for holding the table and icon
        self.table_icon = QHBoxLayout()

        # QLabel to display an icon
        icon_label = QLabel()
        icon_pixmap = QPixmap(get_resource_path(os.path.join("assets", "pos.ico")))
        icon_label.setPixmap(icon_pixmap)        

        # Spacer item to add padding between table and icon
        space = QSpacerItem(60, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        # Add table and icon to the horizontal layout
        self.table_icon.addWidget(self.item_table)
        self.table_icon.addItem(space)
        self.table_icon.addWidget(icon_label)
        self.table_icon.addItem(space)

        # Add the filter search box and table layout to the main vertical layout
        self.v_layout.addWidget(self.filter_search)
        self.v_layout.addLayout(self.table_icon)

        # Quantity input section
        self.quantity_layout = QHBoxLayout()
        self.quantity_label = QLabel("Quantity:")
        self.quantity_label.setObjectName("quantityLabel")
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(1000000)
        self.quantity_layout.addWidget(self.quantity_label)
        self.quantity_layout.addWidget(self.quantity_input)
        self.quantity_layout.addItem(self.spacer)
        self.v_layout.addLayout(self.quantity_layout)

        # Cart display list
        self.cart_list = QListWidget()
        self.cart_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.v_layout.addWidget(QLabel("Cart:"))
        self.v_layout.addWidget(self.cart_list)

        # Container for holding total price, amount received input, and buttons
        self.container = QHBoxLayout()

        # Add empty space to the container
        self.container.addItem(self.spacer)

        # Layout for displaying the total price
        self.total_price = QVBoxLayout()
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setObjectName("totalLabel")
        self.total_price.addItem(self.spacer)
        self.total_price.addWidget(self.total_label)
        self.total_price.addItem(self.spacer)
        self.container.addLayout(self.total_price)

        # Input field for the received amount
        self.received_amount = QVBoxLayout()
        self.received_amount_label = QLabel("Amount Received:")
        self.received_amount.addWidget(self.received_amount_label)
        self.amount = QHBoxLayout()
        self.price_label = QLabel("$")
        self.price_label.setObjectName("priceLabel")
        self.received_amount_input = QLineEdit()
        self.received_amount_input.setObjectName("receivedAmountInput")
        self.amount_validator = QDoubleValidator(0.0, 1e10, 2)  # Min 0, Max 1e10, 2 decimal places
        self.received_amount_input.setValidator(self.amount_validator)
        self.amount.addWidget(self.price_label)
        self.amount.addWidget(self.received_amount_input)
        self.amount.addItem(self.spacer)
        self.received_amount.addLayout(self.amount)
        self.received_amount.addItem(self.spacer)
        self.container.addLayout(self.received_amount)

        # Buttons for adding to cart, clearing, and checkout
        self.button_layout = QVBoxLayout()
        self.button_layout.setObjectName("buttonLayout")

        self.add_button = QPushButton("  Add to Cart")
        self.add_button.setObjectName("addToCartButton")
        add_icon_path = get_resource_path(os.path.join("assets", "cart.png"))
        self.add_button.setIcon(QIcon(add_icon_path))
        self.add_button.setIconSize(QSize(20, 20))
        self.add_button.setEnabled(False)  # Initially disable the button
        self.add_button.clicked.connect(self.add_to_cart)
        self.button_layout.addWidget(self.add_button)

        self.clear_button = QPushButton("  Clear")
        self.clear_button.setObjectName("clearButton")
        clear_icon_path = get_resource_path(os.path.join("assets", "clear.png"))
        self.clear_button.setIcon(QIcon(clear_icon_path))
        self.clear_button.setIconSize(QSize(20, 20))
        self.clear_button.setEnabled(False)
        self.clear_button.clicked.connect(self.clear_cart)
        self.button_layout.addWidget(self.clear_button)

        self.checkout_button = QPushButton("  Checkout")
        self.checkout_button.setObjectName("checkoutButton")
        checkout_icon_path = get_resource_path(os.path.join("assets", "checkout.png"))
        self.checkout_button.setIcon(QIcon(checkout_icon_path))
        self.checkout_button.setIconSize(QSize(20, 20))
        self.checkout_button.setEnabled(False)
        self.checkout_button.clicked.connect(self.checkout)
        self.button_layout.addWidget(self.checkout_button)

        self.container.addLayout(self.button_layout)

        # Add empty space to the container
        self.container.addItem(self.spacer)

        self.v_layout.addLayout(self.container)

        # Initialize variables
        self.total_price = 0
        self.cart = []
        self.name, self.price, self.stock = None, None, None
    
    def selection(self, item_table: QTableWidget):
        """
        Handles item selection from the item table.

        When a user selects an item from the table, this method retrieves
        the item name, price, and stock, and enables the "Add to Cart" button
        if the item is not already in the cart.

        Parameters
        ----------
        item_table : QTableWidget
            The table widget displaying the list of available items for sale.
        """
        self.name, self.price, self.stock = item_selected(item_table)
        
        # Enable 'Add to Cart' button only if the selected item isn't in the cart
        if self.name not in [i[0] for i in self.cart]:
            self.add_button.setEnabled(True)
        else:
            self.add_button.setEnabled(False)

    def add_to_cart(self):
        """
        Adds the selected item to the cart.

        This method checks if a valid item and quantity are selected,
        and adds the item to the cart. It updates the total price
        and enables the necessary buttons for further actions.

        Raises
        ------
        QMessageBox
            If no item is selected or if the requested quantity exceeds stock.
        """
        if self.name == "":
            QMessageBox.warning(self, "No Item Selected", "Please select an item from the list above.")
            return

        self.quantity = self.quantity_input.value()

        # Check if the requested quantity exceeds the available stock
        if self.quantity > self.stock:
            QMessageBox.warning(self, "Invalid Quantity", "Not enough stock. Please select a valid quantity.")
            self.quantity_input.setValue(1)
            return
        
        total_item_price = self.price * self.quantity
        self.total_price += total_item_price

        # Add the item to the cart list and update the display
        self.cart.append((self.name, self.quantity))
        cart_text = f"{self.name}: {self.quantity} x ${self.price:.2f} = ${total_item_price:.2f}"
        self.cart_list.addItem(cart_text)

        # Update the total price label
        self.total_label.setText(f"Total: ${self.total_price:.2f}")

        # Reset the quantity input to 1
        self.quantity_input.setValue(1)

        # Enable the clear and checkout buttons
        self.clear_button.setEnabled(True)
        self.checkout_button.setEnabled(True)

        # Disable the 'Add to Cart' button
        self.add_button.setEnabled(False)

    def clear_cart(self):
        """
        Clears the selected items or the entire cart.

        This method either removes selected items from the cart or clears
        all items if no specific item is selected. It updates the total price
        and disables buttons if the cart becomes empty.
        """
        selected_items = self.cart_list.selectedItems()
        
        if selected_items:
            for item in selected_items:
                row = self.cart_list.row(item)
                item_text = item.text()
                
                # Use regex to extract name and quantity from the item text
                match = re.match(r"^(.*?): (\d+) x \$.+ = \$(\d+\.\d{2})$", item_text)
                if match:
                    name = match.group(1)
                    quantity = int(match.group(2))
                    total_price = float(match.group(3))
                    
                    # Remove item from self.cart
                    if (name, quantity) in self.cart:
                        self.cart.remove((name, quantity))
                        self.total_price -= total_price
                        self.total_label.setText(f"Total: ${self.total_price:.2f}")
                
                # Remove item from cart list
                self.cart_list.takeItem(row)
            
            self.cart_list.clearSelection()  # Unselect all items in the cart list

        else:
            # Clear all items if no specific item is selected
            self.total_price = 0.0
            self.cart.clear()
            self.cart_list.clear()
            self.total_label.setText("Total: $0.00")

        # Clear table selection
        self.item_table.clearSelection()

        # Disable Clear and Checkout buttons if the cart list is empty
        if len(self.cart_list) == 0:
            self.clear_button.setEnabled(False)
            self.checkout_button.setEnabled(False)

    def checkout(self):
        """
        Completes the transaction, updates the stock, and resets the cart.

        This method handles the checkout process by validating the amount received,
        saving the transaction, and updating the stock. It then clears the cart
        and resets relevant fields.

        Raises
        ------
        QMessageBox
            If the received amount is invalid or insufficient.
            After a succesful transaction, display the change to return.
        """
        amount_received = self.received_amount_input.text()
        if not amount_received:
            QMessageBox.warning(self, "Amount Required", "Please enter the amount received.")
            return
        
        amount_received = float(amount_received)
        if amount_received < self.total_price:
            QMessageBox.warning(self, "Insufficient Amount", "The received amount is less than the total price.")
            self.received_amount_input.clear()
            return

        # Calculate the change to return
        change = amount_received - self.total_price
        
        # Save the transaction
        items = save_transaction(self.total_price, amount_received, change, self.cart)
        
        # Update the stock
        discount_stock(items)
        
        # Clear the cart and reset the total price
        self.clear_cart()

        # Clear the received amount input field
        self.received_amount_input.clear()

        # Reset the total price label
        self.total_label.setText("Total: $0.00")

        # Refresh the item table to reflect the changes
        populate_table(self.item_table)        
        
        QMessageBox.information(self, "Success", f"Transaction successful!\nChange to return: ${change:.2f}")

    def refresh(self):
        """
        It refreshes the table, clears the item table selection, input fields, and disable some buttons.
        """
        # Refresh the item table to reflect the changes
        populate_table(self.item_table)

        # Deselect all rows in the table
        self.item_table.clearSelection()

        # Deselect item in the cart list
        self.cart_list.clearSelection()
        
        # Clear input fields
        self.filter_search.clear()
        self.received_amount_input.clear()
        self.quantity_input.setValue(1)

        # Disable Add to cart button
        self.add_button.setEnabled(False)

    def keyPressEvent(self, event: QKeyEvent):
        """
        This method is triggered when the user presses the Escape key.

        Parameters
        ----------
        event : QKeyEvent
            The key press event object containing information about the key pressed.
        """
        if event.key() == Qt.Key.Key_Escape:
            self.refresh()
